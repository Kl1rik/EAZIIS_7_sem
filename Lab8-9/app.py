from flask_cors import cross_origin
from flask import Flask, render_template, request, flash
import logic

app = Flask(__name__)
app.secret_key = "manbearpig_MUDMAN888"

recognize_result_str = ""
speech_text = "no requests yet"


app.run(host='localhost', port=8777)

@app.route('/')
@app.route('/info')
@cross_origin()
def info():
    return render_template('info,html')


@app.route('/speech', methods=['POST', 'GET'])
@cross_origin()
def speech():
    if request.method == 'POST':
        global speech_text
        speech_text = request.form['text']
        voice = request.form['voice']
        print(voice, 'v')
        rate = request.form['rate']
        volume = request.form['volume']
        logic.text_to_speech(speech_text, voice, rate, volume)
    flash(str(speech_text))
    return render_template('speech.html')


@app.route('/recognize', methods=['POST', 'GET'])
@cross_origin()
def recognize():
    if request.method == 'POST':
        print(request.values)
        global recognize_result_str
        recognize_result_str = logic.recognize_speech(speech_text)

    flash(str(recognize_result_str))
    return render_template('recognize.html')


if __name__ == '__main__':
    app.run()
