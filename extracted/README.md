# AI Trainer App

A mobile application developed in MIT App Inventor 2, designed as an AI-powered fitness training interface with intuitive navigation and interactive features.

## Features

- **AI-powered pose recognition**: Uses teachable machine models through the camera
- **Multiple pose training**: Support for 4 different poses with visual references
- **Configurable settings**: 
  - Adjustable hold time (0-3 seconds)
  - Audio feedback toggle
  - Custom teachable machine model URL
- **Real-time feedback**: Audio and visual cues when pose match reaches 50%
- **Training results tracking**: View and clear past training sessions

## Screens

1. **Main Screen (Screen1)**
   - Three navigation buttons: Start Training, Settings, and View Results
   - Clean user interface with a blue background

2. **Settings Screen (Screen2)**
   - Model URL input field
   - Audio feedback toggle switch
   - Hold time selector (0, 1, 2, or 3 seconds)
   - Pose image selection (4 poses)
   - Save settings button

3. **Training Screen (Screen3)**
   - Camera view for pose recognition
   - Current and next pose display
   - Pose match percentage indicator
   - Hold time counter
   - Start/Stop control and pose navigation buttons

4. **Results Screen (Screen4)**
   - Last session date, duration, and poses completed
   - Option to clear results

## How to Use

1. **Setup**:
   - Go to Settings and input your teachable machine model URL
   - Set your preferred hold time (0-3 seconds)
   - Toggle audio feedback on/off
   - Select reference images for each pose

2. **Training**:
   - Start a training session from the main screen
   - The app will show the current pose to match
   - Position yourself to match the pose (aim for >50% match)
   - Hold the pose for the configured duration
   - When successful, the app plays a sound and advances to the next pose

3. **Review**:
   - Check your training results in the Results screen
   - View session date, duration, and number of poses completed

## Technical Details

- Built with MIT App Inventor 2
- Uses TinyDB for persistent storage of settings and results
- Implements camera integration for pose capture
- Compatible with teachable machine pose models