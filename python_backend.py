from flask import Flask, request, jsonify
from gradio_client import Client, handle_file
from celery import Celery

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


# Initialize the Gradio client with your specified model
client = Client("Lakshay1Dagar/Facial_Defect_Detector_with_Fruit_Recommendation")

@app.route('/predict', methods=['POST'])
def predict():
    data = request.args
    task = predict_later.apply_async(args=[data])
    return jsonify({'task_id': task.id}), 202

@celery.task
def predict_later(data):
    if request.method == "GET":
        age = data.get('age')
        gender = data.get('gender')
        face_image_url = data.get('face_image_url')
        hair_image_url = data.get('hair_image_url')

    result = client.predict(
        age=age,
        gender=gender,
        face_image_pred=handle_file(face_image_url),
        hair_image_pred=handle_file(hair_image_url),
        api_name="/predict"
    )
    return result

@app.route('/task_status/<task_id>', methods=['GET'])
def task_status(task_id):
    task = predict_later.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {'state': task.state}
    elif task.state != 'FAILURE':
        response = {'state': task.state, 'result': task.result}
    else:
        response = {'state': task.state, 'error': str(task.info)}
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
