# CREATE TABLE gita_chapters (         create a table in mysql first
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     chapter_name VARCHAR(255),
#     chapter_number INT,
#     verse_count INT,
#     language VARCHAR(10),
#     yoga_name VARCHAR(100),
#     meaning VARCHAR(255),
#     summary TEXT
# );

import json
import mysql.connector

# Connect to MySQL database
db_connection = mysql.connector.connect(
    host="localhost",
    user="your_username",
    password="your_password",
    database="your_database"
)
cursor = db_connection.cursor()

# Open and read the JSON file
with open('/path/to/genai.chapter.json', 'r',encoding='utf-8') as file:
    data = json.load(file)

# Insert data into the MySQL table
for entry in data:
    chapter_name = entry.get('chapterName')
    chapter_number = entry.get('chapterNumber')
    verse_count = entry.get('verseCount')
    language = entry.get('language')
    yoga_name = entry.get('yogaName')
    meaning = entry.get('meaning')
    summary = entry.get('summary')

    cursor.execute('''
        INSERT INTO gita_chapters 
        (chapter_name, chapter_number, verse_count, language, yoga_name, meaning, summary) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    ''', (chapter_name, chapter_number, verse_count, language, yoga_name, meaning, summary))

# Commit the transaction
db_connection.commit()

# Close the connection
cursor.close()
db_connection.close()

