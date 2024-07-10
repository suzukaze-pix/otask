from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, time

app = Flask(__name__)

tasks = []

@app.route('/')
def index():
    current_time = datetime.now().time()
    return render_template('index.html', tasks=tasks, current_time=current_time)

@app.route('/add_task', methods=['POST'])
def add_task():
    title = request.form['title']
    importance = request.form['importance']
    details = request.form['details']
    deadline = request.form['deadline']
    audio = request.files['audio']

    if audio:
        audio.save(f'static/audio/{importance}_{len(tasks)}.mp3')
        audio_file = f'{importance}_{len(tasks)}.mp3'
    else:
        audio_file = None

    task = {
        'id': len(tasks),
        'title': title,
        'importance': importance,
        'details': details,
        'deadline': datetime.strptime(deadline, '%H:%M').time(),
        'completed': False,
        'audio': audio_file
    }
    tasks.append(task)
    return redirect(url_for('index'))

@app.route('/complete_task/<int:task_id>')
def complete_task(task_id):
    for task in tasks:
        if task['id'] == task_id:
            task['completed'] = True
            break
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)