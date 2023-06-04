from dotenv import load_dotenv
import os

load_dotenv()
HOST_DB = os.environ.get("HOST_DB")
NAME_DB = os.environ.get("NAME_DB")
PASS_DB = os.environ.get("PASS_DB")
PORT_DB = os.environ.get("PORT_DB")
USER_DB = os.environ.get("USER_DB")
