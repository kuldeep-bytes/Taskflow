from flask import Blueprint, render_template, request, redirect, url_for, flash

from app.models import db, Task

from datetime import datetime


main = Blueprint("main", __name__)


@main.route("/")
def home():
    return render_template("home.html")


@main.route("/dashboard")
def dashboard():

    total_tasks = Task.query.count()

    completed_tasks = Task.query.filter_by(
        completed=True
    ).count()

    pending_tasks = Task.query.filter_by(
        completed=False
    ).count()

    recent_tasks = Task.query.order_by(
        Task.created_at.desc()
    ).limit(5).all()

    return render_template(
        "dashboard.html",
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        pending_tasks=pending_tasks,
        recent_tasks=recent_tasks
    )


@main.route("/add-task", methods=["GET", "POST"])
def add_task():

    if request.method == "POST":

        title = request.form.get("title")
        description = request.form.get("description")

        start_at = datetime.fromisoformat(
            request.form.get("start_at")
        )

        due_at = datetime.fromisoformat(
            request.form.get("due_at")
        )

        if due_at <= start_at:
            flash("Due time must be after start time!", "error")
            return redirect(url_for("main.add_task"))

        new_task = Task(
            title=title,
            description=description,
            start_at=start_at,
            due_at=due_at
        )

        db.session.add(new_task)
        db.session.commit()

        flash("Task added successfully!", "success")

        return redirect(url_for("main.dashboard"))

    return render_template("add_task.html")

@main.route("/tasks")
def tasks():

    search = request.args.get("search", "")
    status = request.args.get("status", "all")

    query = Task.query

    if search:
        query = query.filter(
            Task.title.ilike(f"%{search}%")
        )

    if status == "pending":
        query = query.filter_by(completed=False)

    elif status == "completed":
        query = query.filter_by(completed=True)

    all_tasks = query.order_by(
        Task.created_at.desc()
    ).all()

    return render_template(
        "tasks.html",
        tasks=all_tasks,
        search=search,
        status=status
    )

@main.route("/edit-task/<int:task_id>", methods=["GET", "POST"])
def edit_task(task_id):

    task = Task.query.get_or_404(task_id)

    if request.method == "POST":

        task.title = request.form.get("title")
        task.description = request.form.get("description")

        start_at = datetime.fromisoformat(
                        request.form.get("start_at")
                    )

        due_at = datetime.fromisoformat(
                request.form.get("due_at")
                )

        if due_at <= start_at:
            flash("Due time must be after start time!", "error")
            return redirect(url_for("main.edit_task", task_id=task.id))

        task.start_at = start_at
        task.due_at = due_at
        
        db.session.commit()
        flash("Task updated successfully!", "success")

        return redirect(url_for("main.tasks"))

    return render_template(
        "edit_task.html",
        task=task
    )

@main.route("/delete-task/<int:task_id>", methods=["POST"])
def delete_task(task_id):

    task = Task.query.get_or_404(task_id)

    db.session.delete(task)
    db.session.commit()
    flash("Task deleted successfully!", "success")

    return redirect(url_for("main.tasks"))

@main.route("/toggle-task/<int:task_id>", methods=["POST"])
def toggle_task(task_id):

    task = Task.query.get_or_404(task_id)

    task.completed = not task.completed

    if task.completed:
        task.completed_at = datetime.now()
        flash("Task completed successfully!", "success")
    else:
        task.completed_at = None
        flash("Task marked as pending!", "success")

    db.session.commit()
    
    return redirect(url_for("main.tasks"))