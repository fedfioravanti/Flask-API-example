from flask import Flask, request, jsonify
from flask_smorest import Api, Blueprint
import joblib
import traceback
import numpy as np
import pandas as pd


app = Flask(__name__)


class APIConfig:
    API_TITLE = "TODO API"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.4"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_SWAGGER_UI_PATH = "/docs"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    OPENAPI_REDOC_PATH = "/redoc"
    OPENAPI_REDOC_UI_URL = "https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js"


app.config.from_object(APIConfig)

api = Api(app)

todo = Blueprint("todo", "todo", url_prefix="/todo", description="TODO API")


tasks = [
    {
        "id": uuid.UUID("43936647-5eb7-4913-8221-4e1a6dc84dbf"),
        "created": datetime.now(timezone.utc),
        "completed": False,
        "task": "Create Flask API app"
    }
]


class CreateTask(Schema):
    task = fields.String()


class UpdateTask(CreateTask):
    completed = fields.Bool()


class Task(UpdateTask):
    id = fields.UUID()
    created = fields.DateTime()


class ListTasks(Schema):
    tasks = fields.List(fields.Nested(Task))


class SortByEnum(enum.Enum):
    task = "task"
    created = "created"


class SortDirectionEnum(enum.Enum):
    asc = "asc"
    desc = "desc"


class ListTasksParameters(Schema):
    order_by = fields.Enum(SortByEnum, load_default=SortByEnum.created)
    order = fields.Enum(SortDirectionEnum, load_default=SortDirectionEnum.asc)


@todo.route("/tasks")
class TodoCollection(MethodView):

    @todo.arguments(ListTasksParameters, location="query")
    @todo.response(status_code=200, schema=ListTasks)
    def get(self, parameters):
        return {
            "tasks": sorted(
                tasks,
                key=lambda task: task[parameters["order_by"].value],
                reverse=parameters["order"] == SortDirectionEnum.desc
            )
        }

    @todo.arguments(CreateTask)
    @todo.response(status_code=201, schema=Task)
    def post(self, task):
        task["id"] = uuid.uuid4()
        task["created"] = datetime.now(timezone.utc)
        task["completed"] = False
        tasks.append(task)
        return task

    
@todo.route("/tasks/<uuid:task_id>")
class TodoTask(MethodView):

    @todo.response(status_code=200, schema=Task)
    def get(self, task_id):
        for task in tasks:
            if task["id"] == task_id:
                return task
        abort(404, f"Task with ID {task_id} not found.")

    @todo.arguments(UpdateTask)
    @todo.response(status_code=200, schema=Task)
    def put(self, payload, task_id):
        for task in tasks:
            if task["id"] == task_id:
                task["completed"] = payload["completed"]
                task["task"] = payload["task"]
                return task
        abort(404, f"Task with ID {task_id} not found.")


    @todo.response(status_code=204)
    def delete(self, task_id):
        for index, task in enumerate(tasks):
            if task["id"] == task_id:
                tasks.pop(index)
                return
        abort(404, f"Task with ID {task_id} not found.")





api.register_blueprint(todo)

    



# CODE BELOW TO BE UPDATED




# load the model (do this ONCE when the app starts)
model_path = 'D:/Federico/02_Projects/01_Data_Science/07_Flask-API-example/models/FinalCall-GBC-01.pkl'
try:
    model = joblib.load(model_path)
    print('Model loaded')
except Exception as e:
    print(f"Error loading model: {e}")
    exit()


@app.route('/predict', methods=['POST'])
def predict():
    if model:
        try:
            json_ = request.json
            print(json_)
            query = pd.get_dummies(pd.DataFrame(json_))
            # query = query.reindex(columns=model_columns, fill_value=0)

            prediction = list(model.predict(query))

            return jsonify({'prediction': str(prediction)})

        except:

            return jsonify({'trace': traceback.format_exc()})
    else:
        print ('Train the model first')
        return ('No model here to use')

if __name__ == '__main__':
    app.run(debug=True)  
