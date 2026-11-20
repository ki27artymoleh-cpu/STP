from abc import ABC, abstractmethod
from typing import List, Optional

from .entities import Profile


class ProfileRepository(ABC):
    """Порт (інтерфейс) сховища анкет.

    Оголошений у Domain; реалізації живуть в Infrastructure.
    """

    @abstractmethod
    def add(self, profile: Profile) -> None: ...

    @abstractmethod
    def get(self, profile_id: str) -> Optional[Profile]: ...

    @abstractmethod
    def list_all(self) -> List[Profile]: ...
