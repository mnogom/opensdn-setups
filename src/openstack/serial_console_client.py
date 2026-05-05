# Source: https://docs.openstack.org/nova/14.0.4/_sources/testing/serial-console.txt

#!/usr/bin/env python3

import sys

from ws4py.client.threadedclient import WebSocketClient


class LazyClient(WebSocketClient):
    def run(self):
        try:
            while not self.terminated:
                try:
                    b = self.sock.recv(4096)
                    while len(b) > 0:
                        # websocket data: opcode + length + data
                        word = b[2 : b[1] + 2]
                        b = b[b[1] + 2 :]
                        sys.stdout.buffer.write(word)
                        sys.stdout.flush()
                except:  # socket error expected
                    pass
        finally:
            self.terminate()


def create_cli_session(url):
    if not url.startswith("ws"):
        raise Exception(
            "Usage: Please use websocket url, Example: ws://127.0.0.1:6083/?token=xxx"
        )
    try:
        ws = LazyClient(url, protocols=["binary"])
        ws.connect()
        while True:
            # keyboard event...
            c = sys.stdin.read(1)
            if c:
                ws.send(c.encode("utf-8"), binary=True)
        ws.run_forever()
    except KeyboardInterrupt:
        ws.close()


if __name__ == "__main__":
    if len(sys.argv) != 2 or not sys.argv[1].startswith("ws"):
        print("Usage %s: Please use websocket url")
        print("Example: ws://127.0.0.1:6083/?token=xxx")
        exit(1)
    create_cli_session(sys.argv[1])
