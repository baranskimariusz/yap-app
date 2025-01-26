from flask import Flask, render_template, redirect, url_for, flash, request, session, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_migrate import Migrate, upgrade
from flask.cli import with_appcontext
from models import db, User, Verb, Kanji, ExerciseResult
from forms import RegistrationForm, LoginForm, VerbExerciseForm, KanjiExerciseForm
from config import Config
import click
import json
import os
import random
import subprocess
import traceback
import time
from collections import defaultdict
from queue import Queue
from threading import Thread, Lock
import uuid

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

# Kolejka zadań i blokada dla wątków
job_queue = Queue()
jobs = {}
job_lock = Lock()

# Funkcja worker do przetwarzania zadań w tle
def worker():
    while True:
        job_id, user_input = job_queue.get()
        
        with job_lock:
            if job_id in jobs:
                jobs[job_id].update({
                    'status': 'processing',
                    'start_time': time.time()
                })
        
        try:
            bot_response = generate_bot_response(user_input)
            
            with job_lock:
                if job_id in jobs:
                    jobs[job_id].update({
                        'status': 'complete',
                        'result': bot_response,
                        'end_time': time.time()
                    })
                    
        except Exception as e:
            with job_lock:
                if job_id in jobs:
                    jobs[job_id].update({
                        'status': 'error',
                        'result': str(e),
                        'end_time': time.time()
                    })
        finally:
            job_queue.task_done()

# Uruchom wątek worker
worker_thread = Thread(target=worker, daemon=True)
worker_thread.start()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

reading_index = defaultdict(list)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.cli.command('reset-db')
@with_appcontext
def reset_db():
    db.drop_all()
    db.create_all()
    upgrade()
    initialize_database()
    click.echo('Baza danych została zresetowana.')

@app.cli.command("init-db")
def init_db():
    db.create_all()
    print("Baza danych zainicjalizowana.")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash('Taki użytkownik już istnieje.', 'danger')
            return redirect(url_for('register'))
            
        try:
            new_user = User(username=form.username.data)
            new_user.set_password(form.password.data)
            db.session.add(new_user)
            db.session.commit()
            
            login_user(new_user)
            flash('Rejestracja zakończona sukcesem. Zalogowano.', 'success')
            return redirect(url_for('dashboard'))
            
        except ValueError as e:
            db.session.rollback()
            flash(str(e), 'danger')
            return redirect(url_for('register'))
            
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            session.pop('verb_list', None)
            session.pop('kanji_list', None)
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Nieprawidłowy login lub hasło.')
    return render_template('login.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/chat', methods=['GET', 'POST'])
@login_required
def chat():
    if request.method == 'POST':
        user_input = request.form.get('user_input', '').strip()
        if not user_input:
            flash("Proszę wprowadzić pytanie")
            return redirect(url_for('chat'))
            
        job_id = str(uuid.uuid4())
        
        with job_lock:
            jobs[job_id] = {
                'status': 'pending',
                'user_input': user_input,
                'created_at': time.time(),
                'result': None
            }
            job_queue.put((job_id, user_input))
        
        print(f"Utworzono zadanie: {job_id}")
        return redirect(url_for('chat_result', job_id=job_id))
    
    return render_template('chat.html')

@app.route('/chat/result/<job_id>')
@login_required
def chat_result(job_id):
    print(f"Sprawdzam zadanie: {job_id}")
    
    with job_lock:
        job = jobs.get(job_id)
    
    if not job:
        print(f"Nie znaleziono zadania: {job_id}")
        flash("Nieprawidłowe lub przestarzałe żądanie")
        return redirect(url_for('chat'))
    
    print(f"Status zadania {job_id}: {job['status']}")
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({
            'status': job['status'],
            'result': job.get('result'),
            'user_input': job.get('user_input')
        })
    
    if job['status'] == 'complete':
        return render_template('chat_result.html',
            user_input=job['user_input'],
            bot_response=job['result']
        )
    elif job['status'] == 'error':
        flash(f"Błąd przetwarzania: {job['result']}")
        return redirect(url_for('chat'))
    
    return render_template('chat_wait.html', job_id=job_id)

@app.route('/exercise/verb', methods=['GET', 'POST'])
@login_required
def exercise_verb():
    form = VerbExerciseForm()
    if form.validate_on_submit():
        user_input = form.user_input.data.strip()
        verb_base = form.verb.data

        verb = Verb.query.filter_by(base_form=verb_base).first()

        correct_answer = verb.masu_form

        if user_input == correct_answer:
            flash('Poprawna odpowiedź!')
            score = 1
        else:
            flash(f'Niepoprawna odpowiedź. Poprawna odpowiedź to: {correct_answer}')
            score = 0

        result = ExerciseResult(
            user_id=current_user.id,
            exercise_type='verb_conjugation',
            score=score
        )
        db.session.add(result)
        db.session.commit()

        return redirect(url_for('exercise_verb'))
    else:
        if 'verb_list' not in session or not session['verb_list']:
            verbs = Verb.query.with_entities(Verb.id).all()
            verb_ids = [verb.id for verb in verbs]
            random.shuffle(verb_ids)
            session['verb_list'] = verb_ids

        while True:
            if not session['verb_list']:
                flash('Ćwiczenie ukończone! Gratulacje!')
                return redirect(url_for('dashboard'))

            verb_id = session['verb_list'].pop(0)
            session.modified = True

            verb = Verb.query.get(verb_id)
            if verb:
                break
            else:
                continue

        form.verb.data = verb.base_form

        eng_translation = verb.eng or ''
        pl_translation = verb.pl or ''

    return render_template('exercise_verb.html', form=form, eng=eng_translation, pl=pl_translation)

@app.route('/exercise/kanji', methods=['GET', 'POST'])
@login_required
def exercise_kanji():
    form = KanjiExerciseForm()
    if form.validate_on_submit():
        user_input = form.user_input.data.strip()
        kanji_char = form.kanji.data

        kanji = Kanji.query.filter_by(character=kanji_char).first()

        correct_readings = kanji.on_yomi.split(',') + kanji.kun_yomi.split(',')

        if user_input in correct_readings:
            flash('Poprawna odpowiedź!')
            score = 1
        else:
            flash(f'Niepoprawna odpowiedź. Poprawne odczyty to: {", ".join(correct_readings)}')
            score = 0

        result = ExerciseResult(
            user_id=current_user.id,
            exercise_type='kanji_reading',
            score=score
        )
        db.session.add(result)
        db.session.commit()

        return redirect(url_for('exercise_kanji'))
    else:
        if 'kanji_list' not in session or not session['kanji_list']:
            kanji_all = Kanji.query.with_entities(Kanji.id).all()
            kanji_ids = [k.id for k in kanji_all]
            random.shuffle(kanji_ids)
            session['kanji_list'] = kanji_ids

        while True:
            if not session['kanji_list']:
                flash('Ćwiczenie ukończone! Gratulacje!')
                return redirect(url_for('dashboard'))

            kanji_id = session['kanji_list'].pop(0)
            session.modified = True

            kanji = Kanji.query.get(kanji_id)
            if kanji:
                break
            else:
                continue

        form.kanji.data = kanji.character

    return render_template('exercise_kanji.html', form=form)

@app.route('/kanji/search', methods=['GET', 'POST'])
def kanji_search():
    kanji_list = []
    if request.method == 'POST':
        reading = request.form.get('reading').strip().lower()
        kanji_list = reading_index.get(reading, [])
    return render_template('kanji_search.html', kanji_list=kanji_list)

@app.route('/stats')
@login_required
def stats():
    results = ExerciseResult.query.filter_by(user_id=current_user.id).all()

    total_exercises = len(results)
    total_correct = sum(result.score for result in results)
    overall_percentage = (total_correct / total_exercises * 100) if total_exercises > 0 else 0

    stats_by_type = {}
    exercise_types = ['verb_conjugation', 'kanji_reading']

    for exercise_type in exercise_types:
        type_results = [result for result in results if result.exercise_type == exercise_type]
        total = len(type_results)
        correct = sum(result.score for result in type_results)
        percentage = (correct / total * 100) if total > 0 else 0
        stats_by_type[exercise_type] = {
            'total': total,
            'correct': correct,
            'percentage': percentage
        }

    return render_template('stats.html',
                           results=results,
                           total_exercises=total_exercises,
                           total_correct=total_correct,
                           overall_percentage=overall_percentage,
                           stats_by_type=stats_by_type)

def initialize_database():
    upgrade()

    Kanji.query.delete()
    db.session.commit()

    with app.open_resource('data/kanji_data.json', 'r') as f:
        kanji_data = json.load(f)
        for item in kanji_data:
            kanji = Kanji(
                character=item['character'],
                on_yomi=', '.join(item['readings']['on_yomi']),
                kun_yomi=', '.join(item['readings']['kun_yomi']),
                meanings=', '.join(item['meanings'])
            )
            db.session.add(kanji)
        db.session.commit()

    Verb.query.delete()
    db.session.commit()

    with app.open_resource('data/verb_data.json', 'r') as f:
        verb_data = json.load(f)
        for item in verb_data:
            verb = Verb(
                base_form=item['base_form'],
                masu_form=item['masu_form'],
                eng=item.get('eng', ''),
                pl=item.get('pl', '')
            )
            db.session.add(verb)
        db.session.commit()
    build_reading_index()

def build_reading_index():
    global reading_index
    reading_index = defaultdict(list)

    kanji_list = Kanji.query.all()
    for kanji in kanji_list:
        on_readings = kanji.on_yomi.split(',')
        for reading in on_readings:
            reading = reading.strip().lower()
            if reading:
                reading_index[reading].append(kanji)

        kun_readings = kanji.kun_yomi.split(',')
        for reading in kun_readings:
            reading = reading.strip().lower()
            if reading:
                reading_index[reading].append(kanji)

def extract_response(output, prompt):
    response = output.replace(prompt, '').strip()
    response = response.split('Student:')[0]
    return response

def generate_bot_response(prompt):
    llama_cpp_build_dir = '/app/llama.cpp/build/bin'
    model_path = '/app/llama.cpp/build/models/mistral-7b-v0.1.Q3_K_L.gguf'
    executable_name = 'llama-cli'

    pre_prompt = (
        "Jesteś pomocnym nauczycielem języka japońskiego. "
        "Odpowiadaj zawsze w języku polskim. "
        "Podaj odpowiedź w jasny i zorganizowany sposób, używając punktów lub numerowanej listy, jeśli to stosowne. "
        "Odpowiedz na poniższe pytanie, aby pomóc swojemu uczniowi.\n\n"
    )
    full_prompt = f"{pre_prompt}Student: {prompt}\nTutor:"

    cmd = [
        os.path.join(llama_cpp_build_dir, executable_name),
        '-m', model_path,
        '--prompt', full_prompt,
        '--temp', '0.7',
        '--n-predict', '256',
        '--top_k', '40',
        '--top_p', '0.9',
        '--repeat_penalty', '1.0',
        '--threads', '4',
        '--ctx_size', '2048',
    ]

    try:
        env = os.environ.copy()
        env['LD_LIBRARY_PATH'] = '/app/llama.cpp/build/src:/app/llama.cpp/build/ggml/src'

        result = subprocess.run(cmd, capture_output=True, text=True, env=env)
        if result.returncode != 0:
            print(f"Subprocess returned non-zero exit code {result.returncode}")
            print(f"Subprocess stderr: {result.stderr}")
            print(f"Subprocess stdout: {result.stdout}")
            return "Przepraszam, wystąpił błąd podczas generowania odpowiedzi."

        output = result.stdout

        response = extract_response(output, full_prompt)
        return response.strip()
    except Exception as e:
        print(f"Error generating bot response: {e}")
        traceback.print_exc()
        return "Przepraszam, wystąpił błąd podczas generowania odpowiedzi."

with app.app_context():
    initialize_database()

if __name__ == '__main__':
    app.run(host='0.0.0.0')