import os
import json
import zipfile
import shutil
import tempfile
import traceback
from io import BytesIO
from flask import Flask, request, render_template, jsonify, send_file
from werkzeug.utils import secure_filename
from utils.compiler import process_aia_file, compile_mit_project

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max upload size
app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()

ALLOWED_EXTENSIONS = {'aia'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    if not allowed_file(file.filename):
        return jsonify({"error": "Only .aia files are allowed"}), 400
    
    try:
        # Create a temporary directory for processing
        temp_dir = tempfile.mkdtemp(dir=app.config['UPLOAD_FOLDER'])
        
        # Save the uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(temp_dir, filename)
        file.save(filepath)
        
        # Process the AIA file
        project_info = process_aia_file(filepath, temp_dir)
        
        # Return project info to the client
        return jsonify({"success": True, "message": "File uploaded successfully", "project_info": project_info})
    
    except Exception as e:
        error_message = str(e)
        traceback_str = traceback.format_exc()
        return jsonify({"error": error_message, "traceback": traceback_str}), 500
    
    finally:
        # Always clean up temporary directory
        if 'temp_dir' in locals():
            try:
                shutil.rmtree(temp_dir)
            except Exception:
                pass

@app.route('/compile', methods=['POST'])
def compile_project():
    data = request.json
    
    if not data or 'projectName' not in data:
        return jsonify({"error": "Missing project information"}), 400
    
    try:
        # Create a temporary directory for compilation
        temp_dir = tempfile.mkdtemp(dir=app.config['UPLOAD_FOLDER'])
        
        # Get the uploaded file from the previous step
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(data['filename']))
        
        # Compile the project
        apk_path = compile_mit_project(file_path, temp_dir, data)
        
        # Create a BytesIO object to store the APK file
        apk_buffer = BytesIO()
        
        # Read the APK file and write it to the buffer
        with open(apk_path, 'rb') as f:
            apk_buffer.write(f.read())
        
        # Reset the buffer position to the beginning
        apk_buffer.seek(0)
        
        # Generate filename for download
        download_filename = f"{data['projectName']}.apk"
        
        # Return the APK file
        return send_file(
            apk_buffer,
            mimetype='application/vnd.android.package-archive',
            as_attachment=True,
            download_name=download_filename
        )
    
    except Exception as e:
        error_message = str(e)
        traceback_str = traceback.format_exc()
        return jsonify({"error": error_message, "traceback": traceback_str}), 500
    
    finally:
        # Always clean up temporary files
        if 'temp_dir' in locals():
            try:
                shutil.rmtree(temp_dir)
            except Exception:
                pass

@app.route('/project-info', methods=['POST'])
def get_project_info():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    if not allowed_file(file.filename):
        return jsonify({"error": "Only .aia files are allowed"}), 400
    
    try:
        # Create a temporary directory for processing
        temp_dir = tempfile.mkdtemp(dir=app.config['UPLOAD_FOLDER'])
        
        # Save the uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(temp_dir, filename)
        file.save(filepath)
        
        # Process the AIA file
        project_info = process_aia_file(filepath, temp_dir)
        
        return jsonify({"success": True, "project_info": project_info})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    finally:
        # Clean up temporary directory
        if 'temp_dir' in locals():
            try:
                shutil.rmtree(temp_dir)
            except Exception:
                pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
