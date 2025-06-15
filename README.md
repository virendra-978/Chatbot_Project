
# 📖 Bhagavad Gita Chatbot (Flask + MySQL)

A conversational web chatbot that provides slokas and chapter summaries from the **Bhagavad Gita**. The application is built using **Flask** for the backend and **MySQL** as the database. Users can ask questions like “What is Sloka 5 from Chapter 2 in Hindi?” and get a relevant response.

## 🌟 Features

- Query Bhagavad Gita slokas and summaries using natural language.
- Supports multilingual output: English (`en`), Hindi (`hi`), Telugu (`te`).
- Sloka and chapter information retrieved from MySQL database.
- Friendly web interface powered by Flask.

## 🛠️ Tech Stack

- Python (Flask)
- MySQL
- HTML (with Jinja2 templates)

## 📁 Project Structure

```
BhagavadGitaChatbot/
│
├── app.py                  # Main Flask application
├── templates/
│   └── index.html          # Frontend web interface
├── static/                 # (Optional) for CSS/JS files
├── README.md               # Project documentation
```

## 🧾 Prerequisites

- Python 3.x
- MySQL Server

## ✅ Steps to Run

1. **Install required Python packages**

```bash
pip install flask mysql-connector-python
```

2. **Set up the MySQL Database**

Create a database named `hackathon` and the following tables:

```sql
CREATE TABLE gita_chapters (
    chapter_number INT,
    chapter_name VARCHAR(255),
    meaning TEXT,
    summary TEXT,
    language VARCHAR(10)
);

CREATE TABLE gita_sloka (
    chapter_number INT,
    sloka_number INT,
    sloka TEXT,
    meaning TEXT,
    language VARCHAR(10)
);
```

> Populate the tables with relevant Bhagavad Gita data in different languages (`en`, `hi`, `te`).

3. **Run the Flask app**

```bash
python app.py
```

4. **Open the Web App**

Navigate to `http://127.0.0.1:5000` in your browser.

## 🧠 Example Queries

- `What is Sloka 4 from Chapter 2 in Hindi?`
- `Give me Chapter 3 in English`
- `Chapter 6 summary in Telugu`

## 📌 Notes

- Default language is **English** if not specified.
- Regular expressions are used to extract chapter, sloka, and language from user input.
- Robust error handling for invalid input or DB errors.

## 👨‍💻 Author

**Bhagavad Gita Chatbot App** by Virendra
