#!/bin/bash

PART="/"
LIMIT=90

while true
do
    USE=$(df "$PART" | awk '{print $5}' | tr -d '%')

    if [ "$USE" -ge "$LIMIT" ]; then
        echo "Disk almost full ($USE%)"

        FILES=$(du -ah "$PART" 2>/dev/null | sort -rh | head -5 | awk '{print $2}')

        zip /tmp/backup.zip $FILES

        echo "Files compressed to /tmp/backup.zip"
    fi

    sleep 60
done
