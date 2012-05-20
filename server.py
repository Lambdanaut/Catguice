from flask import *

import config

app = Flask(__name__)
app.jinja_env.trim_blocks = True

def main():
  app.run(host=config.HOST, port=config.PORT, debug=config.DEVELOPMENT)

@app.route("/")
def hello():
    return render_template("index.html")
