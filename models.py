import pymongo
import util


class Categories:
  def __init__ (self, db):
    self.con = db
    self.db = self.con.db
    self.categories = db.catguice_categories

  def get (self, series = {}):
    return self.categories.find(series)

  def get_one (self, series = {}):
    return self.categories.find_one(series)

  def insert (self, data):
    if "name" in data and not "slug" in data:
      data["slug"] = util.slugify(data["name"])
    return self.categories.insert(data)

  def update (self, series, data):
    return self.categories.update(series, data)

  def delete (self, series):
    category = self.get_one(series)
    products_model = Products(self.con)
    products_model.delete({"category" : category['slug'] })
    return self.categories.remove(series)

class Products:
  def __init__ (self, db):
    self.con = db
    self.db = self.con.db
    self.categories = db.catguice_categories
    self.products = db.catguice_products

  def get (self, series = {}):
    return self.products.find(series)

  def get_one (self, series = {}):
    return self.products.find_one(series)

  def insert (self, data):
    if "name" in data and not "slug" in data:
      data["slug"] = util.slugify(data["name"])
    return self.products.insert(data)

  def update (self, series, data):
    return self.products.update(series, data)

  def delete(self, series):
    return self.products.remove(series)

class Payments:
  def __init__ (self, paypal):
    self.paypal = paypal

class Stats:
  def __init__ (self, db):
    self.con = db
    self.db = self.con.db
    self.stats = db.catguice_stats

  def get (self, series = {}):
    return self.stats.find(series)

  def get_one (self, series = {}):
    return self.stats.find_one(series)

  def insert (self, data):
    return self.stats.insert(data)

  def update (self, series, data):
    return self.stats.update(series, data)
