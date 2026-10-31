#!/usr/bin/env python3
# ============================================================
# URDF Viewer 本地服务（仅标准库，不需要任何第三方包）
# 用法:  python3 serve.py [端口]
# 默认端口 8975。
#
# 为什么不直接用 python3 -m http.server：
#   http.server 遇到带 index.html 的目录不生成目录索引，
#   而本页自己就叫 index.html，所以左侧「模型文件」在根目录会是空的。
#   本脚本在普通静态服务之外多提供一个 JSON 列表接口：
#       <任意目录>/__ls/  →  {"entries":[{"name":..,"is_dir":..}, ...]}
#   index.html 优先走这个接口，失败时再退回解析 HTML 目录索引
#   （nginx autoindex 之类仍然可用）。
# ============================================================
import json
import os
import sys
import threading
import webbrowser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import unquote, urlsplit

MARK = '/__ls/'


class Handler(SimpleHTTPRequestHandler):

    def do_GET(self):
        path = urlsplit(self.path).path
        if MARK in path:
            return self.send_listing(path)
        return super().do_GET()

    def send_listing(self, path):
        base, sub = path.split(MARK, 1)
        target = self.translate_path(unquote(base + sub))
        if not os.path.isdir(target):
            self.send_error(404, 'not a directory')
            return
        entries = []
        try:
            for name in sorted(os.listdir(target)):
                if name.startswith('.'):
                    continue
                entries.append({'name': name,
                                'is_dir': os.path.isdir(os.path.join(target, name))})
        except OSError as exc:
            self.send_error(500, str(exc))
            return
        body = json.dumps({'entries': entries}).encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(body)

    def end_headers(self):
        # 与 index.html 里的 no-store 保持一致，改模型后刷新即可生效
        if self.path.lower().endswith(('.urdf', '.stl', '.dae', '.obj', '.glb', '.gltf')):
            self.send_header('Cache-Control', 'no-store')
        super().end_headers()

    def log_message(self, fmt, *args):
        sys.stderr.write('  %s\n' % (fmt % args))


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8975
    url = 'http://127.0.0.1:%d/index.html' % port
    print('-' * 42)
    print(' 服务目录 : %s' % os.getcwd())
    print(' 访问地址 : %s' % url)
    print(' 停止服务 : Ctrl+C')
    print('-' * 42)

    threading.Timer(1.2, lambda: webbrowser.open(url)).start()
    ThreadingHTTPServer(('127.0.0.1', port), Handler).serve_forever()


if __name__ == '__main__':
    main()
