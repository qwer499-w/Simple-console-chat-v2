# chat_one_file.py
# Простой консольный чат: сервер + клиент в одном файле
# Запускается как сервер (сам подключается к себе) или как чистый клиент

import socket
import threading
import sys
import time

# ────────────────────────────────────────────────
# ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ
# ────────────────────────────────────────────────

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 9999
BUFFER_SIZE = 1024

# Только для сервера
clients = []
lock = threading.Lock()

# Для клиента (и сервера, когда он выступает клиентом)
my_socket = None
my_nickname = "You"


def server_broadcast(message: str, sender_sock=None):
    """Отправляет сообщение всем клиентам кроме отправителя"""
    if not clients:
        return

    data = f"{message}\n".encode("utf-8")
    dead = []

    with lock:
        for client in clients:
            if client is sender_sock:
                continue
            try:
                client.sendall(data)
            except Exception:
                dead.append(client)

    with lock:
        for sock in dead:
            try:
                clients.remove(sock)
                sock.close()
            except Exception:
                pass


def receive_messages():
    """Поток, который принимает сообщения от сервера и выводит их"""
    global my_socket

    while True:
        try:
            raw = my_socket.recv(BUFFER_SIZE)
            if not raw:
                print("\n[Соединение с сервером разорвано]")
                break

            msg = raw.decode("utf-8", errors="replace").rstrip("\r\n")
            if msg:
                # Перерисовываем строку ввода
                print(f"\r{msg:<80}\n{my_nickname}> ", end="", flush=True)

        except Exception as e:
            print(f"\n[Ошибка приёма сообщений: {e}]")
            break

    sys.exit(0)


def client_mode(host: str, port: int):
    global my_socket

    try:
        my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        my_socket.connect((host, port))
        print(f"[ПОДКЛЮЧЕНО] → {host}:{port}")
    except Exception as e:
        print(f"[ОШИБКА ПОДКЛЮЧЕНИЯ] {e}")
        return False

    # Запускаем приём сообщений в отдельном потоке
    threading.Thread(target=receive_messages, daemon=True).start()

    try:
        while True:
            try:
                text = input(f"{my_nickname}> ")
                text = text.rstrip()
                if text.lower() in {"/exit", "/quit", "exit", "quit"}:
                    break
                if text:
                    my_socket.send((text + "\n").encode("utf-8"))
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"[Ошибка отправки] {e}")
                break

    finally:
        try:
            my_socket.close()
        except:
            pass
        print("[ОТКЛЮЧЕНО ОТ СЕРВЕРА]")


def handle_incoming_client(client_sock: socket.socket, addr: tuple):
    ip_port = f"{addr[0]}:{addr[1]}"
    print(f"[ПОДКЛЮЧИЛСЯ] {ip_port}")

    with lock:
        clients.append(client_sock)

    try:
        while True:
            raw = client_sock.recv(BUFFER_SIZE)
            if not raw:
                break

            msg = raw.decode("utf-8", errors="replace").rstrip("\r\n")
            if msg:
                timestamp = time.strftime("%H:%M:%S")
                full_line = f"[{timestamp}] {ip_port}  {msg}"
                print(full_line)
                server_broadcast(full_line, client_sock)

    except Exception:
        pass
    finally:
        with lock:
            if client_sock in clients:
                clients.remove(client_sock)
        try:
            client_sock.close()
        except:
            pass
        print(f"[ОТКЛЮЧИЛСЯ] {ip_port}")


def server_mode(host: str, port: int):
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server_sock.bind((host, port))
        server_sock.listen(8)
        print(f"[СЕРВЕР ЗАПУЩЕН]  {host}:{port}")
        print("   Подключиться можно через: nc localhost 9999   или   telnet localhost 9999")
    except Exception as e:
        print(f"[ОШИБКА ЗАПУСКА СЕРВЕРА] {e}")
        return

    # Сервер сам подключается к себе как клиент
    print("[Сервер подключается к себе как клиент...]")
    client_mode(host, port)   # блокирует, пока пользователь не выйдет

    # После выхода клиента → останавливаем сервер
    print("[Остановка сервера...]")
    try:
        server_sock.close()
    except:
        pass


def main():
    global my_nickname

    print("=== Консольный чат (сервер + клиент в одном файле) ===")
    print("  s = запустить сервер (и подключиться к нему)")
    print("  c = подключиться к существующему серверу\n")

    mode = input("Выбор (s / c): ").strip().lower()

    nickname = input("Ваш ник в чате (Enter = You): ").strip()
    if nickname:
        my_nickname = nickname

    host_input = input(f"Хост [Enter = {DEFAULT_HOST}]: ").strip()
    host = host_input if host_input else DEFAULT_HOST

    port_input = input(f"Порт [Enter = {DEFAULT_PORT}]: ").strip()
    port = int(port_input) if port_input.isdigit() else DEFAULT_PORT

    if mode == "s":
        server_mode(host, port)
    elif mode == "c":
        client_mode(host, port)
    else:
        print("Неверный выбор. Завершение программы.")


if __name__ == "__main__":
    main()
