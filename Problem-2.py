import psutil


WHITELIST_PORTS = [80, 443, 22, 53]   # HTTP, HTTPS, SSH, DNS


print("=== Local Port & Process Traffic Cop ===\n")

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
        print("-" * 40)
