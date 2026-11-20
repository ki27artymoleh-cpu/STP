# Покрокова інструкція з Git (кроки 2–13 лабораторної)

Файли беріть з цього проєкту і додавайте до репозиторію поступово, як описано нижче.
Усі команди перевірені на тестовому репозиторії. Робіть скриншоти термінала/GitHub для звіту.

## Кроки 2–4. Репозиторій, клон, develop
1. На GitHub: New repository `roommate-finder`, галочки Add README + .gitignore (шаблон Python).
2. ```
   git clone <URL> && cd roommate-finder
   git config --global user.name "Ім'я Прізвище"
   git config --global user.email "you@example.com"
   git checkout -b develop
   ```
3. Створіть `config.json` і закомітьте в develop (потрібен для конфлікту):
   ```
   {
     "storage": "memory"
   }
   ```
   ```
   git add config.json && git commit -m "chore: add config.json" && git push -u origin develop
   ```

## Кроки 6–7. feature/domain-layer (3 коміти)
```
git checkout -b feature/domain-layer
# коміт 1: src/__init__.py, src/domain/__init__.py, errors.py, entities.py
git add src && git commit -m "feat(domain): add Profile and Match entities"
# коміт 2: src/domain/repositories.py
git add src && git commit -m "feat(domain): add ProfileRepository interface"
# коміт 3: src/domain/scoring.py, tests/__init__.py, tests/test_domain.py
git add . && git commit -m "feat(domain): add compatibility scoring rule and tests"
git push origin feature/domain-layer
```
На GitHub: New pull request, base `develop`, compare `feature/domain-layer`.
Опис PR: що додано (сутності, інтерфейс, правило сумісності) і що Domain не залежить від інших шарів.
Залишіть коментар у рев'ю (крок 12), виправте окремим комітом, потім Merge pull request.
Локально: `git checkout develop && git pull origin develop`.

## Крок 8. feature/application-layer
```
git checkout -b feature/application-layer
# src/application/__init__.py, use_cases.py
git add src && git commit -m "feat(application): add use cases"
git push origin feature/application-layer      # PR у develop, рев'ю, merge
git checkout develop && git pull origin develop
```

## Кроки 9–10. feature/infrastructure-layer і конфлікт
Гілка створюється від develop ДО того, як ви змінюєте config.json у develop.
```
git checkout -b feature/infrastructure-layer
# src/infrastructure/*.py, tests/test_use_cases.py, tests/test_infrastructure.py
git add . && git commit -m "feat(infrastructure): add in-memory and JSON repositories"
```
Змініть config.json у цій гілці:
```
{
  "storage": "json",
  "json_path": "data/profiles.json"
}
```
```
git add config.json && git commit -m "feat(infrastructure): switch storage to JSON file"
git push origin feature/infrastructure-layer
```
Тепер у develop змініть ТОЙ САМИЙ рядок:
```
git checkout develop
```
```
{
  "storage": "memory",
  "log_level": "INFO"
}
```
```
git add config.json && git commit -m "chore: add log_level to config"
git merge feature/infrastructure-layer
```
Git повідомить `CONFLICT (content): Merge conflict in config.json`. Файл матиме вигляд:
```
{
<<<<<<< HEAD
  "storage": "memory",
  "log_level": "INFO"
=======
  "storage": "json",
  "json_path": "data/profiles.json"
>>>>>>> feature/infrastructure-layer
}
```
Розв'язання: видаліть маркери й об'єднайте обидві зміни:
```
{
  "storage": "json",
  "json_path": "data/profiles.json",
  "log_level": "INFO"
}
```
```
git add config.json
git commit -m "merge: resolve storage config conflict"
git push origin develop
```
(Зробіть скриншоти: повідомлення про конфлікт, файл з маркерами, результат після розв'язання.)

## Крок 11. feature/presentation-layer
```
git checkout -b feature/presentation-layer
# src/presentation/__init__.py, cli.py, data/.gitkeep
git add . && git commit -m "feat(presentation): add CLI composition root"
git push origin feature/presentation-layer     # PR, рев'ю, merge у develop
```

## Крок 13. Реліз
```
git checkout develop && git pull origin develop
python -m unittest discover -s tests -t .      # перевірка
git checkout main && git pull origin main
git merge --no-ff develop -m "release: v1.0.0"
git tag v1.0.0
git push origin main --tags
```

## Крок 14. README
Додайте README.md з цього проєкту (діаграма Mermaid на GitHub відображається автоматично).
```
git checkout -b docs/readme develop
git add README.md && git commit -m "docs: add architecture diagram and run instructions"
```
Це можна зробити й до релізу: злийте в develop перед тегом v1.0.0.
