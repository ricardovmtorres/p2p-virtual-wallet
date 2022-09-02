import socket
import threading
import wallet
import random

IP = socket.gethostbyname(socket.gethostname())
PORT = 5577
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"
# SALDO = wallet.Wallet(4200.00)
SN = []

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} se conectou.")

    connected = True
    while connected:
        # em algum momento recebe uma mensagem e é decodificada
        cod = conn.recv(SIZE).decode(FORMAT)
        if cod == DISCONNECT_MSG:
            connected = False
        print(f"[{addr}] {cod}")

        # chamada do serviço de busca de endereços
        ip, port = search_wallet(addr, cod)

        # e retorna um dado
        # no caso o endereço e porta da hash requerida
        cod = ip+":"+str(port)
        conn.send(cod.encode(FORMAT))

    conn.close()

def search_wallet(addr, cod):
    cod = f"cod received: {cod}"

    # a lista de carteiras conectadas é percorrida e dela extraida os dados desejados
    for name in SN:
        if name[0] == cod:
            addr = name[2]
            break
        elif name[1] == cod:
            addr = name[2]
            break

    return get_ip_port(addr)

def get_ip_port(addr):
    """Recebe um tupla transforma em lista e retorna a segunda posição.

    Quando o cliente se conecta o servidor pricipal ele recebe o IP e porta
    atraves da função accept do pacote socket.

    A variavel addr contem uma túpla.
    Essa tupla tem 2 dados, o primeiro é a string do ID, o segundo o int da porta.
    """
    lt = list(addr)
    return lt[0], lt[1]

def main():
    print("[STARTING] Server is starting...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING] Server is listening on {IP}:{PORT}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        hash = random.getrandbits(128)
        print("hash value: %032x" % hash)
        SN.append( [threading.activeCount() - 1, hash, addr] )
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

if __name__ == "__main__":
    main()