import typing as t
from abc import ABCMeta


class Plugin(metaclass=ABCMeta):

    @property
    def name(self) -> str:
        """Return name of plugin."""
        raise NotImplemented

    def run(self) -> t.Iterator[str]:
        """Run plugin."""
        raise NotImplemented
