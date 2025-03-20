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
    
    temp_dir = None
    
    try:
        # Create a temporary directory for processing
        temp_dir = tempfile.mkdtemp(dir=app.config['UPLOAD_FOLDER'])
        
        # Save the uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(temp_dir, filename)
        file.save(filepath)
        
        # Process the AIA file
        project_info = process_aia_file(filepath, temp_dir)
        
        # Important: Add the filename to the project_info for later reference
        project_info['filename'] = filename
        
        # Return project info to the client
        return jsonify({"success": True, "message": "File uploaded successfully", "project_info": project_info})
    
    except Exception as e:
        error_message = str(e)
        traceback_str = traceback.format_exc()
        return jsonify({"error": error_message, "traceback": traceback_str}), 500
    
    finally:
        # We don't clean up the temporary directory here anymore
        # so the file remains available for the compilation step
        # It will be cleaned up after the compilation or after a reasonable timeout
        pass

@app.route('/compile', methods=['POST'])
def compile_project():
    data = request.json
    
    if not data or 'projectName' not in data:
        return jsonify({"error": "Missing project information"}), 400
    
    if 'filename' not in data:
        return jsonify({"error": "Missing filename"}), 400
        
    temp_dir = None
    output_dir = None
    
    try:
        # Create a temporary directory for compilation
        temp_dir = tempfile.mkdtemp(dir=app.config['UPLOAD_FOLDER'])
        output_dir = tempfile.mkdtemp(dir=app.config['UPLOAD_FOLDER'])
        
        # Get the filename from the request data
        filename = secure_filename(data['filename'])
        
        # Search for uploaded file in the upload folder (from the previous upload step)
        file_path = None
        for root, dirs, files in os.walk(app.config['UPLOAD_FOLDER']):
            if filename in files:
                file_path = os.path.join(root, filename)
                break
        
        # If file not found, return an error
        if not file_path or not os.path.exists(file_path):
            return jsonify({"error": f"File {filename} not found. Please upload the file again."}), 404
        
        # Create project data object for compilation
        project_data = {
            "projectName": data.get('projectName', 'MIT_App'),
            "filename": filename
        }
        
        # Add other properties passed in the request
        if 'components' in data:
            project_data['components'] = data['components']
        if 'screens' in data:
            project_data['screens'] = data['screens']
        if 'version' in data:
            project_data['version'] = data['version']
            
        # Compile the project
        app.logger.info(f"Compiling project {filename} with data: {project_data}")
        apk_path = compile_mit_project(file_path, output_dir, project_data)
        
        if not os.path.exists(apk_path):
            return jsonify({"error": "Failed to generate APK file"}), 500
            
        # Create a BytesIO object to store the APK file
        apk_buffer = BytesIO()
        
        # Read the APK file and write it to the buffer
        with open(apk_path, 'rb') as f:
            apk_buffer.write(f.read())
        
        # Reset the buffer position to the beginning
        apk_buffer.seek(0)
        
        # Generate filename for download
        download_filename = f"{project_data['projectName']}.apk"
        
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
        if temp_dir and os.path.exists(temp_dir):
            try:
                shutil.rmtree(temp_dir)
            except Exception:
                pass
                
        if output_dir and os.path.exists(output_dir):
            try:
                shutil.rmtree(output_dir)
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
    
    temp_dir = None
    
    try:
        # Create a temporary directory for processing
        temp_dir = tempfile.mkdtemp(dir=app.config['UPLOAD_FOLDER'])
        
        # Save the uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(temp_dir, filename)
        file.save(filepath)
        
        # Process the AIA file
        project_info = process_aia_file(filepath, temp_dir)
        
        # Add filename to project info
        project_info['filename'] = filename
        
        return jsonify({"success": True, "project_info": project_info})
    
    except Exception as e:
        error_message = str(e)
        traceback_str = traceback.format_exc()
        return jsonify({"error": error_message, "traceback": traceback_str}), 500
    
    finally:
        # Clean up temporary directory
        if temp_dir and os.path.exists(temp_dir):
            try:
                shutil.rmtree(temp_dir)
            except Exception:
                pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
