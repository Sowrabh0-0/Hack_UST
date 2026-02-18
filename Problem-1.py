# A script that monitors a specific directory for "delete" events. 
# When a file is deleted, it immediately copies the file from a 
# hidden "Shadow" directory to a "Recycle Bin" folder with a 
# metadata file showing who deleted it and when.


# Key Libraries: watchdog, shutil, getpass.

import time
import shutil
import getpass
from datetime import datetime, timezone
from pathlib import Path

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


#Demo Path
WATCH_DIR = Path(r"C:\Users\Admin\Downloads\Hack-probs\DemoFolder")


class DeleteRecoveryHandler(FileSystemEventHandler):
    def on_deleted(self, event):
        if event.is_directory:
            return 

        deleted_file = Path(event.src_path)
        shadow_file = WATCH_DIR / "Shadow" / deleted_file.name
        recycle_bin_file = WATCH_DIR / "Recycle Bin" / deleted_file.name
        metadata_file = WATCH_DIR / "Recycle Bin" / f"{deleted_file.stem}_metadata.txt"

        # Check if the deleted file exists in the Shadow directory
        if shadow_file.exists():
            # Copy the file to the Recycle Bin
            shutil.copy2(shadow_file, recycle_bin_file)

            # Create metadata
            metadata_content = (
                f"Deleted By: {getpass.getuser()}\n"
                f"Deleted At: {datetime.now(timezone.utc).isoformat()}\n"
                f"Original Path: {deleted_file}\n"
            )

            # Write metadata to a file
            with open(metadata_file, 'w') as meta_file:
                meta_file.write(metadata_content)

            print(f"Recovered '{deleted_file.name}' to Recycle Bin with metadata.")
        else:
            print(f"No shadow copy found for '{deleted_file.name}'. Cannot recover.")



if __name__ == "__main__":
    (WATCH_DIR / "Shadow").mkdir(exist_ok=True)
    (WATCH_DIR / "Recycle Bin").mkdir(exist_ok=True)

    event_handler = DeleteRecoveryHandler()
    observer = Observer()
    observer.schedule(event_handler, str(WATCH_DIR), recursive=False)
    observer.start()

    print(f"Monitoring '{WATCH_DIR}' for delete events...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()