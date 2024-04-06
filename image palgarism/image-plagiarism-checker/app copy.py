from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
import os
from src.preprocessing.preprocess import preprocess_image
from src.feature_extraction.extract_features import extract_features
from src.similarity.compare import compare_images

# Define the path to the 'templates' directory and uploads directory
template_dir = os.path.abspath('./src/web_interface/templates')
UPLOAD_FOLDER = os.path.abspath('./uploads')

# Ensure the uploads directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__, template_folder=template_dir)

# Configuration
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    """Check if the file has one of the allowed extensions."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Render the upload form as the index page."""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle image uploads and plagiarism checking."""
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '' or not allowed_file(file.filename):
        return redirect(request.url)
    
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)  # Save the uploaded file

    try:
        processed_img = preprocess_image(file_path)  # Process the uploaded image
        features = extract_features(processed_img)  # Extract features from processed image
        # Note: You need to define how you get 'other_features' for comparison
        other_features = ...  # This should be replaced with actual feature loading logic
        similarity_score = compare_images(features, other_features)  # Compare features
    except Exception as e:
        print(e)  # For debugging purposes, consider logging this error as well
        similarity_score = "Error processing image"
    finally:
        os.remove(file_path)  # Cleanup the uploaded file after processing

    # Pass the similarity score to the results template
    return render_template('results.html', score=similarity_score)

if __name__ == '__main__':
    app.run(debug=True)
