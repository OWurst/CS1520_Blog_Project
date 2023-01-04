from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(1000), nullable=False)
    author = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route("/", methods=['POST', 'GET'])
def index():
    #db.drop_all()
    db.create_all()
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = BlogPost(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'
    else:
        tasks = BlogPost.query.order_by(BlogPost.title).all()
        return render_template("home.html", blogposts = tasks)

    # return render_template("index.html")

@app.route('/new-blog', methods = ['POST', 'GET'])
def new_blog():
    if request.method == 'POST':
        task_title = request.form['title']
        task_content = request.form['content']
        task_author = request.form['author']
        new_task = BlogPost(title = task_title, content=task_content, author = task_author)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'
    else:
        return render_template('new-blog.html')

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = BlogPost.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect("/")
    except:
        return 'There was a problem deleting that task'

@app.route('/blog/<int:id>', methods = ['POST', 'GET'])
def update(id):
    post = BlogPost.query.get_or_404(id)
    if request.method == 'POST':
        redir = '/delete/' + str(id)
        try:
            return redirect(redir)
        except:
            return 'There was an issue deleting your task'
    else:
        return render_template('blog.html', post=post)

if __name__ == "__main__":
    app.run(debug=True)
