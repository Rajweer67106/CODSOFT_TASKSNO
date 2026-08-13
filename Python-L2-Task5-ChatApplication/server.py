import socket
import threading

HOST = "0.0.0.0"
PORT = 5000
clients = {}
lock = threading.Lock()

def broadcast(message, sender=None):
    dead = []
    with lock:
        for client in clients:
            if client != sender:
                try:
                    client.send(message.encode("utf-8"))
                except OSError:
                    dead.append(client)
        for client in dead:
            clients.pop(client, None)

def handle_client(client, address):
    try:
        client.send("Enter your username: ".encode("utf-8"))
        username = client.recv(1024).decode("utf-8").strip()
        if not username:
            username = f"User-{address[1]}"
        with lock:
            clients[client] = username
        print(f"{username} connected from {address}.")
        broadcast(f"[SYSTEM] {username} joined the chat.", client)
        while True:
            data = client.recv(4096)
            if not data:
                break
            message = data.decode("utf-8").strip()
            if message.lower() == "/quit":
                break
            print(f"{username}: {message}")
            broadcast(f"{username}: {message}", client)
    except (ConnectionResetError, OSError):
        pass
    finally:
        with lock:
            username = clients.pop(client, locals().get("username", "Unknown"))

        try:
            client.close()
        except OSError:
            pass
        broadcast(f"[SYSTEM] {username} left the chat.")
        print(f"{username} disconnected.")

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()
    print(f"Chat server running on {HOST}:{PORT}")
    print("Press Ctrl+C to stop the server.")
    try:
        while True:
            client, address = server.accept()
            threading.Thread(
                target=handle_client,
                args=(client, address),
                daemon=True
            ).start()
    except KeyboardInterrupt:
        print("\nServer stopped.")
    finally:
        server.close()

if __name__ == "__main__":
    main()
