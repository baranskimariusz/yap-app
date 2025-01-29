<p align="center">
  <a href="http://yapapp.pl"><img src="http://www.yapapp.pl/static/images/logo-2.png" alt="Logo" height=170></a>
</p>

<h1 align="center">YapApp</h1>

<p align="center"><a href="http://yapapp.pl/">yapapp.pl</a></p>

<div align="center">

</div>

[English](README.md) | [Polski](README-pl.md)

YapApp is a platform for learning Japanese, offering exercises, an AI chatbot, and a progress tracking system.

## Features

- **User registration and login**
- **Verb conjugation exercises**
- **Kanji recognition exercises**
- **Yomi-based indexing**
- **Learning progress statistics**
- **Tutor AI Chatbot**
- **Responsive user interface**
- **Secure data storage**
- **Containerization**
- **CRON jobs for scraping kanji using `kanjiapi.dev`**

## Installation

### Prerequisites

- Docker
- Docker Compose
- Python 3.9+

### Installation Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/baranskimariusz/Yap-App
   cd Yap-App
   ```
2. Build and run the containers:
   ```bash
   touch .env
   # Edytuj plik .env i ustaw odpowiednie wartości
   ```
3. Zbuduj i uruchom kontenery:
   ```bash
   docker compose up --build
   ```
4. Initialize the database:
   ```bash
   docker compose exec web flask reset-db
   ```
5. The application will be available at:
   HTTP: http://localhost:80

## Project structure

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


## Architecture

The application consists of the following components:

1. Frontend: HTML + CSS + JavaScript (Bootstrap)
2. Backend: Flask (Python)
3. Database: PostgreSQL with SQLAlchemy ORM 
4. AI Model: Mistral-7B 
5. Web Server: Nginx 
6. Containerization: Docker 
7. Hosting: DigitalOcean 

### Use of ORM (SQLAlchemy)

The application uses SQLAlchemy as an ORM to manage the PostgreSQL database. Data models are defined in the `models.py` file and include:<br>

`user`: User model with authentication data<br>
`verb`: Model for Japanese verbs<br>
`kanji`: Model for kanji characters with readings and meanings<br>
`exercise_results`: Model for storing users' exercise results

## Requirements and Implementation

**R1: User Registration**<br>
Status: Fulfilled<br>
Implementation: `/register` route in `app.py`

**R2: User Login**<br>
Status: Fulfilled<br>
Implementation: `/login` route using `Flask-Login`

**R3: User Database**<br>
Status: Fulfilled<br>
Technology: PostgreSQL + SQLAlchemy ORM

**R4: Verb Conjugation Exercises**<br>
Status: Fulfilled<br>
Implementation: `/exercise/verb` route

**R5: Kanji Recognition Exercises**<br>
Status: Fulfilled<br>
Implementation: `/exercise/kanji` route

**R6: Saving Statistics**<br>
Status: Fulfilled<br>
Implementation: `exercise_results` model in `models.py`

**R7: Conversational Bot**<br>
Status: Fulfilled<br>
Technology: Mistral-7B + `llama.cpp`

**R8: Custom Character Encoding System**<br>
Status: Fulfilled<br>
Implementation: In-memory indexing in `app.py`

**R9: Responsive Interface**<br>
Status: Fulfilled<br>
Technology: Bootstrap + custom CSS styles

**R10: Performance Optimization**<br>
Status: Fulfilled<br>
Solutions Used: Gunicorn, query optimizations

**R11: Data Security**<br>
Status: Fulfilled<br>
Features Included: Password hashing, data validation

**R12: Scalability**<br>
Status: Fulfilled<br>
Architecture Used: Docker Compose, load balancing, DigitalOcean Droplet

## Tests

### Test Scenarios

#### Full Test:<br>
https://github.com/user-attachments/assets/93391bbb-fb84-4d20-b7cd-bc0e4eeec524

#### Query Test:<br>
https://github.com/user-attachments/assets/1b091245-9c7e-4775-b2cb-5c87886bf2e1

### Report

#### Full Test:
- All buttons are functional.
- Login and registration work; input validation prevents extreme values.
- Exercises handle both correct and incorrect answers.
- Yomi-based indexing works with partial and full searches.
- The user panel is functional, enabling navigation throughout the site.
- History and statistics are correctly saved and calculated.

#### Query Test:
- Query queue works.
- Queries are processed and indexed.
- Responses are generated in the order queries are sent.

## License

The YapApp project is available under the **MIT License**. Details can be found in the `LICENSE` file.

## Authors

**Julia Kozłowska** @alealejulia <br>
**Mariusz Barański** @baranskimariusz 
