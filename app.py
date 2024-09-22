from flask import Flask, render_template, request, jsonify
import mysql.connector

app = Flask(__name__)

# Database connection function
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="mysql123",
        database="hackathon"
    )

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Function to handle user queries
def handle_query(query):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    # Use regular expressions to extract chapter, sloka numbers, and language
    import re
    chapter_match = re.search(r'chapter\s*(\d+)', query, re.IGNORECASE)
    sloka_match = re.search(r'sloka\s*(\d+)', query, re.IGNORECASE)
    language_match = re.search(r'\b(en|hi|te)\b', query, re.IGNORECASE)

    chapter_num = chapter_match.group(1) if chapter_match else None
    sloka_num = sloka_match.group(1) if sloka_match else None
    language = language_match.group(1) if language_match else 'en'  # Default to English

    if chapter_num and sloka_num:
        try:
            cursor.execute("""
                SELECT gita_sloka.sloka, gita_sloka.meaning, gita_chapters.chapter_name 
                FROM gita_sloka 
                JOIN gita_chapters ON gita_sloka.chapter_number = gita_chapters.chapter_number 
                WHERE gita_sloka.sloka_number = %s AND gita_sloka.chapter_number = %s AND gita_sloka.language = %s
            """, (sloka_num, chapter_num, language))
            sloka = cursor.fetchone()
            if sloka:
                return f"Chapter: {sloka['chapter_name']}\nSloka: {sloka['sloka']}\nMeaning: {sloka['meaning']}"
            else:
                return "Sloka not found. Please check the chapter, sloka number, and language."
        except Exception as e:
            return f"Error: {str(e)}"

    elif chapter_num:
        try:
            cursor.execute("""
                SELECT chapter_name, meaning, summary FROM gita_chapters 
                WHERE chapter_number = %s AND language = %s
            """, (chapter_num, language))
            chapter = cursor.fetchone()
            if chapter:
                return f"Chapter: {chapter['chapter_name']}\nSummary: {chapter['summary']}\nMeaning: {chapter['meaning']}"
            else:
                return "Chapter not found. Please check the chapter number and language."
        except Exception as e:
            return f"Error: {str(e)}"

    else:
        return "I can help you find chapters or slokas. Try asking: 'What is Sloka 5 from Chapter 2 in Hindi?'"




@app.route('/get_sloka', methods=['POST'])
def get_sloka():
    user_input = request.form['query']
    response = handle_query(user_input)
    return jsonify(response=response)

if __name__ == "__main__":
    app.run(debug=True)
