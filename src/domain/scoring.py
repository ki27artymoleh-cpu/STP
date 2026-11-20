from .entities import Profile, SleepSchedule


def compatibility_score(a: Profile, b: Profile) -> int:
    """Бізнес-правило: сумісність двох анкет у відсотках (0..100).

    Різні міста -> 0. Інакше сума балів:
    бюджет (30) + режим сну (25) + охайність (20) + куріння (15) + тварини (10).
    """
    if a.city.strip().lower() != b.city.strip().lower():
        return 0

    budget = 30 * (1 - abs(a.budget - b.budget) / max(a.budget, b.budget))

    if a.sleep == b.sleep:
        sleep = 25
    elif SleepSchedule.FLEXIBLE in (a.sleep, b.sleep):
        sleep = 15
    else:
        sleep = 0

    cleanliness = 20 * (1 - abs(a.cleanliness - b.cleanliness) / 4)
    smoking = 15 if a.smoker == b.smoker else 0
    pets = 10 if a.has_pets == b.has_pets else 0

    return round(budget + sleep + cleanliness + smoking + pets)

# Compatibility scoring business rules
