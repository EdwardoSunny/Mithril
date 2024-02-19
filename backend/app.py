from flask import Flask, request, jsonify, send_file
from zipfile import ZipFile, is_zipfile
from flask_cors import CORS
from datetime import datetime
import populate_output_data
import shutil
import os

app = Flask(__name__)
CORS(app)

upload_directory = "user_data/"
output_directory = "pix2pix_data/output_data"


# This function checks that the zip file inputted will be the correct format (either images or 3 folders)
def validate_zip(file_stream):
    with ZipFile(file_stream) as zip_file:
        namelist = zip_file.namelist()
        dir_count = 0
        file_count = 0
        for name in namelist:
            if name.endswith("/"):
                dir_count += 1
            else:
                file_count += 1
                if not name.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp")):
                    return False, "ZIP contains non-image files."
        if dir_count == 3 and file_count == 0:
            return True, "ZIP contains exactly three folders."
        elif dir_count == 0 and file_count > 0:
            return True, "ZIP contains only image files."
        else:
            return False, "ZIP does not meet the criteria."


# This function takes the images from a dataset and checks if there are any
def process_files():
    populate_output_data.populate()
    return "Data Processed"


# Function to clear a directory
def clear_directory(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")


# Endpoint for Uploading a Zip File
@app.route("/upload", methods=["POST"])
def upload_zip():
    # Clears all the directories in the respective folders
    clear_directory(upload_directory)
    clear_directory(output_directory)
    # Checks if a file was even sent in thr request
    if "file" not in request.files:
        return jsonify({"message": "No file part"}), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"message": "No selected file"}), 400
    if file and is_zipfile(file):
        file.seek(0)  # Reset file pointer to the beginning
        valid, message = validate_zip(file)
        if not valid:
            return jsonify({"message": message}), 400
        # Add a directory to add the files
        if not os.path.exists(upload_directory):
            os.makedirs(upload_directory)
        with ZipFile(file) as zip_ref:
            zip_ref.extractall(upload_directory)
        # Process the ZIP file
        process_files()
        # Return a success message
        return jsonify({"message": "File has been processed"}), 202
    else:
        return (
            jsonify({"message": "Invalid file type. Only ZIP files are allowed."}),
            400,
        )


@app.route('/images/<path:image_name>')
def get_image(image_name):
    return send_from_directory('path_to_your_image_folder', image_name)



if __name__ == "__main__":
    app.run(debug=True)
