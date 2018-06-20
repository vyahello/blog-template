from abc import ABC, abstractmethod
from typing import Callable, Any
from flask_sqlalchemy import SQLAlchemy
from server.storage.db import DB


class Session(ABC):
    """Represent abstraction database session."""

    @abstractmethod
    def synchronize(self) -> SQLAlchemy:
        pass

    @abstractmethod
    def add(self, user) -> None:
        pass


class UserSession(Session):
    """Represent concrete database session."""

    def __init__(self, db: DB) -> None:

        def _sync() -> None:
            sync: SQLAlchemy = db.synchronize()
            sync.create_all()

        self._db: DB = db
        self._sync: Callable[..., SQLAlchemy] = _sync

    def synchronize(self) -> SQLAlchemy:
        return self._db.synchronize()

    def add(self, data: Any) -> None:
        self._sync().session.add(data)
        self._sync().session.commit()
