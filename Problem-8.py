# A small Python web server that stays idle until it receives 
# a specific "GET" request from another machine on the local network. 
# Upon receiving it, it executes a pre-defined local maintenance script (like clearing logs).


# Key Libraries: flask or http.server.


from http.server import BaseHTTPRequestHandler, HTTPServer
import subprocess

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/run-maintenance":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Running Maintenance Script...")

            # run the script here
            subprocess.run(["python", "maintenance_script.py"])
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Wrong route")

server = HTTPServer(("", 8080), MyHandler)
print("Server running at http://localhost:8080")
server.serve_forever()
