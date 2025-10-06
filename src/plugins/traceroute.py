import typing as t
import sys
import time
import socket
from subprocess import Popen, PIPE

from . import Plugin

from scapy.all import sr1
from scapy.layers.inet import IP, UDP
import chardet


class TraceRoute(Plugin):

    Repeat = 3

    def __init__(
        self,
        target: str,
        maxhops: int = 32,
        size: int = 40,
        timeout: int = 1
    ) -> None:
        self.target = target
        self.maxhops, self.size = maxhops, size
        self.timeout = timeout

    @property
    def name(self) -> str:
        return f'traceroute to {self.target}, {self.maxhops} hops max'

    @staticmethod
    def _format(hop: t.List[t.Tuple[str, int]]) -> str:
        line = []
        for ip, rtt in hop:
            line.append(f'{ip:^15}({rtt}ms)')
        return ';\t'.join(line)

    def run(self) -> t.Iterator[str]:
        if sys.platform == 'win32':
            return self._windows_run()
        else:
            return self._unix_run()

    def _unix_run(self) -> t.Iterator[str]:
        ttl = 1
        host = socket.gethostbyname(self.target)

        while ttl < self.maxhops:
            hop: t.List[t.Tuple[str, int]] = []
            reached: bool = False

            for _ in range(self.Repeat):
                packet = IP(dst=host, ttl=ttl) / UDP(dport=33433 + ttl)
                start = time.time()
                reply = sr1(packet, timeout=self.timeout, verbose=0)
                end = time.time()
                rtt = int((end - start) * 1000)
                if reply is None:
                    hop.append(('*', self.timeout * 1000))
                elif reply.type == 3:
                    hop.append((host, rtt))
                    reached = True
                else:
                    hop.append((reply.src, rtt))

                # Multiple check if reached
                if reply and reply.src == host:
                    reached = True

            yield f'{ttl:>2}: {self._format(hop)}'
            ttl += 1

            if reached:
                break

    def _windows_run(self) -> t.Iterator[str]:
        host = socket.gethostbyname(self.target)
        process = Popen(['tracert', host], stdout=PIPE)
        while True:
            if process.stdout:
                line = process.stdout.readline()
                if not line:
                    break
                encoding = chardet.detect(line)
                line = line.decode(encoding['encoding'], errors='ignore')
                yield line.strip()
            else:
                break
