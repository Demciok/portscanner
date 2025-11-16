import socket
import concurrent.futures
import time 
import math


def scan_port(ip,port):
    try:
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.settimeout(0.5)
        result = s.connect_ex((ip,port))
        s.close()
        return port if result == 0 else None
    except Exception as e:
        return None

def do_scan_TPE(threads,st,end,ip):
    open_ports = []
    start = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [executor.submit(scan_port, ip, port ) for port in range(st,end+1)]
    end = time.time()
    print(f"Długosc skanu: {(end-start):.3f} sekund")
    for fut in concurrent.futures.as_completed(futures):
        res = fut.result()
        if res:
            open_ports.append(res)
    return open_ports

def grab_banner(ip,port,timeout=1.0,bufsize=1024):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    try:
        s.connect((ip,port))
        banner = s.recv(bufsize)
        return banner.decode(errors='ignore')
    except Exception as e:
        return None
    finally:
        s.close()

def target():
    print("Podaj address ip lub nazwe hosta do skanu: 1- IP address 2 - nazwa hosta ")
    wejscie = int(input(""))
    if wejscie == 1:
        ip_add = input("Wpisz adres IP: ")
        return ip_add
    else:
        host_name = input("Podaj nazwe hosta: ")
        ip_add = socket.gethostbyname(host_name)
        return ip_add

if __name__ == "__main__":
    print("Witaj w skanerze portów")
    st_port_range = 1
    end_port_range = 1024 
    sim_threads = 64
    ip = target()
    open_ports = do_scan_TPE(sim_threads,st_port_range,end_port_range,ip)

    for open_port in open_ports:
        service = grab_banner(ip,open_port)
        print(f"Otwarty port adresu {ip} to: {open_port}, na tym porcie działa usługa {service} ")

    
