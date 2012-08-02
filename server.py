from flask import *
import pymongo

import os

import config
import models
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
categories_model = models.Categories(db)

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
  featured_products = products_model.get(series = {"featured" : True})
  categories = categories_model.get()
  return render_template("index.html", categories=categories)

@app.route("/product/<product_slug>")
def product(product_slug):
  product = products_model.get_one({"slug" : product_slug.lower()})
  if not product: abort(404)
  return render_template("product.html", product=product)

@app.route("/categories/<category_slug>")
def category(category_slug):
  category = categories_model.get_one({"slug" : category_slug.lower()})
  if not category: abort(404)
  products = products_model.get({"category" : category['name'] })
  return render_template("category.html", category=category, products=products)

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
    categories = categories_model.get()
    return render_template("admincp.html", categories=categories)
 
@app.route("/admincp/add_product", methods=['POST'])
def add_product():
  if g.admin:
    if request.method == 'POST':
      # Make sure all the required fields were found. 
      product_fields = ['product_name', 'product_description', 'product_images', 'product_primary_colors', 'product_secondary_color_name', 'product_secondary_colors', 'product_category']
      if not all(map(lambda p: p in request.form, product_fields) ):
        return "There was an error processing your request. Not all of the required fields were found to be submitted. "
      if not request.form['product_name']: return "The product name is required"
      if not request.form['product_category']: return "The category is required"
      if request.form['product_description']: description = request.form['product_description']
      else:                                   description = None
      product_data = {
        'name'                 : request.form['product_name']
      , 'description'          : description
      , 'images'               : util.split_product_list(request.form['product_images'])
      , 'primary_colors'       : util.split_product_list(request.form['product_primary_colors'])
      , 'secondary_color_name' : request.form['product_secondary_color_name']
      , 'secondary_colors'     : util.split_product_list(request.form['product_secondary_colors'])
      , 'category'             : request.form['product_category']
      }
      products_model.insert(product_data)
      flash("Product Added Successfully")
      return redirect(url_for('admincp'))

@app.route("/admincp/add_category", methods=['POST'])
def add_category():
  if g.admin:
    if request.method == 'POST':
      # Make sure all the required fields were found. 
      product_fields = ['category_name', 'category_description', 'category_image']
      if not all(map(lambda p: p in request.form, product_fields) ):
        return "There was an error processing your request. Not all of the required fields were found to be submitted. "
      if not request.form['category_name']: return "The category name is required"
      if request.form['category_description']: description = request.form['category_description']
      else:                                    description = None
      cat_data = {
        'name'       : request.form['category_name']
      , 'description' : description
      , 'image'       : request.form['category_image']
      }
      categories_model.insert(cat_data)
      flash("Category Added Successfully")
      return redirect(url_for('admincp'))

@app.errorhandler(404)
def unauthorized(e):
  return render_template('404.html'), 404
