"""JSON-lines wire helpers. One opaque JSON value per line."""
import json
import socket
from typing import Any


def send_msg(sock: socket.socket, obj: Any) -> None:
    sock.sendall((json.dumps(obj, ensure_ascii=False) + "\n").encode("utf-8"))


def recv_msg(sock_file, timeout: float = 5.0):
    line = sock_file.readline()
    if not line:
        return None
    return json.loads(line.decode("utf-8"))


def call(host: str, port: int, obj: Any, timeout: float = 5.0):
    """One-shot request/response against a game4ai service."""
    with socket.create_connection((host, port), timeout=timeout) as s:
        send_msg(s, obj)
        f = s.makefile("rb")
        return recv_msg(f, timeout)
