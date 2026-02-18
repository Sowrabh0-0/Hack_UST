# This script takes a "snapshot" of the machine (installed packages, environment variables
# , and active users) and saves it to a file. Users can run it again later to see a "Diff"
#  of exactly what changed on the system.


# Key Libraries: subprocess, difflib.

import subprocess
import difflib
import json
from pathlib import Path
SNAPSHOT_FILE = Path("system_snapshot.json")

def take_snapshot():
    snapshot = {
        "installed_packages": subprocess.check_output(["pip", "freeze"]).decode(),
        "environment_variables": dict(subprocess.os.environ),
        "active_users": subprocess.check_output(["who"]).decode()
    }
    with open(SNAPSHOT_FILE, 'w') as f:
        json.dump(snapshot, f, indent=4)

def compare_snapshots():
    if not SNAPSHOT_FILE.exists():
        print("No snapshot found. Please take a snapshot first.")
        return

    with open(SNAPSHOT_FILE, 'r') as f:
        old_snapshot = json.load(f)

    new_snapshot = {
        "installed_packages": subprocess.check_output(["pip", "freeze"]).decode(),
        "environment_variables": dict(subprocess.os.environ),
        "active_users": subprocess.check_output(["who"]).decode()
    }

    for key in old_snapshot:
        print(f"Changes in {key}:")
        diff = difflib.unified_diff(
            old_snapshot[key].splitlines(),
            new_snapshot[key].splitlines(),
            fromfile='old_snapshot',
            tofile='new_snapshot',
            lineterm=''
        )
        print("\n".join(diff))
        print("\n")

if __name__ == "__main__":
    take_snapshot()
    print("Snapshot taken. Run the script again to see changes.")