#!/usr/bin/env python3
"""Localhost-only development HTTP server. Standard library, no remote connections."""
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlsplit,unquote
import os
ROOT=Path(__file__).resolve().parents[1]
class Handler(SimpleHTTPRequestHandler):
    extensions_map={**SimpleHTTPRequestHandler.extensions_map,
        ".js":"text/javascript",".mjs":"text/javascript",
        ".glb":"model/gltf-binary",".json":"application/json",
        ".css":"text/css",".md":"text/markdown"}
    def translate_path(self,path):
        rel=unquote(urlsplit(path).path).lstrip("/")
        if not rel:rel="index.html"
        target=(ROOT/rel).resolve()
        if not target.is_relative_to(ROOT):return str(ROOT/"__blocked__")
        if any(p.startswith(".") for p in target.relative_to(ROOT).parts):
            return str(ROOT/"__blocked__")
        return str(target)
    def end_headers(self):
        self.send_header("Cache-Control","no-cache")
        self.send_header("X-Content-Type-Options","nosniff")
        self.send_header("Referrer-Policy","no-referrer")
        self.send_header("Cross-Origin-Resource-Policy","same-origin")
        self.send_header("Content-Security-Policy",
          "default-src 'self' blob: data:; script-src 'self'; style-src 'self' 'unsafe-inline'; connect-src 'self' blob:; img-src 'self' blob: data:; object-src 'none'; base-uri 'none'; frame-ancestors 'none'")
        super().end_headers()
    def do_POST(self):
        self.send_error(405,"Write operations are not exposed by the server")
if __name__=="__main__":
    port=int(os.environ.get("PORT","8765"))
    print("TRIALUM BUILDER READY http://127.0.0.1:%d/ (Ctrl+C to stop)"%port,flush=True)
    ThreadingHTTPServer(("127.0.0.1",port),Handler).serve_forever()
