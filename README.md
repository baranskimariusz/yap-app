<p align="center">
  <a href="http://yapapp.pl"><img src="http://www.yapapp.pl/static/images/logo-2.png" alt="Logo" height=170></a>
</p>

<h1 align="center">YapApp</h1>

<p align="center"><a href="http://yapapp.pl/">yapapp.pl</a></p>

<div align="center">

</div>

YapApp to platforma do nauki języka japońskiego, oferująca ćwiczenia, chatbot AI oraz system śledzenia postępów.

## Funkcjonalności

- **Rejestracja i logowanie użytkowników**
- **Ćwiczenia odmiany czasowników**
- **Ćwiczenia rozpoznawania znaków kanji**
- **Yomi-based indexing**
- **Statystyki postępów w nauce**
- **Tutor-Chatbot AI**
- **Responsywny interfejs użytkownika**
- **Bezpieczne przechowywanie danych**
- **Konteneryzacja**
- **CRON jobs do scrapowania kanji z wykorzystaniem `kanjiapi.dev`**

## Instalacja

### Wymagania wstępne

- Docker
- Docker Compose
- Python 3.9+

### Kroki instalacyjne

1. Sklonuj repozytorium:
   ```bash
   git clone https://github.com/baranskimariusz/Yap-App
   cd Yap-App
   ```
2. Skonfiguruj zmienne środowiskowe:
   ```bash
   touch .env
   # Edytuj plik .env i ustaw odpowiednie wartości
   ```
3. Zbuduj i uruchom kontenery:
   ```bash
   docker compose up --build
   ```
4. Zainicjuj bazę danych:
   ```bash
   docker compose exec web flask reset-db
   ```
5. Aplikacja będzie dostępna pod adresem:
   HTTP: http://localhost:80

## Struktura projektu

```
└── 📁Yap-App
    └── 📁data
        └── kanji_data.json
        └── verb_data.json
    └── 📁static
        └── 📁css
            └── styles.css
        └── 📁images
            └── logo.png
        └── 📁js
            └── script.js
    └── 📁templates
        └── base.html
        └── chat_result.html
        └── chat_wait.html
        └── chat.html
        └── dashboard.html
        └── exercise_kanji.html
        └── exercise_verb.html
        └── index.html
        └── kanji_search.html
        └── login.html
        └── register.html
        └── stats.html
    └── .gitignore
    └── app.py
    └── config.py
    └── docker-compose.yml
    └── dockerfile
    └── entrypoint.sh
    └── forms.py
    └── gunicorn.conf.py
    └── manage.py
    └── models.py
    └── nginx.conf
    └── README.md
    └── requirements.txt
    └── scraper.py
    └── scraper-cron.sh
```

## Architektura

Aplikacja składa się z następujących komponentów:

1. Frontend: HTML + CSS + JavaScript (Bootstrap)
2. Backend: Flask (Python)
3. Baza danych: PostgreSQL z wykorzystaniem ORM SQLAlchemy
4. Model AI: Mistral-7B
5. Serwer WWW: Nginx
6. Konteneryzacja: Docker
7. Hosting: DigitalOcean

### Wykorzystanie ORM (SQLAlchemy)

Aplikacja wykorzystuje SQLAlchemy jako ORM do zarządzania bazą danych PostgreSQL. Modele danych są zdefiniowane w pliku `models.py` i obejmują:<br>

`user`: Model użytkownika z danymi uwierzytelniającymi<br>
`verb`: Model czasowników japońskich<br>
`kanji`: Model znaków kanji z odczytami i znaczeniami<br>
`exercise_results`: Model wyników ćwiczeń użytkowników

## Wymagania i ich realizacja

**W1: Rejestracja użytkownika**<br>
Status: Spełnione<br>
Implementacja: Ścieżka `/register` w `app.py`

**W2: Logowanie użytkownika**<br>
Status: Spełnione<br>
Implementacja: Ścieżka `/login` z użyciem `Flask-Login`

**W3: Baza danych użytkowników**<br>
Status: Spełnione<br>
Technologia: PostgreSQL + SQLAlchemy ORM

**W4: Ćwiczenie odmiany czasowników**<br>
Status: Spełnione<br>
Implementacja: Ścieżka `/exercise/verb`

**W5: Ćwiczenie rozpoznawania znaków**<br>
Status: Spełnione<br>
Implementacja: Ścieżka `/exercise/kanji`

**W6: Zapisywanie statystyk**<br>
Status: Spełnione<br>
Implementacja: Model `exercise_results` w `models.py`

**W7: Bot konwersacyjny**<br>
Status: Spełnione<br>
Technologia: Mistral-7B + `llama.cpp`

**W8: Własny system kodowania znaków**<br>
Status: Spełnione<br>
Implementacja: Indeksowanie w pamięci w `app.py`

**W9: Responsywny interfejs**<br>
Status: Spełnione<br>
Technologia: Bootstrap + własne style CSS

**W10: Wydajność**<br>
Status: Spełnione<br>
Rozwiązania: Gunicorn, optymalizacje zapytań

**W11: Bezpieczeństwo danych**<br>
Status: Spełnione<br>
Funkcje: Hashowanie haseł, walidacja danych

**W12: Skalowalność**<br>
Status: Spełnione<br>
Architektura: Docker Compose, load balancing, DigitalOcean Droplet

## Testy

### Scenariusze testowe

#### Pełny test:<br>
https://github.com/user-attachments/assets/93391bbb-fb84-4d20-b7cd-bc0e4eeec524

#### Test zapytań:<br>
https://github.com/user-attachments/assets/1b091245-9c7e-4775-b2cb-5c87886bf2e1

### Sprawozdanie

#### Pełny test:
- Wszystkie przyciski są funkcjonalne.
- Logowanie oraz rejestracja działa, walidacja wejścia zapobiega wartościom skrajnym.
- Ćwiczenia obsługują poprawne oraz niepoprawne odpowiedzi.
- Yomi-based indexing działa z częściowym oraz pełnym wyszukiwaniem.
- Panel użytkownika jest funkcjonalny oraz możliwa jest nawigacja po całej stronie.
- Historia oraz statystyki są poprawnie zapisywane oraz obliczane.

#### Test zapytań:
- Kolejka zapytań działa.
- Zapytania są przetwarzane oraz indeksowane.
- Odpowiedzi generowane są w kolejności wysłania zapytań.

## Licencja

Projekt YapApp jest dostępny na licencji **MIT**. Szczegóły znajdują się w pliku `LICENSE`.

## Autorzy

**Julia Kozłowska** @alealejulia <br>
**Mariusz Barański** @baranskimariusz
