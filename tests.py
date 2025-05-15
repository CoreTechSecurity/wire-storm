import socket
import time
import unittest
from threading import Thread

import buffers
from client import create_receiver, create_sender

# Header metadata
MAGIC_BYTE: int = 0xCC
HEADER_SIZE: int = 8


class TestSolution(unittest.TestCase):
    """
    Unit testing class for the WIRE STORM solution.

    Sets up a single sender and N receivers for each test case.

    The senders/receivers are torn down between each test so they can be run in isolation.
    """

    # Map of Thread ID -> Data Received
    data_received: dict[int:bytes] = {}
    # Timeout for each receiver before assuming the connection is broken.
    receiver_timeout_s: int = 5
    # Wait time between each test to allow sockets to tear down.
    sleep_before_data_send_s: float = 0.5
    # Receiver buffer size (per thread).
    buffer_size: int = 1024

    def receive_msg(self, thread_id: int) -> None:
        """Receive a single CTMP message.

        Args:
            thread_id (int): The thread identifier to store the received bytes.

        Raises:
            RuntimeError: If the connection breaks or times out.
        """
        receiver: socket.socket = create_receiver()

        try:
            data = receiver.recv(HEADER_SIZE)
            data_length = int.from_bytes(bytearray(data)[2:4], byteorder="big")
            print(f"Receiver ({thread_id}) - processing ({data_length}) bytes.")

            data_received = [data]
            bytes_received = 0

            while bytes_received < data_length:
                data = receiver.recv(
                    min(data_length - bytes_received, self.buffer_size)
                )
                if not data:
                    raise RuntimeError("Broken connection.")

                data_received.append(data)
                bytes_received += len(data)

            self.data_received[thread_id] = b"".join(data_received)

        except Exception as e:
            print("Receiver thread - caught exception:", str(e))

        finally:
            receiver.close()

    def setUp(self):
        """Set up the sender client."""
        self.data_received.clear()  # Nullify before each test.
        self.sender: socket.socket = create_sender()

    def tearDown(self):
        """Tear down and wait for the sender client to terminate."""
        self.sender.close()
        time.sleep(self.sleep_before_data_send_s)

    def _test_case(
        self, data: bytes, thread_count: int = 1, expect_timeout: bool = False
    ):
        """Generic test case for constructing the receiver threads and validating the result.

        Args:
            data (bytes): Data to be transmitted - including the CTMP header.
            thread_count (int, optional): Number of threads to spawn. Defaults to 1.
            expect_timeout (bool, optional): Whether a timeout is expected to occur (ie no data received). Defaults to False.
        """
        receiver_threads: list[Thread] = []

        for thread_id in range(thread_count):
            receiver_threads.append(Thread(target=self.receive_msg, args=(thread_id,)))
            receiver_threads[-1].start()

        time.sleep(self.sleep_before_data_send_s)
        self.sender.sendall(data)

        for thread in receiver_threads:
            thread.join(timeout=self.receiver_timeout_s)

        for thread_id in range(thread_count):
            if not expect_timeout:
                self.assertIsNotNone(self.data_received[thread_id])
                self.assertEqual(self.data_received[thread_id], data)
            else:
                self.assertIsNone(self.data_received.get(thread_id))

    ## TEST CASES ############################################################

    def test_small_packet(self):
        self._test_case(data=buffers.getb(buffers.t_small))

    def test_large_packet(self):
        self._test_case(data=buffers.getb(buffers.t_large))

    def test_invalid_magic(self):
        self._test_case(
            data=buffers.getb(buffers.t_invalid_header), expect_timeout=True
        )

    def test_additional_receiver(self):
        self._test_case(data=buffers.getb(buffers.t_basic), thread_count=2)

    def test_multiple_receivers(self):
        self._test_case(data=buffers.getb(buffers.t_basic), thread_count=20)

    ##########################################################################


if __name__ == "__main__":
    print(buffers.gets(buffers.s1))
    res = unittest.main(exit=False)
    if not res.result.failures and not res.result.errors and res.result.testsRun >= 4:
        print(buffers.gets(buffers.s2))
