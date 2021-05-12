from flask import Flask,render_template,request, redirect,escape
import datetime
from flask_ckeditor import CKEditor
from flask_wtf import FlaskForm
from flask_ckeditor import CKEditorField
from wtforms import StringField, SubmitField
from flask_wtf.csrf import CSRFProtect
import os
import pprint
from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient()

db = client.blogdb
collection=db.post


app = Flask(__name__)

# db = client['blogdb']
# collection = db['posts']

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

ckeditor=CKEditor(app)
csrf = CSRFProtect(app)

class PostForm(FlaskForm):
    body = CKEditorField('Body') 

    

@app.route('/')
def home():
    blogs = list(collection.find())
    return render_template('index.html',posts=blogs)

@app.route('/search')
def search():
   pass

@app.route('/create', methods=['GET', 'POST'])
def create():
    form = PostForm()
    return render_template('create.html',form=form)

@app.route('/edit/<string:post_id>',methods=['GET', 'POST'])
def edit(post_id):
    form = PostForm()
    document = collection.find_one({'_id': ObjectId(post_id)})
    form.body.data = document['content']  # <--
    return render_template('edit.html', form=form,post=document)

@app.route('/update/<string:post_id>',methods=['GET', 'POST'])
def update(post_id):
    content=request.form.get('body')
    title = request.form.get('title')
    tags=request.form.get('tags').split(',')
    post = {
        "title": title,
        "content": content ,
        "tags": tags,
        "date": datetime.datetime.now()
    }
    collection.update_one({'_id': ObjectId(post_id)}, {"$set":post})

    return redirect(f'/view/{post_id}')



@app.route('/write',methods=['GET', 'POST'])
def write():
    content=request.form.get('body')
    title = request.form.get('title')
    tags=request.form.get('tags')
    # print(content)
    # print(title)
    tags=tags.split(',')
    print(type(tags))
    print(tags)
    
    post = {
        "author":"Gagan",
        "title": title,
        "content": content ,
        "tags": tags,
        "date": datetime.datetime.now()
    }
    # Post(title,content,tags).save()
    post_id = collection.insert_one(post).inserted_id
    print(post_id)

    return redirect(f'/view/{post_id}')

@app.route('/view/<string:post_id>', methods=['GET', 'POST'])
def view(post_id):
    print(post_id)
    document = collection.find_one({'_id': ObjectId(post_id)})
    print(document)
    # print(user["content"])
    return render_template('view.html',post=document)

@app.route('/delete/<string:post_id>', methods=['GET', 'POST'])
def delete(post_id):
    collection.delete_one({'_id': ObjectId(post_id)})
    return redirect('/')


if __name__=="__main__":
    app.run(debug=True)