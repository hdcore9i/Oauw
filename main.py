mport socket
import json

# Konfigurasi pool penambangan
pool_host = '185.215.180.7'
pool_port = 5555

# Konfigurasi proxy
proxy_host = '0.0.0.0'
proxy_port = 3333

def handle_client(client_socket):
    # Membuka koneksi ke pool penambangan
    pool_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    pool_socket.connect((pool_host, pool_port))

    # Membaca data dari penambang dan mengirimkannya ke pool penambangan
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        pool_socket.sendall(data)

    # Membaca respons dari pool penambangan dan mengirimkannya ke penambang
    while True:
        data = pool_socket.recv(1024)
        if not data:
            break
        client_socket.sendall(data)

    # Menutup koneksi ke pool penambangan
    pool_socket.close()
    client_socket.close()

def start_proxy():
    # Membuat socket server untuk proxy
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((proxy_host, proxy_port))
    server_socket.listen(1)

    # Menjalankan server proxy
    print('Stratum proxy sedang berjalan di {}:{}'.format(proxy_host, proxy_port))
    while True:
        client_socket, address = server_socket.accept()
        print('Penambang terhubung dari {}:{}'.format(address[0], address[1]))
        handle_client(client_socket)

if __name__ == '__main__':
    start_proxy()

