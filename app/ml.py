from flask import Blueprint, request, jsonify
import numpy as np
from PIL import Image
import io
import tensorflow as tf

# Create a Blueprint for our AI functions
ml_bp = Blueprint('ml', __name__)

# Load the pre-trained model (do this once on startup)
try:
    model = tf.keras.models.load_model('mnist_model.h5')
except IOError:
    model = None

def preprocess_image(image_data):
    """Converts the canvas image data to a format the model can understand."""
    # The image data is a base64 string, remove the header
    image_data = image_data.split(',')[-1]
    
    # Decode the base64 string and open it as an image
    image = Image.open(io.BytesIO(io.base64.b64decode(image_data)))
    
    # The model expects a 28x28 grayscale image. 
    # The canvas is 280x280, so we resize it.
    image = image.resize((28, 28))
    
    # Convert to grayscale
    image = image.convert('L')
    
    # Convert image to numpy array and normalize
    image_np = np.array(image)
    image_np = image_np / 255.0
    
    # The model expects a batch of images, so we add a dimension
    return np.expand_dims(image_np, axis=0)

@ml_bp.route('/predict', methods=['POST'])
def predict():
    """Receives image data from the canvas and returns a prediction."""
    if not model:
        return jsonify({'error': 'Model not loaded. Did you run train_model.py?'}), 500

    data = request.get_json()
    if 'image' not in data:
        return jsonify({'error': 'No image data provided'}), 400

    try:
        # Preprocess the image
        processed_image = preprocess_image(data['image'])
        
        # Make a prediction
        prediction = model.predict(processed_image)
        
        # Get the predicted digit (the one with the highest probability)
        predicted_digit = int(np.argmax(prediction))
        
        return jsonify({'prediction': predicted_digit})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
