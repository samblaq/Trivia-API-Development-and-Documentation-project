from dotenv import load_dotenv
import os
load_dotenv()
DB_NAME = os.environ.get("trivia")
DB_USER=os.environ.get("postgres")
DB_PASSWORD = os.environ.get("Passw0rd1")