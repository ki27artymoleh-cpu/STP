import uuid
from typing import List

from src.domain.entities import Match, Profile, SleepSchedule
from src.domain.errors import ProfileNotFoundError
from src.domain.repositories import ProfileRepository
from src.domain.scoring import compatibility_score


class RegisterProfileUseCase:
    def __init__(self, repository: ProfileRepository) -> None:
        self._repository = repository

    def execute(self, name: str, city: str, budget: int, sleep: str,
                smoker: bool, has_pets: bool, cleanliness: int) -> Profile:
        profile = Profile(
            id=uuid.uuid4().hex[:8],
            name=name,
            city=city,
            budget=budget,
            sleep=SleepSchedule(sleep),
            smoker=smoker,
            has_pets=has_pets,
            cleanliness=cleanliness,
        )
        self._repository.add(profile)
        return profile


class ListProfilesUseCase:
    def __init__(self, repository: ProfileRepository) -> None:
        self._repository = repository

    def execute(self) -> List[Profile]:
        return self._repository.list_all()


class FindMatchesUseCase:
    def __init__(self, repository: ProfileRepository) -> None:
        self._repository = repository

    def execute(self, profile_id: str, limit: int = 3,
                min_score: int = 50) -> List[Match]:
        me = self._repository.get(profile_id)
        if me is None:
            raise ProfileNotFoundError(f"Анкету {profile_id} не знайдено")

        matches = [
            Match(other, compatibility_score(me, other))
            for other in self._repository.list_all()
            if other.id != me.id
        ]
        matches = [m for m in matches if m.score >= min_score]
        matches.sort(key=lambda m: m.score, reverse=True)
        return matches[:limit]
