from flask import Flask, render_template, request
import matplotlib.pyplot as plt
import os

app = Flask(_name_)

# ---------------- ENGINE HEALTH LOGIC ----------------
def predict_engine_health(temp, rpm, oil):
    score = 100

    # Temperature effect
    if temp > 100:
        score -= 40
    elif temp > 90:
        score -= 25
    elif temp > 80:
        score -= 10

    # RPM effect
    if rpm > 6000:
        score -= 30
    elif rpm > 5000:
        score -= 20
    elif rpm > 4000:
        score -= 10

    # Oil effect
    if oil < 20:
        score -= 40
    elif oil < 40:
        score -= 25
    elif oil < 60:
        score -= 10

    if score >= 75:
        status = "GOOD ✅"
    elif score >= 50:
        status = "WARNING ⚠️"
    else:
        status = "BAD ❌"

    return score, status


# ---------------- GRAPH FUNCTION ----------------
def create_graph(rpm, score):
    # project ka root path
    base_dir = app.root_path

    # static folder ka full path
    static_dir = os.path.join(base_dir, "static")

    # agar static folder nahi ho to bana do
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)

    # graph ka full path
    graph_path = os.path.join(static_dir, "graph.png")

    plt.figure()
    plt.plot([0, rpm], [100, score])
    plt.xlabel("RPM")
    plt.ylabel("Health Score")
    plt.title("Engine Health vs RPM")
    plt.grid(True)
    plt.savefig(graph_path)
    plt.close()


# ---------------- ROUTES ----------------
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    try:
        temp = float(request.form.get("temperature"))
        rpm = float(request.form.get("rpm"))
        oil = float(request.form.get("oil"))

        score, status = predict_engine_health(temp, rpm, oil)
        create_graph(rpm, score)

        result = f"Health Score: {score}/100 | Status: {status}"

        return render_template("index.html", result=result, graph=True)

    except Exception as e:
        return render_template(
            "index.html",
            result="Invalid input! Please enter correct values."
        )


# ---------------- RUN APP ----------------
if _name_ == "_main_":
    app.run(debug=True)
