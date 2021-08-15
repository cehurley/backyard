from .mysql_provider import MySQLProvider
from dotenv import dotenv_values


config = dotenv_values(".env")
Env = MySQLProvider(config)
Registry = {}
