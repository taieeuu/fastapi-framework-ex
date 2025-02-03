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
sshpass -p $sudo_pass ssh ap@$REMOTE_IP_ADDRESS <<EOF
  echo $sudo_pass | sudo -S bash -c '

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

    # 停止並重新啟動 Docker Compose 服務
    docker compose stop backend nginx redis
    docker compose up --remove-orphans --build -d
    
    echo ">>> 清理 Docker 構建緩存"
    docker builder prune -a -f
    echo ">>> 清理完成！"

    # 執行 Redis 的 FLUSHDB 命令來清除數據
    if docker ps --filter "name=redis" --filter "status=running" | grep -q "redis"; then
      docker compose exec redis redis-cli -a pk_redis@6620 FLUSHDB
    fi
  '
EOF
