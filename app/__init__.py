import os
from flask import Flask, render_template, request
from dotenv import load_dotenv
import json
from peewee import *
import datetime
from playhouse.shortcuts import model_to_dict

load_dotenv()
app = Flask(__name__)

mydb = MySQLDatabase(os.getenv('MYSQL_DATABASE'), user=os.getenv('MYSQL_USER'), password=os.getenv('MYSQL_PASSWORD'), host=os.getenv('MYSQL_HOST'), port=3306)

class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)
    class Meta:
        database = mydb

mydb.connect()
mydb.create_tables([TimelinePost])

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/about')
def about():
    with open('./app/static/work_ex.json', 'r') as json_file:
        work_ex = json.load(json_file)
    
    with open('./app/static/hobbies.json', 'r') as json_file:
        hobbies = json.load(json_file)
        
    return render_template('about.html', work_ex=work_ex, hobbies=hobbies)

@app.route('/projects')
def projects():
    with open('./app/static/codingProjects.json', 'r') as json_file:
        codingProjects = json.load(json_file)
        
    return render_template('projects.html', codingProjects=codingProjects)

@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_posts():
    name = request.form['name']
    email = request.form['email']
    content = request.form['content']
    timeline_post = TimelinePost.create(name=name, email=email, content=content)
    
    return model_to_dict(timeline_post)

@app.route('/api/timeline_post', methods=['GET'])
def get_time_line_posts():
    return {
        'timeline_posts': [model_to_dict(p) for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())]
    }

if __name__ == '__main__':
    app.run(debug=True)
