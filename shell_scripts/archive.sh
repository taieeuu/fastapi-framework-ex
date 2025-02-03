#!/bin/sh

ENV="$1"
TAG="$2"

# 檢查是否傳入標籤和IP地址參數
if [ -z "$TAG" ] || [ -z "$ENV" ]; then
  echo "請提供標籤名稱和環境參數"
  echo "用法: $0 <tag> <env>"
  exit 1
fi

if [ "$ENV" = "prod" ]; then
  IP_ADDRESS="172.22.1.150"
elif [ "$ENV" = "prod2" ]; then
  IP_ADDRESS="172.22.1.151"
elif [ "$ENV" = "uat" ]; then
  IP_ADDRESS="172.22.2.150"
else
  echo "環境參數只能是 prod 或 prod2 或 uat"
  echo $ENV , $TAG
  exit 1
fi

echo "標籤名稱: $TAG"
# 設定輸出文件名為當前路徑下的 dist/da.zip
OUTPUT_FILE="dist/$TAG/$IP_ADDRESS/da.tar.gz"
echo "輸出文件: $OUTPUT_FILE"
# 確保 dist 目錄存在
mkdir -p "dist/$TAG/$IP_ADDRESS"

git fetch --tags

# 使用 git archive 創建標籤的存檔文件
git archive --format tar --output temp.tar "$TAG"

# 檢查 git archive 命令是否成功
if [ $? -ne 0 ]; then
  echo "存檔文件創建失敗"
  rm temp.tar
  exit 1
fi

# 創建臨時目錄來解壓縮文件
TEMP_DIR=$(mktemp -d)
tar -xf temp.tar -C "$TEMP_DIR"

# 檢查解壓縮是否成功
if [ $? -ne 0 ]; then
  echo "解壓縮失敗"
  rm -rf "$TEMP_DIR" temp.tar
  exit 1
fi

# 刪除臨時的 tar 文件
rm temp.tar

# 修改文件名
# OLD_NAME="docker-compose.$IP_ADDRESS.yml"
# NEW_NAME="docker-compose.override.yml"
# OLD_FILENAME="$TEMP_DIR/$OLD_NAME"
# NEW_FILENAME="$TEMP_DIR/$NEW_NAME"


# 創建版本文件
VERSION_FILENAME="$TEMP_DIR/$TAG"
touch "$VERSION_FILENAME"

# if [ -f "$OLD_FILENAME" ]; then
#   cp "$OLD_FILENAME" "$NEW_FILENAME"
# else
#   echo "文件 $OLD_NAME 不存在，不產生 $NEW_NAME"
# fi


# 重新壓縮文件為 tar.gz 格式
tar --no-xattrs -czf "$OUTPUT_FILE" -C "$TEMP_DIR" .


# 清理臨時目錄
rm -rf "$TEMP_DIR"

echo "存檔文件創建並修改成功: $OUTPUT_FILE"

# 如果有 deploy 參數，則執行 deploy.sh
if [ "$3" = "deploy" ]; then
  echo "執行 deploy.sh"
  bash ./shell_scripts/deploy_v2.sh "$OUTPUT_FILE" "$IP_ADDRESS"
  exit 0
fi
