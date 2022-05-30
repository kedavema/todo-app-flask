from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/database.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    completed = db.Column(db.Boolean)

    def __init__(self, title, completed):
        self.title = title
        self.completed = completed

    def __repr__(self):
        return f'<Todo: {self.title}>'


# Endpoint for todo list
@app.route('/')
def index():
    todos = Todo.query.all()
    return render_template('index.html', todos=todos)

  
# Endpoint for create todo
@app.route('/todo/create', methods=['POST'])
def create():
    title = request.form['title']
    todo = Todo(title, completed=False)
    db.session.add(todo)
    db.session.commit()
    return redirect(url_for('index'))
  
  
# Endpoint for update todo
@app.route('/todo/<int:todo_id>/update')
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.completed = not todo.completed
    db.session.commit()
    return redirect(url_for('index'))
  

# Endpoint for delete todo
@app.route('/todo/<int:todo_id>/delete')
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('index'))
  

# Run the app
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)