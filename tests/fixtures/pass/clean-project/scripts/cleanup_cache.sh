#!/bin/bash
# 清理本机构建缓存（临时文件，不属于业务数据的销毁范围）
set -euo pipefail
rm -rf node_modules/.vite dist .cache
echo "cache purged"
