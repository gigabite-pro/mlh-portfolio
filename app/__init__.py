import os
from flask import Flask, render_template, request
from dotenv import load_dotenv
import json

load_dotenv()
app = Flask(__name__)

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


if __name__ == '__main__':
    app.run(debug=True)
