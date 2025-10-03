import typing as t
import time

from . import Plugin

import pywifi


class WiFi(Plugin):

    def __init__(self, scanning: int) -> None:
        self.wifi = pywifi.PyWiFi()
        self.iface = self.wifi.interfaces()[0]
        self.scanning = scanning

    @property
    def name(self) -> str:
        return f'scan APs with interface {self.iface.name()}'

    @staticmethod
    def _format(profile: pywifi.profile.Profile) -> str:
        if not profile.ssid or not profile.bssid:
            raise RuntimeError('could not get wifi info')
        info: t.List[str] = [profile.ssid, profile.bssid]
        if hasattr(profile, 'signal'):
            signal = int(getattr(profile, 'signal'))
            info.append(f'{signal}db')
        if hasattr(profile, 'freq'):
            freq = int(getattr(profile, 'freq'))
            info.append(f'{freq / 1e6}MHz')
        return ' '.join(info)

    def run(self) -> t.Iterator[str]:
        self.iface.scan()
        time.sleep(self.scanning)
        for ap in self.iface.scan_results():
            yield self._format(ap)
