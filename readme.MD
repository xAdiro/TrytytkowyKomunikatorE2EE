# Projekt w django na zaliczenie fakultetu
#### Projekt można pobrać i samemu włączyć przy użyciu docker compose'a ale jest on też dostepny na <a href="http://adiro.online">http://adiro.online</a> (ale tylko do 3 lutego)

## Opis
Stworzyliśmy komunikator z szyfrowaniem end-to-end. Klucze są generowane przy każdym załadowaniu strony, więc po odświeżeniu napisane wiadomości przepadają (z naszej strony, odbiorca dalej ma do nich dostęp tak długo jak nie odświeży strony).
Niektóre części strony są ładowane asynchronicznie poprzez ciągłe zapytania, co jest rozwiązaniem nieoptymalnym ale najprostszym w zrealizowaniu.

Po zaakceptowaniu zaproszenia do znajomych trzeba odświeżyć stronę żeby nowa osoba pokazała się na liście, ale zaproszenia i czat wczytywane są samoczynnie.


## Pomocne komendy
1. Zainstaluj docker i docker-compose
2. Odpal `docker-compose build` będąc w folderze projektu
3. `docker-compose up` włącza projekt na porcie localhost:8000

### Migracje
1. `docker ps` wyświetla aktywne kontenery, skopiuj ID kontenera z django
2. `docker exec -it <ID_KONTENRA> python manage.py migrate` zmigruje baze

### Bezpośredni dostęp do bazy
1. `docker ps` wyświetla aktywne kontenery, skopiuj ID kontenera z bazą MySql
2. `docker exec -it <ID_KONTENERA> mysql -uroot -p` loguje na roota w bazie
