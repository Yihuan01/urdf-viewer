#!/usr/bin/env bash
# ============================================================
# URDF Viewer 一键启动脚本
# 用法:  ./start_viewer.sh [端口]
# 默认端口 8975。在本目录（index.html 所在处）起一个本地 HTTP 服务，
# 并尝试自动打开浏览器。
# ============================================================
set -e

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PORT="${1:-8975}"
URL="http://127.0.0.1:${PORT}/index.html"

echo "----------------------------------------"
echo " 服务目录 : $HERE"
echo " 访问地址 : $URL"
echo " 停止服务 : Ctrl+C"
echo "----------------------------------------"

# 后台尝试打开浏览器（有图形界面时）
(
  sleep 1.2
  for b in xdg-open google-chrome chromium chromium-browser firefox microsoft-edge open; do
    if command -v "$b" >/dev/null 2>&1; then
      "$b" "$URL" >/dev/null 2>&1 &
      break
    fi
  done
) &

cd "$HERE"
exec python3 serve.py "$PORT"
