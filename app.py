from flask import Flask, render_template, request
from test import *
from summary import *
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/execute_function', methods=['POST'])
def execute_function():
    function_name = request.form['function_name']
    text = request.form['text1']
    text=ct=str(text)
    function_name = request.form['function_name']
    if function_name == 'function1':
        text=hey(text)
        return render_template("about.html",x=text,y=ct)
    elif function_name == 'function2':
        text=hey(text)
        return render_template("about.html",x=text,y=ct)
    elif function_name == 'function3':
        text=sum(text)
        return render_template("about.html",x=text,y=ct)
    else:
        result = "Invalid function name"
    return result

# def function1(text):
#     text=hey(text)
#     return render_template("about.html",x=text)

# def function2(text):
#     text=hey(text)
#     return render_template("about.html",x=text)
# def function3(text):
#     text=hey(text)
#     return render_template("about.html",x=text)

if __name__ == '__main__':
    app.run()
