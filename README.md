# Python Full Stack Web Development – Task 3
## Database-Driven CRUD Application with Flask (Authenticated Users Only)

**Maincrafts Technology Internship**

---

## Objective
Build a real database-driven CRUD system where:
- Only logged-in users can manage data
- Users can Create, Read, Update, and Delete records
- Data is stored permanently in SQLite
- Frontend forms are connected to backend logic

---

## Features Implemented
1. Add a new student
2. View all students
3. Edit student details
4. Delete a student
5. Restrict access to logged-in users only

---

## Tech Stack
- **Backend:** Python + Flask
- **Frontend:** HTML, CSS
- **Database:** SQLite
- **Security:** Flask Sessions
- **Password Hashing:** Werkzeug

---

## Project Structure
```
python-fullstack-task3/
├── app.py
├── database.db          (auto-created on first run)
├── requirements.txt
├── README.md
├── static/
│   └── style.css
└── templates/
    ├── login.html
    ├── register.html
    ├── dashboard.html
    ├── students.html
    ├── add_student.html
    └── edit_student.html
```

---

## Database Design

### users table (from Task-2)
| Column   | Type    |
|----------|---------|
| id       | INTEGER PRIMARY KEY |
| username | TEXT UNIQUE |
| password | TEXT (HASHED) |

### students table (Task-3)
| Column | Type |
|--------|------|
| id     | INTEGER PRIMARY KEY |
| name   | TEXT |
| email  | TEXT |
| course | TEXT |

---

## CRUD Flow

```
CREATE  → GET  /add-student   → show form
          POST /add-student   → INSERT into DB → redirect /students

READ    → GET  /students      → SELECT * FROM students → render table

UPDATE  → GET  /edit/<id>     → fetch student → show pre-filled form
          POST /edit/<id>     → UPDATE in DB  → redirect /students

DELETE  → GET  /delete/<id>   → DELETE from DB → redirect /students
```

---

## Security Rules
- All CRUD routes check session → redirect to /login if not authenticated
- Passwords hashed using Werkzeug (never stored in plain text)
- Session-based access control active on every protected route

---

## How to Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the app
python app.py

# 3. Open browser
# http://127.0.0.1:5000
```

Database is created automatically on first run.

---

*Submitted by: Mohammed Rishan | Maincrafts Technology – Python Full Stack Internship*
# python-task-3
