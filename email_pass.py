import os
from dotenv import load_dotenv

# Ye function chhipi hui .env file ko background mein load kar lega
load_dotenv()

# Yahan code sidha .env file se tera asli data uthayega
email_ = os.getenv('MY_EMAIL')
pass_ = os.getenv('MY_APP_PASSWORD')