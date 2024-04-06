from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
import os
from src.preprocessing.preprocess import preprocess_image
from src.feature_extraction.extract_features import extract_features
from src.similarity.compare import compare_images

# Import your preprocessing, feature extraction, and comparison functions here

template_dir = os.path.abspath('./src/web_interface/templates')

app = Flask(__name__, template_folder=template_dir)

UPLOAD_FOLDER = os.path.abspath('./uploads/')
DATASET_FOLDER = os.path.abspath('./datasets/original/')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET'])
def index():
    """Render the upload form as the index page."""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle image uploads and plagiarism checking."""
    file = request.files.get('file')
    if file and file.filename:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Process the uploaded image
        processed_image = preprocess_image(filepath)
        uploaded_features = extract_features(processed_image)
        
        highest_similarity = 0
        similar_image_name = ""
        
        # Iterate through each image in the original dataset folder
        for image_file in os.listdir(DATASET_FOLDER):
            image_path = os.path.join(DATASET_FOLDER, image_file)
            # Preprocess the dataset image
            dataset_image = preprocess_image(image_path)
            # Extract features of the dataset image
            dataset_features = extract_features(dataset_image)
            # Compare features between uploaded and dataset image
            similarity = compare_images(uploaded_features, dataset_features)
            # Update highest similarity and store the most similar image name
            if similarity > highest_similarity:
                highest_similarity = similarity
                similar_image_name = image_file
        
        os.remove(filepath)  # Cleanup: remove the uploaded file after processing
        
        # Determine the result based on the highest similarity score
        if highest_similarity > 0.8:
            result = f"Potential Plagiarism Detected with {similar_image_name} (Similarity: {int(highest_similarity*100)}%)"
        else:
            result = f"No Plagiarism Detected with {similar_image_name} (Similarity: {int(highest_similarity*100)}%)"
        
        return render_template('results.html', result=result)
    else:
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
