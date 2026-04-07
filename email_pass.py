import os
from dotenv import load_dotenv

current_folder = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(current_folder, '.env')

# Koshish 1: Standard tareeka (override=True purani memory delete karta hai)
load_dotenv(env_path, override=True)

email_ = os.getenv('MY_EMAIL')
pass_ = os.getenv('MY_APP_PASSWORD')

# Koshish 2 (The Brahmastra): Agar Windows abhi bhi nautanki kare, toh file ko forcefully read karo!
if pass_ is None and os.path.exists(env_path):
    print("⚠️ Windows Cache detected! Force-reading file...")
    with open(env_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line.startswith('MY_EMAIL='):
                email_ = line.split('=', 1)[1]
            elif line.startswith('MY_APP_PASSWORD='):
                pass_ = line.split('=', 1)[1]

