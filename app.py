from flask import Flask, render_template, request, redirect
import json
import google.generativeai as genai
app = Flask(__name__)

genai.configure(api_key="AQ.Ab8RN6L25YYnrTofZNdEdsjSw4Vh0Yuk0BOURNShBIxUbjnHHw")

model = genai.GenerativeModel("gemini-2.0-flash")


@app.route("/")
def home():
    return render_template("welcome.html")


@app.route("/onboarding")
def onboarding():
    return render_template("onboarding.html")


@app.route("/save_user", methods=["POST"])
def save_user():

    user_data = {
        "name": request.form["name"],
        "age": request.form["age"],
        "occupation": request.form["occupation"],
        "goal": request.form["goal"]
    }

    with open("data/users.json", "w") as file:
        json.dump(user_data, file, indent=4)

    return redirect("/dashboard")


@app.route("/dashboard")
def dashboard():

    with open("data/users.json", "r") as file:
        user = json.load(file)

    with open("data/tasks.json", "r") as file:
        tasks = json.load(file)

    return render_template(
        "dashboard.html",
        user=user,
        tasks=tasks
    )


@app.route("/tasks")
def tasks():

    with open("data/users.json", "r") as file:
        user = json.load(file)

    with open("data/tasks.json", "r") as file:
        tasks = json.load(file)

    completed_tasks = sum(
        1 for task in tasks if task["completed"]
    )

    pending_tasks = len(tasks) - completed_tasks

    progress = 0

    if len(tasks) > 0:
        progress = int(
            (completed_tasks / len(tasks)) * 100
        )

    return render_template(
        "tasks.html",
        user=user,
        tasks=tasks,
        completed_tasks=completed_tasks,
        pending_tasks=pending_tasks,
        progress=progress
    )


@app.route("/analytics")
def analytics():

    with open("data/users.json", "r") as file:
        user = json.load(file)

    return render_template(
        "analytics.html",
        user=user
    )


@app.route("/journal")
def journal():

    with open("data/users.json", "r") as file:
        user = json.load(file)

    return render_template(
        "journal.html",
        user=user
    )


@app.route("/ai")
def ai():

    with open("data/users.json", "r") as file:
        user = json.load(file)

    return render_template(
        "ai_coach.html",
        user=user,
        ai_response=None
    )


@app.route("/ask_ai", methods=["POST"])
def ask_ai():

    with open("data/users.json", "r") as file:
        user = json.load(file)

    question = request.form["question"]

    prompt = f"""
    You are LifeSync AI Coach.

    User Information:
    Name: {user['name']}
    Occupation: {user['occupation']}
    Goal: {user['goal']}

    Give personalized, practical and motivating advice.

    User Question:
    {question}
    """

    try:

        response = model.generate_content(prompt)

        ai_response = response.text

    except Exception as e:

        ai_response = f"Error: {str(e)}"

    return render_template(
        "ai_coach.html",
        user=user,
        ai_response=ai_response,
        user_question=question
    )


@app.route("/settings")
def settings():

    with open("data/users.json", "r") as file:
        user = json.load(file)

    return render_template(
        "settings.html",
        user=user
    )


@app.route("/add_task", methods=["POST"])
def add_task():

    task = request.form["task"]

    with open("data/tasks.json", "r") as file:
        tasks = json.load(file)

    tasks.append({
        "task": task,
        "completed": False
    })

    with open("data/tasks.json", "w") as file:
        json.dump(tasks, file, indent=4)

    return redirect("/tasks")


@app.route("/complete_task/<int:index>")
def complete_task(index):

    with open("data/tasks.json", "r") as file:
        tasks = json.load(file)

    tasks[index]["completed"] = not tasks[index]["completed"]

    with open("data/tasks.json", "w") as file:
        json.dump(tasks, file, indent=4)

    return redirect("/tasks")


@app.route("/delete_task/<int:index>")
def delete_task(index):

    with open("data/tasks.json", "r") as file:
        tasks = json.load(file)

    tasks.pop(index)

    with open("data/tasks.json", "w") as file:
        json.dump(tasks, file, indent=4)

    return redirect("/tasks")


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )