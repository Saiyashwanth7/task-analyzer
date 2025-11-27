const API_BASE = 'http://127.0.0.1:8000/api';
let currentStrategy = 'Smart Balance';

// DOM Elements
const addTaskForm = document.getElementById('addTaskForm');
const analyzeBtn = document.getElementById('analyzeBtn');
const loading = document.getElementById('loading');
const resultsSection = document.getElementById('resultsSection');
const tasksList = document.getElementById('tasksList');
const strategyButtons = document.querySelectorAll('.btn-strategy');

// Strategy Selection
strategyButtons.forEach(btn => {
    btn.addEventListener('click', () => {
        strategyButtons.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        currentStrategy = btn.dataset.strategy;
    });
});

// Add Task Form Submit
addTaskForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const taskData = {
        title: document.getElementById('title').value,
        due_date: document.getElementById('due_date').value || null,
        estimated_hours: document.getElementById('estimated_hours').value || null,
        importance: parseInt(document.getElementById('importance').value),
        dependencies: document.getElementById('dependencies').value || '',
        completed: false
    };
    
    try {
        const response = await fetch(`${API_BASE}/tasks/add/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(taskData)
        });
        
        if (response.ok) {
            alert('✅ Task added successfully!');
            addTaskForm.reset();
            document.getElementById('importance').value = 5; // Reset to default
        } else {
            const error = await response.json();
            alert('❌ Error adding task: ' + JSON.stringify(error));
        }
    } catch (error) {
        alert('❌ Error: ' + error.message);
    }
});

// Analyze Tasks
analyzeBtn.addEventListener('click', async () => {
    loading.classList.remove('hidden');
    resultsSection.classList.add('hidden');
    
    try {
        const response = await fetch(`${API_BASE}/tasks/analyze/?strategy=${encodeURIComponent(currentStrategy)}`);
        
        if (!response.ok) {
            throw new Error('Failed to analyze tasks');
        }
        
        const tasks = await response.json();
        displayTasks(tasks);
        
    } catch (error) {
        alert('❌ Error analyzing tasks: ' + error.message);
    } finally {
        loading.classList.add('hidden');
    }
});

// Display Tasks
function displayTasks(tasks) {
    if (tasks.length === 0) {
        tasksList.innerHTML = '<p style="text-align: center; color: #999;">No tasks found. Add some tasks first!</p>';
        resultsSection.classList.remove('hidden');
        return;
    }
    
    tasksList.innerHTML = tasks.map((task, index) => {
        const priorityClass = getPriorityClass(task.priority_score);
        const explanation = task.priority_explanation;
        
        return `
            <div class="task-card">
                <div class="task-header">
                    <div>
                        <span style="color: #999; font-size: 20px; font-weight: bold;">#${index + 1}</span>
                        <h3 class="task-title">${task.title}</h3>
                    </div>
                    <span class="priority-badge ${priorityClass}">
                        Score: ${task.priority_score}
                    </span>
                </div>
                
                <div class="task-details">
                    <div class="detail-item">
                        <strong>📅 Due:</strong> ${task.due_date || 'Not set'}
                    </div>
                    <div class="detail-item">
                        <strong>⏱️ Effort:</strong> ${task.estimated_hours ? task.estimated_hours + 'h' : 'Not set'}
                    </div>
                    <div class="detail-item">
                        <strong>⭐ Importance:</strong> ${task.importance}/10
                    </div>
                    <div class="detail-item">
                        <strong>✅ Status:</strong> ${task.completed ? 'Done' : 'Pending'}
                    </div>
                </div>
                
                <div class="task-explanation">
                    <h4>Priority Breakdown:</h4>
                    <div class="explanation-grid">
                        <div class="explanation-item">
                            <strong>Urgency</strong>
                            ${explanation.urgency.reason}
                        </div>
                        <div class="explanation-item">
                            <strong>Importance</strong>
                            ${explanation.importance.reason}
                        </div>
                        <div class="explanation-item">
                            <strong>Effort</strong>
                            ${explanation.effort.reason}
                        </div>
                        <div class="explanation-item">
                            <strong>Blocker</strong>
                            ${explanation.forward_deps.reason}
                        </div>
                        <div class="explanation-item">
                            <strong>Dependencies</strong>
                            ${explanation.backward_deps.reason}
                        </div>
                    </div>
                </div>
            </div>
        `;
    }).join('');
    
    resultsSection.classList.remove('hidden');
}

// Get Priority Class
function getPriorityClass(score) {
    if (score >= 70) return 'priority-high';
    if (score >= 40) return 'priority-medium';
    return 'priority-low';
}