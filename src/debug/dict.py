from typing import Iterator, TypeVar, Union, Set, Dict, Mapping, Iterable
import collections.abc
import botconfig
from src.debug.history import History

__all__ = ["CheckedDict"]

KT = TypeVar("KT")
VT = TypeVar("VT")
KT_co = TypeVar("KT_co", covariant=True)
VT_co = TypeVar("VT_co", covariant=True)

class CheckedDict(collections.abc.MutableMapping):
    """ Dict container with additional features to aid in debugging.

    Common mutation methods are exposed to more easily set breakpoints,
    and a history of mutations can be enabled to track when and where the
    collection was modified in the past.
    """

    def __new__(cls, name: str, arg: Union[None, Mapping, Iterable] = None, **kwargs):
        if not botconfig.DEBUG_MODE:
            if arg is None:
                return dict(**kwargs)
            else:
                return dict(arg, **kwargs)

        return super().__new__(cls)

    def __init__(self, name: str, arg: Union[None, Mapping, Iterable] = None, **kwargs):
        self._history = History(name)
        if arg is None:
            self._dict = dict(**kwargs) # type: Dict[KT, VT]
        else:
            self._dict = dict(arg, **kwargs) # type: Dict[KT, VT]

    def clear(self) -> None:
        self._history.add("clear")
        self._dict.clear()

    def __setitem__(self, k: KT, v: VT) -> None:
        self._history.add("setitem", k, v)
        self._dict[k] = v

    def __delitem__(self, k: KT) -> None:
        self._history.add("delitem", k)
        del self._dict[k]

    def __getitem__(self, k: KT) -> VT_co:
        return self._dict[k]

    def __len__(self) -> int:
        return len(self._dict)

    def __format__(self, format_spec: str) -> str:
        return format(self._dict, format_spec)

    def __str__(self) -> str:
        return str(self._dict)

    def __repr__(self) -> str:
        return repr(self._dict)

    def __iter__(self) -> Iterator[KT_co]:
        return iter(self._dict)
