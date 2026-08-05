"""JSON-lines wire protocol helpers. One message per line, UTF-8 JSON."""
import json
import socket


def send_msg(sock: socket.socket, obj: dict) -> None:
    sock.sendall((json.dumps(obj, ensure_ascii=False) + "\n").encode("utf-8"))


def recv_msg(sock_file, timeout: float = 5.0):
    line = sock_file.readline()
    if not line:
        return None
    return json.loads(line.decode("utf-8"))


def call(host: str, port: int, obj: dict, timeout: float = 5.0):
    """One-shot request/response against a game4ai service."""
    with socket.create_connection((host, port), timeout=timeout) as s:
        send_msg(s, obj)
        f = s.makefile("rb")
        return recv_msg(f, timeout)
