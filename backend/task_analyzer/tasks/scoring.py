from datetime import datetime, date


def calculate_urgency(due_date_str):
    if not due_date_str:
        return 10, "No due date set"
    due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
    today = date.today()
    days_until_due = (due_date - today).days

    if days_until_due < 0:
        days_overdue = abs(days_until_due)
        # Here, for each overdue day, 5 points are being added to make it more prioritized
        score = min(100, (days_overdue * 5) + 100)
        reason = "This is an overdue task"
    elif days_until_due == 0:
        score = 95
        reason = "This needs to be completed by today"
    elif days_until_due == 1:
        score = 90
        reason = "This needs to be completed by tommorrow"
    elif days_until_due == 2:
        score = 80
        reason = f"This needs to be completed by {days_until_due} days"
    elif days_until_due == 3:
        score = 70
        reason = f"This needs to be completed by {days_until_due} days"
    elif days_until_due <= 7:
        score = 50
        reason = f"This needs to be completed by {days_until_due} days"
    elif days_until_due <= 14:
        score = 30
        reason = f"This needs to be completed by {days_until_due} days"
    else:
        score = 20
        reason = f"This needs to be completed by {days_until_due} days"
    return score, reason


def calculate_importance(importance):
    if importance == None or 1 > importance or importance > 10:
        importance = 5
    score = importance * 10
    level = ""
    if score >= 80:
        level = "CRITICAL"
    elif score >= 60:
        level = "HIGH"
    elif score >= 40:
        level = "MEDIUM"
    else:
        level = "LOW"

    reason = f"{level} importance ({importance}/10)"
    return score, reason


def calculate_effort(estimated_hour):
    estimated_hour=float(estimated_hour) if estimated_hour else None
    if not estimated_hour or estimated_hour <= 0:
        estimated_hour = 4

    if estimated_hour <= 1:
        score = 100
        reason = f"High priority as this only takes {estimated_hour} hours of time"
    elif estimated_hour <= 2:
        score = 80
        reason = f"Medium priority as this takes {estimated_hour} hours of time"
    elif estimated_hour <= 4:
        score = 60
        reason = f"This takes {estimated_hour} hours of time"
    elif estimated_hour <= 8:
        score = 40
        reason = f"This takes {estimated_hour} hours of time"
    else:
        score = 20
        reason = f"This takes {estimated_hour} hours of time"
    return score, reason


def calculate_dependencies(taskid, all_tasks):
    blocked_tasks = 0
    for task in all_tasks:
        dependency_list = [int(i) for i in task.get("dependencies", '').split(",") if i.strip().isdigit()]
        if taskid in dependency_list:
            blocked_tasks += 1
    if blocked_tasks <= 0:
        score = 0
        reason='No tasks are blocked by this task'
    elif blocked_tasks <= 1:
        score = 30
        reason
    elif blocked_tasks <= 2:
        score = 60
        reason = f"This task is blocking {blocked_tasks} tasks"
    else:
        score = 100
        reason = f"This task is blocking {blocked_tasks} tasks"
    
    return score, reason

def calculate_backward_dependency(task, all_task):
    # Parse dependencies from string to list
    """ This function checks how many incomplete dependencies a task has and assigns a multiplier based on that number.
    """
    dependency_string = task.get("dependencies", "")
    
    # Convert string "1,3,5" to list [1, 3, 5]
    if isinstance(dependency_string, str):
        if not dependency_string or dependency_string.strip() == "":
            dependency_list = []
        else:
            dependency_list = [int(i.strip()) for i in dependency_string.split(",") if i.strip().isdigit()]
    else:
        dependency_list = dependency_string  # Already a list
    
    if not dependency_list:
        multiplier = 1.0
        return multiplier, "No dependencies - ready to start"

    blocker_count = 0
    for task_id in dependency_list:
        dependency_task = next((t for t in all_task if t.get("id") == task_id), None)
        if dependency_task and not dependency_task.get("completed", False):
            blocker_count += 1

    if blocker_count == 0:
        multiplier = 1.0
        reason = "All dependencies completed - ready to start"
    elif blocker_count == 1:
        multiplier = 0.8
        reason = f"Blocked by {blocker_count} incomplete task"
    elif blocker_count == 2:
        multiplier = 0.6
        reason = f"Blocked by {blocker_count} incomplete tasks"
    elif blocker_count >= 3:
        multiplier = 0.4
        reason = f"Blocked by {blocker_count} incomplete tasks"
    
    return multiplier, reason

def calculate_priority_score(task, all_tasks, strategy="Smart Balance"):
    # Strategy weights
    STRATEGY_WEIGHTS = {
        "Smart Balance": {
            "urgency": 0.30,
            "importance": 0.35,
            "effort": 0.20,
            "dependence": 0.15,
        },
        "Deadline Driven": {
            "urgency": 0.60,
            "importance": 0.20,
            "effort": 0.10,
            "dependence": 0.10,
        },
        "High Impact": {
            "urgency": 0.15,
            "importance": 0.55,
            "effort": 0.15,
            "dependence": 0.15,
        },
        "Fastest Wins": {
            "urgency": 0.20,
            "importance": 0.20,
            "effort": 0.45,
            "dependence": 0.15,
        },
    }

    weights = STRATEGY_WEIGHTS.get(strategy)
    urgency_score, urgency_reason = calculate_urgency(task.get("due_date"))
    importance_score, importance_reason = calculate_importance(task.get("importance"))
    effort_score, effort_reason = calculate_effort(task.get("estimated_hours"))
    dependency_score, dependency_reason = calculate_dependencies(
        task.get("id"), all_tasks
    )

    base_score = (
        urgency_score * weights["urgency"]
        + importance_score * weights["importance"]
        + effort_score * weights["effort"]
        + dependency_score*weights["dependence"]
    )
    dependency_muliplier,multiplier_reason=calculate_backward_dependency(task,all_tasks)
    final_score=base_score*dependency_muliplier
    
    #explanation on why that particular task is proritized at it's position
    explanation = {
        'base_score': round(base_score, 2),
        'final_score': round(final_score, 2),
        'urgency': {'score': urgency_score, 'reason': urgency_reason},
        'importance': {'score': importance_score, 'reason': importance_reason},
        'effort': {'score': effort_score, 'reason': effort_reason},
        'forward_deps': {'score': dependency_score, 'reason': dependency_reason},
        'backward_deps': {'multiplier': dependency_muliplier, 'reason': multiplier_reason}
    }
    return final_score,explanation

def prioritized_tasks(all_tasks, strategy="Smart Balance"):
    scored_tasks = []
    for task in all_tasks:
        result = calculate_priority_score(task, all_tasks, strategy)
        priority_score, explanation = result
        # Create new dict with priority info
        task_with_score = {
            **task,  # Copy all original fields
            'priority_score': round(priority_score, 2),
            'priority_explanation': explanation
        }
        scored_tasks.append(task_with_score)
    return scored_tasks

def get_sorted_tasks(all_tasks, strategy="Smart Balance"):
    """Get tasks sorted by priority"""
    scored_tasks = prioritized_tasks(all_tasks, strategy)
    sorted_tasks = sorted(scored_tasks, key=lambda x: x['priority_score'], reverse=True)
    return sorted_tasks