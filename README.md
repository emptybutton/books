# books
Что бы начать, замените в названиях и содержаниях всех файлах:
1. `books` - на название вашего приложение в kebab-case
2. `books` - на название вашего приложение в snake_case
2. `Backend application for books` - на описание

Backend application for books.

## Развертывание для разработки
```bash
git clone https://github.com/emptybutton/books.git
docker compose -f books/deployments/dev/docker-compose.yaml up
```
