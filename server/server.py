import os
from flask import Flask, render_template, request

from Dados import Dados

app = Flask(__name__)

dados = Dados()

@app.route('/')
def hello():
    usuario = request.args.get('usuario')
    print(usuario)
    return render_template('indexPrincipal.html')


app.run()
