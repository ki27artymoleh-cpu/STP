import argparse
import json
import sys
from pathlib import Path

from src.application.use_cases import (
    FindMatchesUseCase, ListProfilesUseCase, RegisterProfileUseCase,
)
from src.domain.errors import DomainError
from src.domain.repositories import ProfileRepository
from src.infrastructure.json_repository import JsonProfileRepository
from src.infrastructure.memory_repository import InMemoryProfileRepository

CONFIG_PATH = Path(__file__).resolve().parents[2] / "config.json"


def build_repository(config: dict) -> ProfileRepository:
    """Composition root: тут (і лише тут) обирається конкретне сховище."""
    if config.get("storage") == "json":
        return JsonProfileRepository(config.get("json_path", "data/profiles.json"))
    return InMemoryProfileRepository()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="roommate-finder")
    sub = parser.add_subparsers(dest="command", required=True)

    reg = sub.add_parser("register", help="створити анкету")
    reg.add_argument("--name", required=True)
    reg.add_argument("--city", required=True)
    reg.add_argument("--budget", type=int, required=True)
    reg.add_argument("--sleep", choices=["early", "late", "flexible"], default="flexible")
    reg.add_argument("--smoker", action="store_true")
    reg.add_argument("--pets", action="store_true")
    reg.add_argument("--cleanliness", type=int, default=3)

    sub.add_parser("list", help="показати всі анкети")

    match = sub.add_parser("match", help="підібрати співмешканців")
    match.add_argument("--id", required=True)
    match.add_argument("--limit", type=int, default=3)
    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))

    repository = build_repository(config)
    register = RegisterProfileUseCase(repository)
    list_profiles = ListProfilesUseCase(repository)
    find_matches = FindMatchesUseCase(repository)

    try:
        if args.command == "register":
            p = register.execute(args.name, args.city, args.budget, args.sleep,
                                 args.smoker, args.pets, args.cleanliness)
            print(f"Анкету створено. ID: {p.id}")
        elif args.command == "list":
            for p in list_profiles.execute():
                print(f"{p.id}  {p.name}, {p.city}, до {p.budget} грн")
        elif args.command == "match":
            for m in find_matches.execute(args.id, limit=args.limit):
                print(f"{m.score:>3}%  {m.profile.name} ({m.profile.id})")
    except DomainError as err:
        print(f"Помилка: {err}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
