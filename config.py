"""
    The configuration file for CatGuice. 
    This file holds constants that control how the website behaves. 
"""

import os

# You can specify your Database's username and password in a "secrets.py" file if you wish. 
# This has the advantage of allowing you to open source the website while hiding your secret credentials. 
try: 
  import secrets
  dbUsername = secrets.dbUsername
  dbPassword = secrets.dbPassword
except:  
  dbUsername = "your_username_goes_here"
  dbPassword = "your_password_goes_here_dude"
# Your database's host. "localhost" will usually be fine here. 
dbHost = "ds029817.mongolab.com"
# Your database's port. Mongodb's default port is 27017 
dbPort = 29817

# The Host of CatGuice server. 
HOST = "0.0.0.0"
# The Port the server will run off of
PORT = int(os.environ.get('PORT', 5000))

# If this is set to True, then the server will automatically reload modules that have been changed. 
# Set this to False when you're running the website in production mode. 
DEVELOPMENT = True
