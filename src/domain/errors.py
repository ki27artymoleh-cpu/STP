class DomainError(Exception):
    """Базова помилка предметної області."""


class ValidationError(DomainError):
    """Порушено бізнес-правило під час створення сутності."""


class ProfileNotFoundError(DomainError):
    """Анкету з таким ідентифікатором не знайдено."""
