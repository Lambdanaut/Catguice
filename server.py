from flask import *

import config
import pymongo
import models

app = Flask(__name__)
app.jinja_env.trim_blocks = True

# Database
db_con = pymongo.Connection(config.dbHost,config.dbPort)
db     = db_con.heroku_app2925802
db.authenticate(config.dbUsername, config.dbPassword)

products = models.Products(db)

def main():
  app.run(host=config.HOST,port=config.PORT,debug=config.DEVELOPMENT)

@app.route("/")
def index():
  hot_products = products.get(series = {"hot" : True})
  return render_template("index.html")

@app.route("/product/<int:product_id>")
def product(product_id):
  return render_template("product.html")

@app.route("/about")
def about():
  return render_template("about.html")

@app.errorhandler(404)
def unauthorized(e):
  return render_template('404.html'), 404
