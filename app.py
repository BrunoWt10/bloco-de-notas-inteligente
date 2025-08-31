import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# --- Configuração ---
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- Modelo do Banco de Dados ---
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Note {self.id}>'

# --- Rotas da Aplicação ---

@app.route('/')
def home():
    notes = Note.query.order_by(Note.date_created.desc()).all()
    return render_template('index.html', notes=notes)

@app.route('/add_note', methods=['GET', 'POST'])
def add_note():
    if request.method == 'POST':
        note_title = request.form['title']
        note_content = request.form['content']
        new_note = Note(title=note_title, content=note_content)
        db.session.add(new_note)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add_note.html')

@app.route('/edit_note/<int:note_id>', methods=['GET', 'POST'])
def edit_note(note_id):
    note = Note.query.get_or_404(note_id)
    if request.method == 'POST':
        note.title = request.form['title']
        note.content = request.form['content']
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add_note.html', note=note)

@app.route('/delete_note/<int:note_id>', methods=['POST'])
def delete_note(note_id):
    note_to_delete = Note.query.get_or_404(note_id)
    db.session.delete(note_to_delete)
    db.session.commit()
    return redirect(url_for('home'))

# --- Inicialização ---
if __name__ == '__main__':
    with app.app_context():
        db.create_all() # Cria as tabelas do banco de dados
    app.run(debug=True)