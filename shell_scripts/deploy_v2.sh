#!/bin/bash

# 檢查參數是否提供正確
if [ $# -ne 2 ]; then
  echo "Usage: $0 <local_file_path> <remote_ip_address>"
  exit 1
fi


# 獲取參數
LOCAL_FILE_PATH=$1
REMOTE_IP_ADDRESS=$2


echo "scp $LOCAL_FILE_PATH  ap@$REMOTE_IP_ADDRESS:/home/ap"

# 複製檔案到遠端伺服器
scp "$LOCAL_FILE_PATH" "ap@$REMOTE_IP_ADDRESS:/home/ap"

read -sp "Enter sudo password: " sudo_pass

# 連接到遠端伺服器並執行後續命令
# ssh "root@$REMOTE_IP_ADDRESS" << EOF
sshpass -p "$sudo_pass" ssh ap@"$REMOTE_IP_ADDRESS" <<EOF
  echo "$sudo_pass" | sudo -S bash -c '


    execute_in_nginx_container() {
      version="\$1"
      echo ">>> version: \$version ..."
      rolling_command="bash ./shell_scripts/rolling-update.sh"
      if docker ps --filter "name=nginx" --filter "status=running" | grep -q "nginx"; then
        echo ">>> 執行 Nginx 容器內的指令"
        echo ">>> \$rolling_command \$version"
        docker exec nginx sh -c "\$rolling_command \$version"
        echo ">>> Nginx 容器指令執行完成"
      else
        echo "Error: Nginx 容器未運行"
        exit 1
      fi
    }
    
    check_service_response() {
      url="\$1"
      max_retries=5
      wait_time=3
      attempt=1
      echo ">>> 對 \$url 進行服務檢查..."
      while [ "\$attempt" -le "\$max_retries" ];do
        echo ">>> 嘗試第 \$attempt 次檢查服務狀態..."
        curl -o /dev/null -s -w "%{http_code}\n" \$url > /tmp/response.txt
        status_code=\$(cat /tmp/response.txt)
        echo \$response
        if [ "\$status_code" -eq 200 ]; then
          echo ">>> 請求成功，返回狀態碼為 200"
          break
        fi
        if [ "\$attempt" -eq "\$max_retries" ]; then
          echo ">>> 請求失敗，超過最大重試次數"
          exit 1
        fi
        echo ">>> 服務尚未啟動，等待 \$wait_time 秒後重試..."
        sleep "\$wait_time"
        let attempt=attempt+1
      done
    }

    mv /home/ap/da.tar.gz /root/da.tar.gz

    # 提取檔案名稱
    FILENAME=\$(basename "$LOCAL_FILE_PATH")

    # 如果存在，備份舊的目錄
    if [ -d "/root/da" ]; then
      mkdir -p "/root/da_backup"
      mv "/root/da" "/root/da_backup/da.\$(date +%Y%m%d%H%M%S)"
    fi

    mkdir -p /root/da

    # 解壓縮至指定目錄
    tar -xzf "/root/\$FILENAME" -C "/root/da"

    cp /home/ap/.env /root/da/.env

    # 切換到指定目錄
    cd "/root/da" || exit

    docker stop backend_v2
    docker compose -f docker-compose.v2.yml up --build -d


    check_service_response "http://localhost:8082"

    execute_in_nginx_container v2

    docker stop backend_v1
    docker compose -f docker-compose.v1.yml up --build -d

    check_service_response "http://localhost:8080"

    execute_in_nginx_container v1

    echo ">>> 清理 Docker 構建緩存"
    docker builder prune -a -f
    echo ">>> 清理完成！"

    # 執行 Redis 的 FLUSHDB 命令來清除數據
    if docker ps --filter "name=redis" --filter "status=running" | grep -q "redis"; then
      docker compose exec redis redis-cli -a pk_redis@6620 FLUSHDB
    fi
  '
EOF
