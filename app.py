from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, time, timedelta


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f'<Task {self.id}>'

    @property
    def local_date(self):
        return self.date_created - timedelta(hours=3)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        content = request.form['content']
        todo = Todo(content=content)
        try:
            db.session.add(todo)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an error while trying to add your task.'
    elif request.method == 'GET':
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>')
def detele(id):
    task = Todo.query.get_or_404(id)
    try:
        db.session.delete(task)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an error while trying to delete your task.'


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        content = request.form['content']
        task.content = content
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an error while trying to update your task.'
    elif request.method == 'GET':
        return render_template('update.html', task=task)


if __name__ == '__main__':
    app.run(debug=True)
