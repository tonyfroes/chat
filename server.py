from config import *

class Server:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(ADDRESS)
        self.status = True

        print(f'[Server] Servidor rodando na porta {SERVER}')
        print(f'[Server] Aguardando conexoes')

    def msg_all_users(self, conn, name, message):
        for user in users:
            if user['connected'] != conn:
                user['connected'].send(f'{name}: {message}'.encode(FORMAT))
            else:
                user['connected'].send(f'{name} disse: {message}'.encode(FORMAT))

    def handle_client(self, name, conn):
        INDEX = 0
        CONNECT = True
        print(f'[Nova Conexao ] {name} connected')
        while CONNECT:
            messageLenght = conn.recv(HEADER).decode(FORMAT)
            if messageLenght:
                message = conn.recv(int(messageLenght)).decode(FORMAT)
                if message == DISCONNECT_MESSAGE:
                    CONNECT = False
                else:
                    print(f'{name} disse: {message}')
                    self.msg_all_users(conn, name, message)
        for user in users:
            if user['connected'] == conn:
                break
            INDEX += 1
        users.pop(INDEX)
        conn.close()

    def start(self):
        self.server.listen()
        while True:
            conn, addr = self.server.accept()
            messageLenght = conn.recv(HEADER).decode(FORMAT)
            if messageLenght:
                name = conn.recv(int(messageLenght)).decode(FORMAT)
            if name != DISCONNECT_MESSAGE:
                users.append({'name': name, 'connected': conn})
                print(f'{name} connected')
                thread = threading.Thread(target=self.handle_client, args=(name, conn))
                thread.start()
                print(f"[Threads Ativas] {threading.active_count() - 1}")


if __name__ == '__main__':
    server = Server()
    server.start()


        
    
