from flask import Flask, jsonify, request
from utils.data_processing import load_employee_data, validate_employee_data
from models.recommendation import recommend_task_redistribution

app = Flask(__name__)

@app.route("/api/recommendations", methods=["GET"])
def get_recommendations():
    df = load_employee_data("data/employees.json")
    validate_employee_data(df)
    recs = recommend_task_redistribution(df)
    return jsonify(recs)

if __name__ == "__main__":
    app.run(debug=True)
