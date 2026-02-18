# A tool that maps every open network port on the machine to its specific Process ID (PID)
# and the user running it. It generates a summary of "Suspicious Ports" 
# (e.g., anything open that isn't on a pre-approved whitelist).


# Key Libraries: psutil, socket.


import psutil


WHITELIST_PORTS = [80, 443, 22, 53]   # HTTP, HTTPS, SSH, DNS
connections = psutil.net_connections(kind='inet')

for conn in connections:
    
    if conn.status == psutil.CONN_LISTEN:
        
        local_port = conn.laddr.port
        pid = conn.pid
        
        try:
            process = psutil.Process(pid)
            process_name = process.name()
            username = process.username()
        except:
            process_name = "Unknown"
            username = "Unknown"
        
        if local_port not in WHITELIST_PORTS:
            status = "Suspicious Port"
        else:
            status = "Allowed"
        
        print(f"Port: {local_port}")
        print(f"Process: {process_name}")
        print(f"PID: {pid}")
        print(f"User: {username}")
        print(f"Status: {status}")
        print()
