from flask import (Flask, request, jsonify)
from validator import (TaskSchema)
from data_manager import (Transaction)
from marshmallow import ValidationError
from env_vars import STATUS
import uuid


app = Flask(__name__)


@app.route("/tasks", methods=["GET"])
def get():
    data = data_manager.read_csv_file()
    filter_task = request.args.get("status")
    if filter_task:
        data = list(
            filter(lambda _status: _status["status"] == filter_task, data)
        )
    return jsonify(data)

@app.route("/tasks", methods=["POST"])
def post():
    request_data = request.json
    request_data['task_id'] = str(uuid.uuid4())
    try:
        request_data = task_scheme.load(request_data)
    except ValidationError as err:
        print(f"Error: {err.messages}")
        return jsonify({"error": "Validation failed", "messages": err.messages}), 400
    data = [request_data.get("task_id"), request_data.get("title"),
            request_data.get("description"), request_data.get("status")]
    data_manager.write_csv_file(dataset=[data])
    return jsonify(request_data)

@app.route("/tasks/<task_id>", methods=["PUT"])
def put(task_id):
    request_data = request.json
    data = data_manager.read_csv_file()
    data_list = []
    for index, _data in enumerate(data[0:]):
        if _data.get("task_id") == task_id:
            _data.update(request_data)
        else:
            return jsonify({"error": "Validation failed", "messages": f"No task_id: {task_id} found."}), 404
        data_list.append([value for _, value in _data.items()])
    data_manager.write_csv_file(dataset=data_list, write_option="w")
    return jsonify(_data)

@app.route("/tasks/<task_id>", methods=["DELETE"])
def delete(task_id):
    data = data_manager.read_csv_file()
    data_list = []
    for index, _data in enumerate(data[0:]):
        if _data.get("task_id") == task_id:
            data.pop(index)
            continue
        data_list.append([d for _,d in _data.items()])
    data_manager.write_csv_file(dataset=data_list, write_option="w")
    return jsonify(_data)


if __name__ == "__main__":
    task_scheme = TaskSchema()
    data_manager = Transaction()
    data_manager.write_csv_file()
    app.run(host="0.0.0.0", port=5001, debug=True)