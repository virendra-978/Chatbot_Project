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

    if "chapter" in query and "sloka" in query:
        try:
            chapter_num = int(query.split("chapter")[1].split()[0])
            sloka_num = int(query.split("sloka")[1].split()[0])
            cursor.execute("""
                SELECT sloka, meaning FROM gita_sloka 
                WHERE sloka_number = %s AND chapter_number = %s
            """, (sloka_num, chapter_num))
            sloka = cursor.fetchone()
            if sloka:
                return f"Sloka: {sloka['sloka']}\nMeaning: {sloka['meaning']}"
            else:
                return "Sloka not found. Please check the chapter and sloka number."
        except:
            return "Please provide valid chapter and sloka numbers."
    
    elif "chapter" in query:
        try:
            chapter_num = int(query.split("chapter")[1].split()[0])
            cursor.execute("""
                SELECT chapter_name, meaning, summary FROM gita_chapters 
                WHERE chapter_number = %s
            """, (chapter_num,))
            chapter = cursor.fetchone()
            if chapter:
                return f"Chapter: {chapter['chapter_name']}\nSummary: {chapter['summary']}\nMeaning: {chapter['meaning']}"
            else:
                return "Chapter not found. Please check the chapter number."
        except:
            return "Please provide a valid chapter number."
    
    else:
        return "I can help you find chapters or slokas. Try asking: 'What is Sloka 5 from Chapter 2?'"

# Web route to handle user query via form submission
@app.route('/get_sloka', methods=['POST'])
def get_sloka():
    user_input = request.form['query']
    response = handle_query(user_input)
    return jsonify(response=response)

# API endpoint to get sloka and meaning by chapter and sloka numbers (GET request)
@app.route('/api/sloka', methods=['GET'])
def api_get_sloka():
    chapter_num = request.args.get('chapter')
    sloka_num = request.args.get('sloka')
    
    if not chapter_num or not sloka_num:
        return jsonify({"error": "Chapter number and Sloka number are required."}), 400

    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT sloka, meaning FROM gita_sloka 
            WHERE sloka_number = %s AND chapter_number = %s
        """, (sloka_num, chapter_num))
        sloka = cursor.fetchone()
        
        if sloka:
            return jsonify({
                "chapter": chapter_num,
                "sloka_number": sloka_num,
                "sloka": sloka['sloka'],
                "meaning": sloka['meaning']
            }), 200
        else:
            return jsonify({"error": "Sloka not found. Please check the chapter and sloka number."}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API endpoint to get chapter summary and meaning by chapter number (GET request)
@app.route('/api/chapter', methods=['GET'])
def api_get_chapter():
    chapter_num = request.args.get('chapter')
    
    if not chapter_num:
        return jsonify({"error": "Chapter number is required."}), 400

    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT chapter_name, meaning, summary FROM gita_chapters 
            WHERE chapter_number = %s
        """, (chapter_num,))
        chapter = cursor.fetchone()

        if chapter:
            return jsonify({
                "chapter_number": chapter_num,
                "chapter_name": chapter['chapter_name'],
                "summary": chapter['summary'],
                "meaning": chapter['meaning']
            }), 200
        else:
            return jsonify({"error": "Chapter not found. Please check the chapter number."}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#if __name__ == "_main_":
 #   app.run(debug=True)
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)