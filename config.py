from dotenv import load_dotenv
import os

load_dotenv()
HOST_DB = os.environ.get("HOST_DB")
NAME_DB = os.environ.get("NAME_DB")
PASS_DB = os.environ.get("PASS_DB")
PORT_DB = os.environ.get("PORT_DB")
USER_DB = os.environ.get("USER_DB")
SECRET = os.environ.get("SECRET")
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
