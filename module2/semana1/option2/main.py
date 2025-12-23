from flask.views import MethodView
from flask import (Flask, request, jsonify)
from validator import (TaskSchema)
from data_manager import (Transaction)
from marshmallow import ValidationError
import uuid


class TaskAPI(MethodView):
    init_every_request = False

    def __init__(self, data, schema):
        self.schema = schema
        self.data = data

    def _get_item(self):
        data = data_manager.read_csv_file()
        filter_task = request.args.get("status")
        if filter_task:
            data = list(
                filter(lambda _status: _status["status"] == filter_task, data)
            )
        return data

    def get(self):
        data = self._get_item()
        return jsonify(data)
    
    def post(self):
        request_data = request.json
        request_data['task_id'] = str(uuid.uuid4())
        try:
            request_data = self.schema.load(request_data)
        except ValidationError as err:
            print(f"Error: {err.messages}")
            return jsonify({"error": "Validation failed", "messages": err.messages}), 400
        data = [request_data.get("task_id"), request_data.get("title"),
                request_data.get("description"), request_data.get("status")]
        data_manager.write_csv_file(dataset=[data])
        return jsonify(request_data)

    def put(self, task_id):
        try:
            request_data = self.schema.load(request.json)
        except ValidationError as err:
            print(f"Error: {err.messages}")
            return jsonify({"error": "Validation failed", "messages": err.messages}), 400
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

    def delete(self, task_id):
        data = data_manager.read_csv_file()
        data_list = []
        for index, _data in enumerate(data[0:]):
            if _data.get("task_id") == task_id:
                data.pop(index)
                continue
            data_list.append([d for _,d in _data.items()])
        data_manager.write_csv_file(dataset=data_list, write_option="w")
        return jsonify(_data)


def register_api(app, data, model, name):
    tasks = TaskAPI.as_view(f"{name}", data, model)
    app.add_url_rule(f"/{name}/", view_func=tasks, methods=["GET", "POST"])
    app.add_url_rule(f"/{name}/<task_id>", view_func=tasks, methods=["PUT", "DELETE"])

if __name__ == "__main__":
    app = Flask(__name__)
    task_schema = TaskSchema()
    data_manager = Transaction()
    data_manager.write_csv_file()
    register_api(app, data_manager, task_schema, "tasks")
    app.run(host="0.0.0.0", port=5001, debug=True)
