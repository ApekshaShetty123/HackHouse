import os
from flask import Flask, render_template
app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY')
print(app.secret_key)
