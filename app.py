from flask import Flask, render_template, request
from test import *
from summary import *
from plagiarism import *

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/execute_function', methods=['POST'])
def execute_function():
    function_name = request.form['function_name']
    text = request.form['text1']
    file = request.files.get('filename')

    if file:  
        file_content = file.read().decode('utf-8')
        text = ct =str(file_content)
    else:
        text = ct =str(text)

    if function_name == 'function1':
        text=plag(text)
        text="plagiarism value = "+ str(text)
        return render_template("about.html",x=text,y=ct)
    elif function_name == 'function2':
        text=paraphrase_sentence(text)
        return render_template("about.html",x=text,y=ct)
    elif function_name == 'function3':
        text=sum(text)
        return render_template("about.html",x=text,y=ct)
    else:
        text=plag(text)
        text="plagiarism value = "+ str(text)
        return render_template("about.html",x=text,y=ct)

if __name__ == '__main__':
    app.run()
