from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()

# OCR.space API endpoint
API_URL = "https://api.ocr.space/parse/image"
API_KEY = "K82456287588957"  # Your provided API key

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    try:
        # Prepare the API request
        payload = {
            'apikey': API_KEY,
            'isOverlayRequired': False,
            'language': 'eng',
        }
        
        files = {
            'file': (file.filename, file.read(), file.content_type)
        }
        
        # Make the API request
        response = requests.post(API_URL, files=files, data=payload)
        result = response.json()
        
        # Extract the text from the response
        if result['IsErroredOnProcessing'] == False:
            extracted_text = result['ParsedResults'][0]['ParsedText']
            return jsonify({'text': extracted_text})
        else:
            return jsonify({'error': 'Error processing the image'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    app.run(debug=True)