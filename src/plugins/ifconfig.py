import typing as t
import socket

from . import Plugin

import psutil


class IFConfig(Plugin):

    def __init__(self) -> None:
        self.ifs = psutil.net_if_addrs()

    @property
    def name(self) -> str:
        return 'ifconfig information'

    @staticmethod
    def _format(ifname: str, addrs: t.List[psutil._common.snicaddr]) -> str:
        lines = [ifname]
        for addr in addrs:
            fam = addr.family
            if fam == socket.AF_INET:
                lines.append(f'  IPv4: {addr.address}')
                lines.append(f'  netmask: {addr.netmask}')
                lines.append(f'  boardcast: {addr.broadcast}')
            elif fam == socket.AF_INET6:
                lines.append(f'  IPv6: {addr.address}')
                lines.append(f'  netmask: {addr.netmask}')
                lines.append(f'  boardcast: {addr.broadcast}')
            elif fam == psutil.AF_LINK:
                lines.append(f'  MAC: {addr.address}')
        return '\n'.join(lines)

    def run(self) -> t.Iterator[str]:
        for ifname, addrs in psutil.net_if_addrs().items():
            yield self._format(ifname, addrs)
