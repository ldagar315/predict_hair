from flask import Flask, request, jsonify
from gradio_client import Client, handle_file

app = Flask(__name__)

# Initialize the Gradio client with your specified model
client = Client("https://7c52857bc931c54613.gradio.live")

@app.route('/predict', methods=['POST','GET'])
def predict():
    # Extract the required parameters from the incoming request
    data = request.args

    # Validate and retrieve the necessary parameters
    age = data.get('age')
    gender = data.get('gender')
    aqi = data.get('aqi')
    location = data.get('location')
    activity_lvl = data.get('activity_lvl')
    goal = data.get('goal')
    medical_cond = data.get('medical_cond')
    smoking_status = data.get('smoking_status')
    face_image_url = data.get('face_image_url')
    hair_image_url = data.get('hair_image_url')

    if not age or not gender or not aqi or not location or not goal or not activity_lvl or not medical_cond or not smoking_status or not face_image_url or not hair_image_url:
        return jsonify({'error': 'Missing required parameters'}), 400

    try:
        # Use the Gradio client to make a prediction
        result = client.predict(
            age=age,
            gender=gender,
            aqi = aqi, 
            location = location, 
            activity_lvl = activity_lvl,
            goal = goal, 
            medical_cond = medical_cond,
            smoking_status = smoking_status,
            face_image=handle_file(face_image_url),
            hair_image=handle_file(hair_image_url),
            api_name="/predict"
        )

        return jsonify({'result': result}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

