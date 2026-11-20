from dataclasses import dataclass
from enum import Enum

from .errors import ValidationError


class SleepSchedule(str, Enum):
    EARLY = "early"
    LATE = "late"
    FLEXIBLE = "flexible"


@dataclass(frozen=True)
class Profile:
    """Анкета потенційного співмешканця."""

    id: str
    name: str
    city: str
    budget: int          # максимальна частка оренди на місяць, грн
    sleep: SleepSchedule
    smoker: bool
    has_pets: bool
    cleanliness: int     # 1 (толерантний до безладу) .. 5 (педант)

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValidationError("Ім'я не може бути порожнім")
        if not self.city.strip():
            raise ValidationError("Місто не може бути порожнім")
        if self.budget <= 0:
            raise ValidationError("Бюджет має бути додатнім")
        if not 1 <= self.cleanliness <= 5:
            raise ValidationError("Охайність має бути в діапазоні 1..5")


@dataclass(frozen=True)
class Match:
    """Результат підбору: кандидат і відсоток сумісності."""

    profile: Profile
    score: int
