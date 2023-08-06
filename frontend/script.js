// frontend/script.js
const apiUrl = 'http://localhost:5000/tasks';

async function createTask() {
    const title = document.getElementById('title').value;
    const description = document.getElementById('description').value;
    const dueDate = document.getElementById('dueDate').value;
    const status = document.getElementById('status').value;

    const newTask = {
        title,
        description,
        due_date: dueDate,
        status,
    };

    try {
        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(newTask),
        });

        if (response.ok) {
            const data = await response.json();
            displayTask(data);
            clearForm();
        } else {
            console.error('Failed to create a task:', response.statusText);
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

function displayTask(task) {
    const tasksList = document.getElementById('tasks');
    const li = document.createElement('li');
    li.innerHTML = `<span>Title: ${task.title}</span><br>
                    <span>Description: ${task.description}</span><br>
                    <span>Due Date: ${new Date(task.due_date).toLocaleString()}</span><br>
                    <span>Status: ${task.status}</span><br>
                    <button onclick="deleteTask(${task.id})">Delete</button>`;
    tasksList.appendChild(li);
}

async function getTasks() {
    try {
        const response = await fetch(apiUrl);
        if (response.ok) {
            const data = await response.json();
            data.forEach(displayTask);
        } else {
            console.error('Failed to fetch tasks:', response.statusText);
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

async function deleteTask(taskId) {
    try {
        const response = await fetch(`${apiUrl}/${taskId}`, {
            method: 'DELETE',
        });

        if (response.ok) {
            const taskElement = document.querySelector(`li span[onclick="deleteTask(${taskId})"]`).parentElement;
            taskElement.remove();
        } else {
            console.error('Failed to delete the task:', response.statusText);
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

function clearForm() {
    document.getElementById('title').value = '';
    document.getElementById('description').value = '';
    document.getElementById('dueDate').value = '';
    document.getElementById('status').value = 'Not Started';
}

getTasks();
