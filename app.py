from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__) # instance of a flask app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db' # suing SQLite, can also use MySQL or PostGRE SQL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app) # creating the instance of db

class Todo(db.Model): # defining database schema
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    desc = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

@app.route("/", methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']

        todo = Todo(title=title, desc=desc)
        db.session.add(todo) # add to data base
        db.session.commit() # commit changes

    allTodo = Todo.query.all()

    return render_template('index.html', allTodo = allTodo) # use to render a html page using flask from templates folder
    # also passing the variable allTodod to the html page
    # return "Hello, World!"

@app.route("/delete/<int:sno>")
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

@app.route("/update/<int:sno>", methods=['GET', 'POST'])
def update(sno):
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first() # extract the todo we want to update
        todo.title = title
        todo.desc = desc
        db.session.add(todo) # add to data base
        db.session.commit() # commit changes
        return redirect("/")

    todo = Todo.query.filter_by(sno=sno).first() # extract the todo we want to update
    return render_template('update.html', todo = todo) # pass it to update.html and render it



@app.route("/show")
def show():
    allTodo = Todo.query.all()
    print(allTodo) # whenever we go to the show page all the data is printed on terminal``
    return "showing all the data in db"



# routes are used to make pages
@app.route("/products")
def products():
    return "This is Produts Page"

if __name__ == "__main__": # calling the app
    app.run(debug = True, port = 8000)