from flask import Flask
from django.shortcuts import render

app = Flask(__name__)


@app.route('/')
def hello_world(request):
    return render(request,'')


if __name__ == '__main__':
    app.run()
