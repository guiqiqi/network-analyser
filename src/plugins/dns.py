import typing as t

from . import Plugin

import dns.resolver


class DNS(Plugin):

    def __init__(self, domains: t.List[str]) -> None:
        self.domains = domains
        self.resolver = dns.resolver.Resolver()

    @property
    def name(self) -> str:
        nameservers = [str(ns) for ns in self.resolver.nameservers]
        return f'resolve with ns: {", ".join(nameservers)}'

    def run(self) -> t.Iterator[str]:
        for domain in self.domains:
            try:
                answer = self.resolver.resolve(domain, 'A')
                addresses = [rdata.address for rdata in answer]
                yield f'{domain}: {", ".join(addresses)}'
            except dns.resolver.NoAnswer:
                yield f'{domain}: no answer'
