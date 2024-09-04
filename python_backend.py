from flask import Flask, request, jsonify
from gradio_client import Client, handle_file
import google.generativeai as genai
import os


genai.configure(api_key= 'AIzaSyApz-2HGHovDuwzOPCQLqIEhMXNaYgXuyU')

model_json = genai.GenerativeModel('gemini-1.5-pro', 
                              generation_config= {
                                  "response_mime_type": "application/json"
                                  
                              })

model = genai.GenerativeModel('gemini-1.5-pro')
output = { "Monday" :
    {"fruits": {
        "first": { "name": "Apple", 
        "dosage" : "1 medium",
        "benefits": "Apple is good antioxidant that will help you to give sustained energy"}, 
        "second": {
            "name": "Banana",
            "dosage": "1 large",
            "benefits": "Banana contains Phosphorous which preserves your salt balance and gives you active energy throught the day"
        }
    }
     }, 
    "Tuesday" :{
     "fruits":{
         "first": { "name": "Mango", 
        "dosage" : "2 slices",
        "benefits": "Mango is good for the natural sugars present in mangos, such as fructose and glucose, provide a quick and sustained energy boost"},
         "second" : {"....."},
        

     }}}
app = Flask(__name__)

# Initialize the Gradio client with your specified model
client = Client("Lakshay1Dagar/facial_defect_detector")

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
            img_face = handle_file(face_image_url),
            img_hair = handle_file(hair_image_url),
            api_name="/predict"
        )

        face_pred = result[0]['label']
        hair_pred = result[1]['label']
        content = f''' You a game character that is expert nutritionist, You have to design weekly fruit consumption plan for the the main character
        that has the following stats. Chart a weekly plan in the format specified below. Choose fruits from the list below
        you can repeat the fruits as well and can suggest more than one fruit. Remember to make it personlised for the character based on the following stats
        age : {age}
        gender : {gender}
        aqi : {aqi}, consider this for the pollution severity
        location : {location}, consider this for the fruit availablity
        activity level : {activity_lvl}
        goal : {goal}
        medical condition : {medical_cond}, consider this for only for better recommnedations not for allergen / harm / side effects
        Smoking / Alcohol Consumption : {smoking_status}
        Defects on face : {face_pred} on face
        Hair Health : {hair_pred} 
        Use this JSON schema:
         FruitPlan = {output}
        Return a 'list[FruitPlan]'
        '''
        response = model_json.generate_content(content)

        return jsonify({'result': result[:2], 'gen_ai_response': response.text}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

