import typing as t

from . import Plugin

import requests


class ExternalIP(Plugin):

    def __init__(self, server: str) -> None:
        self.server = server

    @property
    def name(self) -> str:
        return f'external IP with {self.server}'

    def run(self) -> t.Iterator[str]:
        try:
            yield requests.get(self.server).text
        except Exception:
            yield 'unable to reach server'
