# CREATE TABLE gita_sloka (  //create table for sloka in MYSQL
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     sloka_number INT,
#     speaker varchar(255),
#     language VARCHAR(10),
#     sloka VARCHAR(255),
#     meaning text,
#     chapter_number int default 1
# ); 
import json
import mysql.connector

# Connect to MySQL database
db_connection = mysql.connector.connect(
    host="localhost",  # Change if using a remote server
    user="your_username",
    password="your_password",
    database="your_database"
)
cursor = db_connection.cursor()

# Open and read the JSON file (ensure the correct path)
with open('/path/to/sloka.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Insert data into the gita_sloka table
for entry in data:
    sloka_number = entry.get('slokaNumber')  # Adapt to match JSON key names
    speaker = entry.get('speaker')
    language = entry.get('language')
    sloka = entry.get('sloka')
    meaning = entry.get('meaning')

    cursor.execute('''
        INSERT INTO gita_sloka 
        (sloka_number, speaker, language, sloka, meaning) 
        VALUES (%s, %s, %s, %s, %s)
    ''', (sloka_number, speaker, language, sloka, meaning))

# Commit the transaction
db_connection.commit()

# Close the connection
cursor.close()
db_connection.close()
