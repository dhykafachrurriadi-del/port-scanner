import socket
import threading
from datetime import datetime

# 1. Minta input dari pengguna
host = input("Masukkan host: ")

try:
    port_awal = int(input("Port awal: "))
    port_akhir = int(input("Port akhir: "))
except ValueError:
    print("Port harus berupa angka.")
    raise SystemExit

# 2. Ubah nama host menjadi alamat IP
try:
    ip = socket.gethostbyname(host)
except socket.gaierror:
    print("Host tidak ditemukan.")
    raise SystemExit

# Alat bantu: kunci supaya tulisan antar thread tidak bertabrakan
kunci = threading.Lock()
# Batasi maksimal 100 thread berjalan bersamaan
batas = threading.Semaphore(100)
file_log = open("scan_log.txt", "a")


def catat(port, status):
    """Cetak ke layar dan simpan ke file log."""
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    baris = f"{waktu} | {ip} | Port {port}: {status}"
    with kunci:
        print(baris)
        file_log.write(baris + "\n")


def cek_port(port):
    """Ketuk satu port lalu catat hasilnya."""
    with batas:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(3)
            s.connect((ip, port))
            catat(port, "OPEN")
            s.close()
        except ConnectionRefusedError:
            catat(port, "CLOSED")
        except socket.timeout:
            catat(port, "TIMEOUT")
        except OSError:
            catat(port, "ERROR")


# 3. Jalankan satu thread untuk tiap port
print(f"Scanning {ip} port {port_awal}-{port_akhir} ...")
mulai = datetime.now()
daftar_thread = []

try:
    for port in range(port_awal, port_akhir + 1):
        t = threading.Thread(target=cek_port, args=(port,))
        t.start()
        daftar_thread.append(t)

    for t in daftar_thread:
        t.join()
except KeyboardInterrupt:
    print("Dihentikan dengan Ctrl+C")

file_log.close()
print("Selesai dalam", datetime.now() - mulai)