# A small Python web server that stays idle until it receives 
# a specific "GET" request from another machine on the local network. 
# Upon receiving it, it executes a pre-defined local maintenance script (like clearing logs).


# Key Libraries: flask or http.server.


import http.server
from logging import Handler

class MaintenanceHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/run-maintenance":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Running maintenance script...")
            # Here you would add the code to execute your maintenance script
            # For example: subprocess.run(["python", "maintenance_script.py"])
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")

if __name__ == "__main__":
    server_address = ('', 8080) 
    httpd = http.server.HTTPServer(server_address, MaintenanceHandler)
    print("Server is running on port 8080...")
    httpd.serve_forever()