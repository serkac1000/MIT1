# MIT App Inventor 2 Compiler

A web application that helps you compile MIT App Inventor 2 projects (.aia files) into Android APK files.

## Features

- Upload and analyze MIT App Inventor 2 project files (.aia)
- View project information including screens, components, and App Inventor version
- Compile projects to Android APK files
- Configure compilation options like target Android version
- Download compiled APK files

## Installation

### Prerequisites

- Python 3.6 or higher
- Flask

### Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/mit-app-inventor-compiler.git
   cd mit-app-inventor-compiler
   ```

2. Install dependencies:
   ```
   pip install flask
   ```

3. Run the application:
   ```
   python app.py
   ```

4. Access the web interface at http://localhost:5000

## Usage

1. Open the web interface in your browser
2. Click "Choose file" and select your .aia project file
3. Click "Upload Project" to analyze the file
4. Review the project information
5. Set compilation options
6. Click "Compile Project" to build the APK
7. Once compilation is complete, click "Download APK" to save the file

## Implementation Notes

This implementation provides a basic simulation of the compilation process. In a production environment, you would need to integrate with the official MIT App Inventor build server API or implement a full Android build chain.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- MIT App Inventor team for their amazing tool
- Contributors to the project
