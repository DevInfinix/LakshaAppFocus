import sqlite3

class Database:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.conn.row_factory = sqlite3.Row  # Use Row factory to fetch rows as dictionaries
        self.cursor = self.conn.cursor()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                task_name TEXT,
                                project TEXT,
                                status BOOLEAN,
                                day INTEGER,
                                month INTEGER,
                                year INTEGER
                            )''')
        self.conn.commit()

    def add_todo(self, task_name, project, status, day, month, year):
        self.cursor.execute('''INSERT INTO tasks (task_name, project, status, day, month, year)
                               VALUES (?, ?, ?, ?, ?, ?)''', (task_name, project, status, day, month, year))
        self.conn.commit()

    def delete_todo(self, task_id):
        self.cursor.execute('''DELETE FROM tasks WHERE id = ?''', (task_id,))
        self.conn.commit()

    def update_todo_status(self, task_id, status):
        self.cursor.execute('''UPDATE tasks SET status = ? WHERE id = ?''', (status, task_id))
        self.conn.commit()

    def search_todo_by_project(self, project):
        self.cursor.execute('''SELECT * FROM tasks WHERE project = ?''', (project,))
        return [dict(row) for row in self.cursor.fetchall()]

    def search_todo_by_id(self, task_id):
        self.cursor.execute('''SELECT * FROM tasks WHERE id = ?''', (task_id,))
        return dict(self.cursor.fetchone())

    def get_completed_tasks(self):
        self.cursor.execute('''SELECT * FROM tasks WHERE status = ?''', (True,))
        return [dict(row) for row in self.cursor.fetchall()]

    def get_total_tasks_done(self):
        self.cursor.execute('''SELECT COUNT(*) FROM tasks WHERE status = ?''', (True,))
        return self.cursor.fetchone()[0]

    def __del__(self):
        self.conn.close()