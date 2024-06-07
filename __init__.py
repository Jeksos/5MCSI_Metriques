fic S onia
Sony Sons
Ven 07/06/2024 12:33
from flask import Flask, render_template_string, render_template, jsonify from flask import render_template from flask import json from datetime import datetime from urllib.request import urlopen import sqlite3 app = Flask(_name_) @app.route('/') def hello_world():
Olivier Guerriau<oguerriau@gmail.com>
​
Vous​
from flask import Flask, render_template, jsonify
import json
from datetime import datetime
from urllib.request import urlopen

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route("/contact/")
def MaPremiereAPI():
    return render_template('contact.html')

@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') -
273.15 # Conversion de Kelvin en °C
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route("/histogramme/")
def histogramme():
    return render_template("histogramme.html")

@app.route('/commits')
def commit():
    response = urlopen('https://api.github.com/repos/Jeksos/5MCSI_Metriques/commits')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []

    for list_element in json_content:
        commit = list_element.get('commit').get('message')
        author = list_element.get('commit').get('author').get('name')
        date_commit = list_element.get('commit').get('author').get('date')
        results.append({'commit': commit, 'author': author,
'date_commit': date_commit})

    return jsonify(results=results)

@app.route('/commits/<date_string>')
def commit_date(date_string):
    date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
    minutes = date_object.minute
    response = urlopen('https://api.github.com/repos/Jeksos/5MCSI_Metriques/commits')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))

    filtered_commits = []
    for commit_info in json_content:
        commit_date =
datetime.strptime(commit_info.get('commit').get('author').get('date'),
'%Y-%m-%dT%H:%M:%SZ')
        if commit_date.minute == minutes:
            commit = commit_info.get('commit').get('message')
            author = commit_info.get('commit').get('author').get('name')
            date_commit = commit_info.get('commit').get('author').get('date')
            filtered_commits.append({'commit': commit, 'author':
author, 'date_commit': date_commit})

    return jsonify(results=filtered_commits)

if __name__ == "__main__":
    app.run(debug=True)
