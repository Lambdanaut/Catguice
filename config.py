"""
    The configuration file for CatGuice. 
    This file holds constants that control how the website behaves. 
"""

import os

# The Host of CatGuice server. 
HOST = "0.0.0.0"
# The Port the server will run off of
PORT = int(os.environ.get('PORT', 5000))

# If this is set to True, then the server will automatically reload modules that have been changed. 
# Set this to False when you're running the website in production mode. 
DEVELOPMENT = True
