import pymongo

class Products:
  def __init__ (self, db):
    self.db = db.db
    self.products = db.catguice_products

  def get (self, series = {}):
    return self.products.find(series)

  def insert (self, data):
    self.products.insert(data)

  def update (self, series, data):
    self.products.update(series, data)
