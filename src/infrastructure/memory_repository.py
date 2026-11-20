from typing import Dict, List, Optional

from src.domain.entities import Profile
from src.domain.repositories import ProfileRepository


class InMemoryProfileRepository(ProfileRepository):
    def __init__(self) -> None:
        self._items: Dict[str, Profile] = {}

    def add(self, profile: Profile) -> None:
        self._items[profile.id] = profile

    def get(self, profile_id: str) -> Optional[Profile]:
        return self._items.get(profile_id)

    def list_all(self) -> List[Profile]:
        return list(self._items.values())
