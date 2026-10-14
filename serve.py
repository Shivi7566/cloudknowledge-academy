import http.server
import socketserver
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

PORT = 8080
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        # Support clean URLs like /roadmaps -> /roadmaps.html
        path_without_query = self.path.split('?')[0].rstrip('/')
        if path_without_query:
            clean_file = os.path.join(DIRECTORY, path_without_query.lstrip('/') + '.html')
            if os.path.isfile(clean_file):
                self.path = '/' + os.path.basename(clean_file)
        return super().do_GET()

def run():
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Cloud Knowledge Academy dev server live at: http://localhost:{PORT}")
        sys.stdout.flush()
        httpd.serve_forever()

if __name__ == "__main__":
    run()
