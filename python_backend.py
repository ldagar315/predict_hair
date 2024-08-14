from flask import Flask, request, jsonify
from gradio_client import Client, handle_file

app = Flask(__name__)

client = Client("https://a9dcb184b0b833f4e6.gradio.live")

@app.route('/predict_hair', methods=['POST', 'GET'])
def predict_hair():
    if request.method == 'GET':
        hair_image_url = request.args.get('hair_image_url')
    else:
        if 'hair_image_url' not in request.json:
            return jsonify({'error': 'No image URL provided'}), 400
        hair_image_url = request.json['hair_image_url']

    if not hair_image_url:
        return jsonify({'error': 'No image URL provided'}), 400

    try:
        result = client.predict(
            img_hair=handle_file(hair_image_url),
            api_name="/predict_hair"
        )
        print(result)
        return jsonify({'result': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
