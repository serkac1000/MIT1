import os
import zipfile
import json
import subprocess
import shutil
import tempfile
import xml.etree.ElementTree as ET
from io import BytesIO

def process_aia_file(filepath, temp_dir):
    """
    Extract and analyze the AIA file to get project information
    
    Args:
        filepath: Path to the uploaded AIA file
        temp_dir: Temporary directory for extraction
        
    Returns:
        Dictionary containing project information
    """
    project_info = {
        "projectName": "",
        "components": [],
        "screens": [],
        "version": "",
        "filename": os.path.basename(filepath)
    }
    
    # Create extraction directory
    extract_dir = os.path.join(temp_dir, "extracted")
    os.makedirs(extract_dir, exist_ok=True)
    
    # Extract the AIA file (which is a ZIP file)
    with zipfile.ZipFile(filepath, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)
    
    # Get project name from project.properties
    props_path = os.path.join(extract_dir, "project.properties")
    if os.path.exists(props_path):
        with open(props_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith("name="):
                    project_info["projectName"] = line.split("=", 1)[1].strip()
                    break
    
    # Get screens and components information
    screens_dir = os.path.join(extract_dir, "src")
    if os.path.exists(screens_dir):
        for item in os.listdir(screens_dir):
            if os.path.isdir(os.path.join(screens_dir, item)):
                screen_name = item
                project_info["screens"].append(screen_name)
                
                # Parse screen1.scm file to get components
                scm_file = os.path.join(screens_dir, item, f"{screen_name}.scm")
                if os.path.exists(scm_file):
                    try:
                        with open(scm_file, 'r', encoding='utf-8') as f:
                            content = f.read()
                            # Simple parsing to identify component types
                            # This is a basic implementation; a more robust parser would be needed for production
                            component_types = set()
                            for line in content.split("\n"):
                                if "component" in line.lower() and "type" in line.lower():
                                    parts = line.split()
                                    for i, part in enumerate(parts):
                                        if part.lower() == "type":
                                            if i+1 < len(parts):
                                                component_type = parts[i+1].strip("\"',()[]")
                                                component_types.add(component_type)
                            
                            project_info["components"].extend(list(component_types))
                    except Exception as e:
                        print(f"Error parsing SCM file: {e}")
    
    # Get version from youngandroidproject/project.properties
    yap_path = os.path.join(extract_dir, "youngandroidproject", "project.properties")
    if os.path.exists(yap_path):
        with open(yap_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith("main="):
                    project_info["version"] = line.split("=", 1)[1].strip()
                    break
    
    # Deduplicate components
    project_info["components"] = list(set(project_info["components"]))
    
    return project_info

def compile_mit_project(aia_path, output_dir, project_data):
    """
    Compile the MIT App Inventor project to an APK
    
    Args:
        aia_path: Path to the AIA file
        output_dir: Directory to output the compiled APK
        project_data: Dictionary containing project information
        
    Returns:
        Path to the compiled APK file
    """
    # In a real implementation, this would interact with the Companion or
    # MIT App Inventor compilation services. For the sake of this implementation,
    # we'll simulate the compilation process.
    
    # Create workspace directory
    workspace_dir = os.path.join(output_dir, "workspace")
    os.makedirs(workspace_dir, exist_ok=True)
    
    # Extract the AIA file to the workspace
    with zipfile.ZipFile(aia_path, 'r') as zip_ref:
        zip_ref.extractall(workspace_dir)
    
    # Path to the output APK
    apk_path = os.path.join(output_dir, f"{project_data['projectName']}.apk")
    
    # In a real implementation, we would:
    # 1. Convert blocks to Java/Kotlin code
    # 2. Generate Android app structure
    # 3. Compile using Android SDK
    # 4. Sign the APK
    
    # For this example, we'll create a mock APK file
    # In a real implementation, you would use the official MIT App Inventor build server
    # or use a tool like Buildserver (https://github.com/mit-cml/appinventor-sources/tree/master/buildserver)
    
    # Create a simple dummy APK file (this is just for demonstration)
    # In a real implementation, you would use proper Android build tools
    with open(apk_path, 'wb') as f:
        dummy_apk = BytesIO()
        with zipfile.ZipFile(dummy_apk, 'w') as zip_ref:
            # Add a mock manifest file
            manifest_content = f"""<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="org.example.{project_data['projectName'].lower().replace(' ', '_')}">
    <application
        android:label="{project_data['projectName']}">
    </application>
</manifest>"""
            zip_ref.writestr("AndroidManifest.xml", manifest_content)
            
            # Add a mock classes.dex file
            zip_ref.writestr("classes.dex", b"DUMMY DEX FILE")
            
            # Add resources directory
            zip_ref.writestr("res/README", "Resources directory")
        
        dummy_apk.seek(0)
        f.write(dummy_apk.read())
    
    # In production, you would use something like this:
    # subprocess.run(["java", "-jar", "buildserver.jar", "--input", aia_path, "--output", apk_path])
    
    return apk_path
