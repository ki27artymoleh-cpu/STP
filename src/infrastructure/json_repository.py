import json
from pathlib import Path
from typing import List, Optional

from src.domain.entities import Profile, SleepSchedule
from src.domain.repositories import ProfileRepository


class JsonProfileRepository(ProfileRepository):
    def __init__(self, path: str) -> None:
        self._path = Path(path)

    def add(self, profile: Profile) -> None:
        items = self.list_all()
        items.append(profile)
        self._path.parent.mkdir(parents=True, exist_ok=True)
        data = [self._to_dict(p) for p in items]
        self._path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    def get(self, profile_id: str) -> Optional[Profile]:
        return next((p for p in self.list_all() if p.id == profile_id), None)

    def list_all(self) -> List[Profile]:
        if not self._path.exists():
            return []
        raw = json.loads(self._path.read_text(encoding="utf-8"))
        return [self._from_dict(d) for d in raw]

    @staticmethod
    def _to_dict(p: Profile) -> dict:
        return {
            "id": p.id, "name": p.name, "city": p.city, "budget": p.budget,
            "sleep": p.sleep.value, "smoker": p.smoker,
            "has_pets": p.has_pets, "cleanliness": p.cleanliness,
        }

    @staticmethod
    def _from_dict(d: dict) -> Profile:
        return Profile(
            id=d["id"], name=d["name"], city=d["city"], budget=d["budget"],
            sleep=SleepSchedule(d["sleep"]), smoker=d["smoker"],
            has_pets=d["has_pets"], cleanliness=d["cleanliness"],
        )
