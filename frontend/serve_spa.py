#!/usr/bin/env python3
"""
HomeLab OS — High Performance SPA Static Server
Serves production frontend build (dist) with automatic SPA client-side fallback to index.html
Supports all routes (/login, /server-management, /devices, /analytics, /activity, etc.)
"""

import os
import sys
import socketserver
import http.server

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 5173
BASE_DIR = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "dist")

class SPAHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)

    def do_GET(self):
        # Strip query parameters and hashes for file check
        clean_path = self.path.split('?', 1)[0].split('#', 1)[0]
        local_target = self.translate_path(clean_path)

        # If static file or directory with index.html exists, serve directly
        if os.path.exists(local_target) and not (os.path.isdir(local_target) and not os.path.exists(os.path.join(local_target, "index.html"))):
            return super().do_GET()

        # Fallback to index.html for SPA client-side routing (e.g. /login, /server-management)
        self.path = "/index.html"
        return super().do_GET()

    def end_headers(self):
        # Enable CORS and disable aggressive caching for dev/preview
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        super().end_headers()

    def log_message(self, format, *args):
        # Suppress noisy logs unless error
        if args and str(args[1]) in ('200', '304'):
            return
        sys.stderr.write(f"[{self.log_date_time_string()}] {format % args}\n")

if __name__ == "__main__":
    socketserver.TCPServer.allow_reuse_address = True
    print(f"🚀 [HomeLab OS] Serving SPA from '{BASE_DIR}' on http://0.0.0.0:{PORT}...")
    with socketserver.TCPServer(("0.0.0.0", PORT), SPAHandler) as httpd:
        httpd.serve_forever()
