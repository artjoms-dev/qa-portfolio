import socket
import time
import os

LOG_FILE = "gpr_log.txt"

def log_message(message):
    with open(LOG_FILE, "a") as log:
        log.write(message + "\n")

def gpr_emulator():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", 9000))
    server.listen(1)
    print("[GPR] Device is running...")
    
    conn, addr = server.accept()
    print(f"[GPR] Connection from {addr}")
    
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            print(f"[GPR] Received: {data.decode()}")
            conn.sendall(b"OK")
    except:
        print("[GPR] Connection lost!")
    finally:
        conn.close()
        server.close()

def drone_software():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect(("127.0.0.1", 9000))
        log_message("[Drone] Connected to GPR")
        print("[Drone] Connected to GPR")

        for _ in range(3):
            client.sendall(b"Ping")
            time.sleep(1)

        client.close()
        log_message("[Drone] Connection lost - ERROR")
        print("[Drone] Connection lost - ERROR")

    except ConnectionRefusedError:
        log_message("[Drone] ERROR: Cannot connect to GPR")
        print("[Drone] ERROR: Cannot connect to GPR")

def check_logs():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as log:
            logs = log.read()
            if "[Drone] Connection lost - ERROR" in logs:
                print("[Test] Test Passed: Connection loss detected")
            else:
                print("[Test] Test Failed: No error found in logs")
    else:
        print("[Test] Test Failed: Log file not found")

if __name__ == "__main__":
    import threading
    gpr_thread = threading.Thread(target=gpr_emulator)
    gpr_thread.start()
    
    time.sleep(1)
    drone_software()
    
    time.sleep(2)
    check_logs()
