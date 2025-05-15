import socket

# Default parameters for the WIRE STORM challenge.
HOST: str = "127.0.0.1"
SEND_PORT: int = 33333
RECV_PORT: int = 44444


def create_sender(
    host: str = HOST, port: int = SEND_PORT, timeout_s: float = 5.0
) -> socket.socket:
    """Create a sender client to connect to the test server."""
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.settimeout(timeout_s)
    connection.connect((host, port))
    return connection


def create_receiver(host: str = HOST, port: int = RECV_PORT) -> socket.socket:
    """Create a receiver client to connect to the test server."""
    return create_sender(host, port)
