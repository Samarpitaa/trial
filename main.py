from flask import Flask, request, jsonify
from datetime import datetime
import sqlite3

app = Flask(__name__)

DATABASE = 'task_manager.db'


def create_connection():
    return sqlite3.connect('task_manager.db')

def execute_query(query, args=()):
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(query, args)
    conn.commit()
    conn.close()


def fetch_all(query, args=()):
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(query, args)
    rows = cur.fetchall()
    conn.close()
    return rows

@app.route('/tasks', methods=['POST'])
def create_task():
    try:
        data = request.json
        title = data['title']
        description = data['description']
        due_date = datetime.strptime(data['due_date'], '%Y-%m-%d %H:%M:%S')
        status = data['status']

        query = 'INSERT INTO tasks (title, description, due_date, status) VALUES (?, ?, ?, ?)'
        execute_query(query, (title, description, due_date, status))

        return jsonify({'message': 'Task created successfully.'}), 201
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Failed to create a task.'}), 500


@app.route('/tasks', methods=['GET'])
def get_tasks():
    try:
        query = 'SELECT * FROM tasks'
        tasks = fetch_all(query)

        task_list = []
        for task in tasks:
            task_list.append({
                'id': task[0],
                'title': task[1],
                'description': task[2],
                'due_date': task[3],
                'status': task[4],
            })

        return jsonify(task_list), 200
    except Exception as e:
        return jsonify({'error': 'Failed to fetch tasks.'}), 500

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    try:
        query = 'DELETE FROM tasks WHERE id = ?'
        execute_query(query, (task_id,))
        return '', 204
    except Exception as e:
        return jsonify({'error': 'Failed to delete the task.'}), 500

if __name__ == '__main__':
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            due_date TEXT NOT NULL,
            status TEXT NOT NULL
        )
    '''
    execute_query(create_table_query)
    app.run(debug=True)

