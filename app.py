from flask import Flask, render_template, request, redirect, jsonify
from google.cloud import storage
import sqlite3
import random

app = Flask(__name__)
DB_NAME = 'blog.db'
BUCKET_NAME = 'final-gcp-ws'
def upload_file(source_file,destination_file):
    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(destination_file)
    blob.upload_from_file(source_file,content_type=source_file.content_type)
    return blob.public_url
def generate_name_tag(name):
    number = random.randint(100000,999999)
    return f"{name}_{number}"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS blogs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            image_url TEXT NOT NULL,
            content TEXT NOT NULL,
            author TEXT NOT NULL
        )
        ''')
    conn.commit()  # Replace with your GCS bucket name
    conn.close()

@app.route('/')
def get_blogs():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT id, title, image_url, content, author FROM blogs')
    blogs = cursor.fetchall()
    conn.close()
    return render_template('blogs.html', blogs=blogs),200

@app.route('/blogs',methods=['GET','POST'])
def create_blogs():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        author = request.form.get('author')
        image = request.files.get('image')

        if not title or not content or not author or not image:
            return jsonify({'error': 'Please fill all the fields!'}), 400
        image_url = upload_file(image,generate_name_tag(author))

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO blogs (title, image_url, content, author) VALUES (?, ?, ?, ?)',
                       (title, image_url, content, author))
        conn.commit()
        conn.close()
        return  redirect('/')
    return render_template('create_blogs.html'),200

if __name__ == '__main__':

    init_db()
    app.run(debug=True) 
