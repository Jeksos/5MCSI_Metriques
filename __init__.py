from flask import Flask, render_template, jsonify, json
from datetime import datetime
from urllib.request import urlopen

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route('/tawarano/')
def meteo():
    try:
        response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
        raw_content = response.read()
        json_content = json.loads(raw_content.decode('utf-8'))
        results = []
        for item in json_content['list']:
            dt_value = item['dt']
            temp_day_value = item['main']['temp'] - 273.15  # Conversion de Kelvin en °C
            results.append({'Jour': dt_value, 'temp': temp_day_value})
        return jsonify(results=results)
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route("/histogramme/")
def histogramme():
    return render_template("histogramme.html")

@app.route("/contact/")
def contact():
    return render_template('contact.html')

@app.route('/commits')
def commits():
    try:
        response = urlopen('https://api.github.com/repos/Jeksos/5MCSI_Metriques/commits')
        raw_content = response.read()
        json_content = json.loads(raw_content.decode('utf-8'))
        results = []
        for item in json_content:
            commit_message = item['commit']['message']
            author = item['commit']['author']['name']
            date_commit = item['commit']['author']['date']
            results.append({'commit': commit_message, 'author': author, 'date_commit': date_commit})
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/commits/<date_string>')
def commits_by_date(date_string):
    try:
        date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
        response = urlopen('https://api.github.com/repos/Jeksos/5MCSI_Metriques/commits')
        raw_content = response.read()
        json_content = json.loads(raw_content.decode('utf-8'))
        filtered_commits = []
        for item in json_content:
            commit_date = datetime.strptime(item['commit']['author']['date'], '%Y-%m-%dT%H:%M:%SZ')
            if commit_date.minute == date_object.minute:
                commit_message = item['commit']['message']
                author = item['commit']['author']['name']
                date_commit = item['commit']['author']['date']
                filtered_commits.append({'commit': commit_message, 'author': author, 'date_commit': date_commit})
        return jsonify(results=filtered_commits)
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == "__main__":
    app.run(debug=True)
