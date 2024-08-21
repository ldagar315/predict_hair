from flask import Flask, request, jsonify
from gradio_client import Client, handle_file

app = Flask(__name__)

# Initialize the Gradio client with your specified model
client = Client("Lakshay1Dagar/Facial_Defect_Detector_with_Fruit_Recommendation")

@app.route('/predict', methods=['POST','GET'])
def predict():
    # Extract the required parameters from the incoming request
    if request.method == 'GET':
        age = request.args.get('age')
        gender = request.args.get('gender')
        face_image_url = request.args.get('face_image_url')
        hair_image_url = request.args.get('hair_image_url')

    if not age or not gender or not face_image_url or not hair_image_url:
        return jsonify({'error': 'Missing required parameters'}), 400

    try:
        # Use the Gradio client to make a prediction
        result = client.predict(
            age=age,
            gender=gender,
            face_image_pred=handle_file(face_image_url),
            hair_image_pred=handle_file(hair_image_url),
            api_name="/predict"
        )

        return jsonify({'result': result}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
