from flask import Flask, abort, redirect, url_for, render_template, jsonify
app = Flask(__name__)

keyword_mulcher = KeywordMulcher()

@app.route('/')
def dashboard():
    return render_template('dashboard.html', data=data)

@app.route('/update_crawler', methods=['POST'])
def update_crawler():
    keyword_mulcher.process(request.form['data'])
    return jsonify({'message': 'Crawler Updated'})

@app.route('/empty_crawler', methods=['POST'])
def empty_crawler():
    keyword_mulcher.empty_crawl_list()
    
@app.route('/stop_crawler', methods=['POST'])
def stop_crawler():
    keyword_mulcher.stop()

@app.route('/start_crawler', methods=['POST'])
def start_crawler():
    keyword_mulcher.start()