import pymongo
import util

class Categories:
  def __init__ (self, db):
    self.db = db.db
    self.categories = db.catguice_categories

  def get (self, series = {}):
    return self.categories.find(series)

  def get_one (self, series = {}):
    return self.categories.find_one(series)

  def insert (self, data):
    self.products.insert(data)

  def update (self, series, data):
    self.products.update(series, data)

class Products:
  def __init__ (self, db):
    self.db = db.db
    self.products = db.catguice_products

  def get (self, series = {}):
    return self.products.find(series)

  def get_one (self, series = {}):
    return self.products.find_one(series)

  def insert (self, data):
    if "name" in data and not "slug" in data:
      data["slug"] = util.slugify(data["name"])
    self.products.insert(data)

  def update (self, series, data):
    self.products.update(series, data)
