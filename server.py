from flask import *
import pymongo

import os

import config
import mail
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
  if categories.count() == 1:
    return redirect(url_for('category', category_slug = categories[0]['slug']))
  else:
    return render_template("index.html", categories=categories)

@app.route("/about")
def about():
  return render_template("about.html")

@app.route("/custom_order", methods=['GET', 'POST'])
def custom_order():
  if request.method == 'GET':
    return render_template("custom_order.html")
  if request.method == 'POST':
    # Mail Catguice
    inquire_catguice_subject = "Custom Order from " + request.form['name']
    inquire_catguice_email = render_template("custom_order_email.html", client=request.form)
    mail.send_mail(config.MY_EMAIL, config.MY_EMAIL, inquire_catguice_subject, inquire_catguice_email)
    return render_template("custom_order_success.html")

@app.route("/product/<product_slug>", methods=['GET', 'POST'])
def product(product_slug):
  if request.method == 'GET':
    product = products_model.get_one({"slug" : product_slug.lower()})
    if not product: abort(404)
    category = categories_model.get_one({"slug" : product['category'] })
    return render_template("product.html", product=product, category=category)
  elif request.method == 'POST':
    if g.admin:
      # Delete the product
      products_model.delete({"slug" : product_slug})
      flash("Product <strong>" + product_slug + "</strong> Deleted Successfully")
      return redirect(url_for('admincp'))

@app.route("/product/<product_slug>/purchase", methods=['POST'])
def purchase_product(product_slug):
  product = products_model.get_one({"slug" : product_slug.lower() })
  if not product: abort(404)
  category = categories_model.get_one({"slug" : product['category'] })
  # Mail Catguice
  purchase_catguice_subject = "Purchase from " + request.form['client_name']
  purchase_catguice_email = render_template("catguice_email.html", client=request.form, product=product, category=category)
  mail.send_mail(config.MY_EMAIL, config.MY_EMAIL, purchase_catguice_subject, purchase_catguice_email)
  # Mail Client
  purchase_catguice_subject = "Instructions for Completing your Purchase"
  purchase_catguice_email = render_template("customer_email.html", client=request.form, category=category)
  mail.send_mail(config.MY_EMAIL, config.MY_EMAIL, purchase_catguice_subject, purchase_catguice_email)
  return redirect(url_for('purchase_product_success', product_slug=product_slug))

@app.route("/product/<product_slug>/purchase_success", methods=['GET'])
def purchase_product_success(product_slug):
  # Purchase Success
  product = products_model.get_one({"slug" : product_slug.lower() })
  if not product: abort(404)
  category = categories_model.get_one({"slug" : product['category'] })
  return render_template("purchase_success.html", product=product, category=category)

@app.route("/product/<product_slug>/edit", methods=['GET', 'POST'])
def edit_product(product_slug):
  if not secrets_found: abort(404)
  if g.admin:
    product = products_model.get_one({"slug" : product_slug.lower() })
    if not product: abort(404)
    if request.method == 'GET':
      return redirect(url_for('purchase_product_success', product_slug=product_slug))
    elif request.method == 'POST':
      pass

@app.route("/categories/<category_slug>", methods=['GET', 'POST'])
def category(category_slug):
  if request.method == 'GET':
    category = categories_model.get_one({"slug" : category_slug.lower()})
    if not category: abort(404)
    products = products_model.get({"category" : category['slug'] })
    return render_template("category.html", category=category, products=products)
  elif request.method == 'POST':
    # Delete the category
    if g.admin:
      categories_model.delete({"slug" : category_slug.lower()})
      flash("Category and all of its Associated Products Deleted Successfully")
      return redirect(url_for('admincp'))

@app.route("/admincp", methods=['GET','POST'])
def admincp():
  if not secrets_found: abort(404)
  if request.method == 'POST':
    if not 'admin_password' in request.form: abort(404)
    if request.form['admin_password'] == secrets.admin_password:
      session['admin_password']=secrets.admin_password
      session.permanent = True
      return redirect(url_for('admincp', admin=True))
    return redirect(url_for('admincp', admin=False))
  elif request.method == 'GET':
    products = products_model.get()
    categories = categories_model.get()
    return render_template("admincp.html", products=products, categories=categories)
 
@app.route("/admincp/add_product", methods=['POST'])
def add_product():
  if g.admin:
    if request.method == 'POST':
      # Make sure all the required fields were found. 
      product_fields = ['product_name', 'product_description', 'product_price', 'product_images', 'product_primary_colors', 'product_secondary_color_name', 'product_secondary_colors', 'product_sizes', 'product_category']
      if not all(map(lambda p: p in request.form, product_fields) ):
        return "There was an error processing your request. Not all of the required fields were found to be submitted. "
      if not request.form['product_name']: return "The product name is required"
      if not request.form['product_category']: return "The category is required"
      if request.form['product_description']: description = request.form['product_description']
      else:                                   description = None
      if 'product_secondary_color_optional' in request.form: secondary_color_optional = True
      else:                                                  secondary_color_optional = False
      product_data = {
        'name'                     : request.form['product_name']
      , 'description'              : description
      , 'price'                    : request.form['product_price']
      , 'images'                   : util.split_product_list(request.form['product_images'])
      , 'primary_colors'           : util.split_product_list(request.form['product_primary_colors'])
      , 'secondary_color_name'     : request.form['product_secondary_color_name']
      , 'secondary_colors'         : util.split_product_list(request.form['product_secondary_colors'])
      , 'secondary_color_optional' : secondary_color_optional
      , 'sizes'                    : util.split_product_list(request.form['product_sizes'])
      , 'category'                 : request.form['product_category']
      }
      products_model.insert(product_data)
      flash("Product Added Successfully")
      return redirect(url_for('admincp'))

@app.route("/admincp/add_category", methods=['POST'])
def add_category():
  if g.admin:
    if request.method == 'POST':
      # Make sure all the required fields were found. 
      category_fields = ['category_name', 'category_singular_name', 'category_description', 'category_image']
      if not all(map(lambda c: c in request.form, category_fields) ):
        return "There was an error processing your request. Not all of the required fields were found to be submitted. "
      if not request.form['category_name']: return "The category name is required"
      if request.form['category_description']: description = request.form['category_description']
      else:                                    description = None
      if 'category_purchasable' in request.form: purchasable = True
      else:                                      purchasable = False
      cat_data = {
        'name'          : request.form['category_name']
      , 'singular_name' : request.form['category_singular_name']
      , 'description'   : description
      , 'image'         : request.form['category_image']
      , 'purchasable'   : purchasable
      }
      categories_model.insert(cat_data)
      flash("Category Added Successfully")
      return redirect(url_for('admincp'))

@app.errorhandler(404)
def unauthorized(e):
  return render_template('404.html'), 404