# A small Python web server that stays idle until it receives 
# a specific "GET" request from another machine on the local network. 
# Upon receiving it, it executes a pre-defined local maintenance script (like clearing logs).


# Key Libraries: flask or http.server.

from flask import Flask
import subprocess

app = Flask(__name__)

@app.route("/run-maintenance")
def run_maintenance():
    subprocess.run(["python", "maintenance_script.py"])
    return "Running Maintenance script..."

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def catch_all(path):
    return "Wrong route", 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
