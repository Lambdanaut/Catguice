from flask import *

import config

app = Flask(__name__)
app.jinja_env.trim_blocks = True

def main():
  app.run(host=config.HOST,port=config.PORT,debug=config.DEVELOPMENT)

@app.route("/")
def index():
  return render_template("index.html")

@app.route("/about")
def about():
  return render_template("about.html")

@app.errorhandler(404)
def unauthorized(e):
  return render_template('404.html'), 404
