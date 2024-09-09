from flask import Flask, request, jsonify
from gradio_client import Client, handle_file
import google.generativeai as genai
import os
import json



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

def get_fruits_benefits(json_response):
  unique_fruits = []
  unique_fruits_json = []
  for i in json_response:
    for j in json_response[i]['fruits']:
      if json_response[i]['fruits'][j]['name'] not in unique_fruits:
        my_dict = {}
        unique_fruits.append(json_response[i]['fruits'][j]['name'])
        my_dict['fruit'] = json_response[i]['fruits'][j]['name']
        my_dict['benefit'] = json_response[i]['fruits'][j]['benefits']
        try :
          my_dict['image'] = fruit_images[json_response[i]['fruits'][j]['name']]
        except KeyError:
          continue
        unique_fruits_json.append(my_dict)
  return unique_fruits_json   

fruit_images = {
    'Apple' : 'https://firebasestorage.googleapis.com/v0/b/facial-gen-ai-fruit-recom.appspot.com/o/fruit_images%2Fred-apple-leaf-slice-white-background-29914331.jpg?alt=media&token=ba699af7-d101-48e2-a02a-90e8d2b7f48d',
    'Banana' : 'https://firebasestorage.googleapis.com/v0/b/facial-gen-ai-fruit-recom.appspot.com/o/fruit_images%2FBANANA-PDP.jpg_1723792764773.jpg?alt=media&token=258567ef-58b3-40ca-aa89-f5bdb0be0642',
    'Guava' : 'https://firebasestorage.googleapis.com/v0/b/facial-gen-ai-fruit-recom.appspot.com/o/fruit_images%2FGuvava.jpg?alt=media&token=561d9d28-65e7-4ffd-8c25-855e9eceb111',
    'Pear' : 'https://firebasestorage.googleapis.com/v0/b/facial-gen-ai-fruit-recom.appspot.com/o/fruit_images%2FIndianPear(Babugosha)-pdp.jpg_1724045690263.jpg?alt=media&token=7beceb25-24b6-4d73-8e5d-fc6e676a7d60',
    'Kiwi' : 'https://firebasestorage.googleapis.com/v0/b/facial-gen-ai-fruit-recom.appspot.com/o/fruit_images%2FKIWIGREEN-pdp.jpg_1723792814093.jpg?alt=media&token=abc40cca-ba9e-4ee3-82cd-d9e4a3edbf29',
    'Mango' : 'https://firebasestorage.googleapis.com/v0/b/facial-gen-ai-fruit-recom.appspot.com/o/fruit_images%2FMangoBanganapalli-PDP.jpg_1723792993796.jpg?alt=media&token=8728f207-306f-449c-b279-56c21c522365',
    'Papaya' : 'https://firebasestorage.googleapis.com/v0/b/facial-gen-ai-fruit-recom.appspot.com/o/fruit_images%2FPAPAYARIPE-pdp.jpg_1723792868072.jpg?alt=media&token=fadfaa71-a56d-4a1e-aa1d-3f2425669c8f',
    'Pomegranate' : 'https://firebasestorage.googleapis.com/v0/b/facial-gen-ai-fruit-recom.appspot.com/o/fruit_images%2FPOMEGRANATE-pdp.jpg_1723792901263.jpg?alt=media&token=8578e8cb-87af-4a8f-b0ad-f2fa33eb9718',
    'Watermelon' : 'https://firebasestorage.googleapis.com/v0/b/facial-gen-ai-fruit-recom.appspot.com/o/fruit_images%2FWATERMELON-pdp.jpg_1723792942607.jpg?alt=media&token=e0ac1ea0-1c47-4fcf-af2f-5a3c028cbe3d',
    'Avacado' : 'https://firebasestorage.googleapis.com/v0/b/facial-gen-ai-fruit-recom.appspot.com/o/fruit_images%2Favacado.jpg?alt=media&token=bc589e7f-1748-4bbc-bc10-395a69faa1ec',
    'Dragon Fruit' : 'https://firebasestorage.googleapis.com/v0/b/facial-gen-ai-fruit-recom.appspot.com/o/fruit_images%2Fdragon%20fruit.jpg?alt=media&token=cc997868-107e-45ee-a38b-0499efdb77ba',
    'Grapes' : 'https://firebasestorage.googleapis.com/v0/b/facial-gen-ai-fruit-recom.appspot.com/o/fruit_images%2Fgrapes.jpg?alt=media&token=05236b75-ee8c-442b-b5d9-f18af2a6b3c7',
    'Muskmelon' : 'https://firebasestorage.googleapis.com/v0/b/facial-gen-ai-fruit-recom.appspot.com/o/fruit_images%2Fmuskmelon.jpg?alt=media&token=b4988333-a270-4747-af1e-29b463533fd9',
    'Orange' : 'https://firebasestorage.googleapis.com/v0/b/facial-gen-ai-fruit-recom.appspot.com/o/fruit_images%2Forange.jpg?alt=media&token=a71d976a-d6ec-43cb-bfa7-6cd350f2c319',
    'Peach' : 'https://firebasestorage.googleapis.com/v0/b/facial-gen-ai-fruit-recom.appspot.com/o/fruit_images%2Fpeach.jpg?alt=media&token=834c9551-2154-46c3-981e-707c3a7da514',
    'Pineapple' : 'https://firebasestorage.googleapis.com/v0/b/facial-gen-ai-fruit-recom.appspot.com/o/fruit_images%2Fpineapple.jpg?alt=media&token=8571b9f4-084c-4a21-8aaf-053074289930',
    'Plum' : 'https://firebasestorage.googleapis.com/v0/b/facial-gen-ai-fruit-recom.appspot.com/o/fruit_images%2Fplum.jpg?alt=media&token=87c2928d-415a-4c52-b971-bda2f64555f8',
    'Berries (Mix)' : 'https://firebasestorage.googleapis.com/v0/b/facial-gen-ai-fruit-recom.appspot.com/o/fruit_images%2FBlackberry.jpg?alt=media&token=c9e1fcce-c307-416b-9e4c-2b1dfc22d464',
    'MuskMelon (Kharbooja)' : 'https://firebasestorage.googleapis.com/v0/b/facial-gen-ai-fruit-recom.appspot.com/o/fruit_images%2Fmuskmelon.jpg?alt=media&token=b4988333-a270-4747-af1e-29b463533fd9'
}

app = Flask(__name__)

# Initialize the Gradio client with your specified model
client = Client("Lakshay1Dagar/facial_defect_detector")

@app.route('/')
def running():
    return 'This is server is live and running'

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
        content = f''' You a game character that is expert nutritionist, You have to design a personalised weekly fruit consumption plan for the the main character
        with the following parameters. 
        age : {age}
        gender : {gender}
        aqi : {aqi}, consider this for the pollution severity
        location : {location}, consider this for the fruit availablity
        activity level : {activity_lvl}
        goal : {goal}
        medical condition : {medical_cond}, consider this for only for better recommnedations not for allergen / harm / side effects
        Smoking / Alcohol Consumption : {smoking_status}
        Defects on face : {face_pred} on face
        Hair Health : {hair_pred} on Norwood scale
        Output the result in this JSON schema:
         FruitPlan = {output}
        Return a tuple(FruitPlan)
        '''
        response = model_json.generate_content(content)
        json_response = json.loads(response.text)
        fruit_benefits = get_fruits_benefits(json_response)

        return jsonify({'result': result, 'gen_ai_response': json_response,'fruit_benefits':fruit_benefits}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

