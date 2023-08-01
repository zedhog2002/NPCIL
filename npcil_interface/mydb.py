import mysql.connector

dataBase = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    passwd = 'Kingshuk@2002'
)

cursorObject = dataBase.cursor()
cursorObject.execute("CREATE DATABASE npcil_db")