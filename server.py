from flask import *

import os

import config
import forms
import models
import pymongo
import util

try:
  import secrets
  secrets_found = True
except:
  print("The admin control panel located at " + url_for("admincp") + " is disabled because you don't have a proper admin_password set in your secrets.py file. " )
  secrets_found = False

app = Flask(__name__)
app.jinja_env.trim_blocks = True

# Secret Key
if config.DEVELOPMENT: app.secret_key = "0"
else                 : app.secret_key = os.urandom(24)

# Database
db_con = pymongo.Connection(config.dbHost,config.dbPort)
db     = db_con.heroku_app2925802
db.authenticate(config.dbUsername, config.dbPassword)

products_model = models.Products(db)
products_model.insert({"name":"A product that is the best! "})

def main():
  app.run(host=config.HOST,port=config.PORT,debug=config.DEVELOPMENT)

@app.before_request
def before_request():
  # Check the sessions
  if "admin_password" in session and secrets_found: 
    if session["admin_password"] == secrets.admin_password:
      g.admin = True 
    else: g.admin = False
  else: g.admin = False

@app.context_processor
def inject_template():
  return dict(admin = g.admin, util = util, config = config)

@app.route("/")
def index():
  hot_products = products_model.get(series = {"hot" : True})
  return render_template("index.html")

@app.route("/product/<product_slug>")
def product(product_slug):
  product = products_model.get_one({"slug" : product_slug.lower()})
  if not product: abort(404)
  return render_template("product.html", product=product)

@app.route("/about")
def about():
  return render_template("about.html")

@app.route("/admincp", methods=['GET','POST'])
def admincp():
  if not secrets_found: abort(404)
  if request.method == 'POST':
    if not 'admin_password' in request.form: abort(404)
    if request.form['admin_password'] == secrets.admin_password:
      session['admin_password']=secrets.admin_password
      session.permanent = True
      return render_template("admincp.html", admin=True)
    return render_template("admincp.html", admin=False)
  elif request.method == 'GET':
    return render_template("admincp.html")

@app.route("/admincp/add_product")
def add_product():
  pass

@app.errorhandler(404)
def unauthorized(e):
  return render_template('404.html'), 404
