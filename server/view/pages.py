from abc import ABC, abstractmethod
from flask import flash, redirect, request, url_for
from werkzeug.local import LocalProxy


class Flash(ABC):
    """Represent abstraction of a flash."""

    @abstractmethod
    def display(self) -> str:
        pass


class UrlFor(ABC):
    """Represent abstraction of url redirection."""

    @abstractmethod
    def __call__(self) -> str:
        pass


class Redirect(ABC):
    """Represent abstraction of redirection."""

    @abstractmethod
    def link(self) -> str:
        pass


class Request(ABC):
    """Represent abstraction of request redirection."""

    @abstractmethod
    def get(self) -> str:
        pass


class PageFlash(Flash):
    """Represent a flash for a particular event ."""

    def __init__(self, message: str, event: str) -> None:
        self._message: str = message
        self._event: str = event

    def display(self) -> str:
        return flash(self._message, self._event)


class PageRedirect(Redirect):
    """Represent concrete redirection."""

    def __init__(self, endpoint: UrlFor) -> None:
        self._endpoint: UrlFor = endpoint

    def link(self) -> str:
        return redirect(self._endpoint())


class PageRequest(Request):
    """Represent next request page."""

    def __init__(self, page: str) -> None:
        self._page: str = page
        self._req: LocalProxy = request

    def get(self) -> str:
        return self._req.args.get(self._page)


class PageUrlFor(UrlFor):
    """Represent concrete url redirection."""

    def __init__(self, endpoint: str) -> None:
        self._endpoint: str = endpoint

    def __call__(self) -> str:
        return url_for(self._endpoint)
