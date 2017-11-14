from flask import Flask, abort, redirect, url_for, render_template, jsonify
app = Flask(__name__)


@app.route('/')
def dashboard():
    return render_template('dashboard.html', data=data)

@app.route('/update_crawler', methods=['POST'])
def update_crawler():
    keyword_mulcher = KeywordMulcher()
    keyword_mulcher.process(request.form['data'])
    return jsonify({'message': 'Crawler Updated'})

@app.route('/empty_crawler', methods=['POST'])
def empty_crawler():
    pass
    
@app.route('/stop_crawler', methods=['POST'])
def stop_crawler():
    pass