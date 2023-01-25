# Projekt w django na zaliczenie fakultetu

1. Zainstaluj docker i docker-compose
2. Odpal `docker-compose build` będąc w folderze projektu
3. `docker-compose up` włącza projekt na porcie localhost:8000

## Migracje
1. `docker ps` wyświetla aktywne kontenery, skopiuj ID kontenera z django
2. `docker exec -it <ID_KONTENRA> python manage.py migrate` zmigruje baze

## Bezpośredni dostęp do bazy
1. `docker ps` wyświetla aktywne kontenery, skopiuj ID kontenera z bazą MySql
2. `docker exec -it <ID_KONTENERA> mysql -uroot -p` loguje na roota w bazie
