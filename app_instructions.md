# AI Trainer App - MIT App Inventor 2 Instructions

## How to Recreate This App from Scratch

If you prefer to build the app from scratch rather than importing the .aia file, follow these step-by-step instructions:

### Step 1: Create a New Project
1. Go to [MIT App Inventor](https://appinventor.mit.edu/)
2. Click "Create Apps!" to go to the MIT App Inventor environment
3. Sign in with your Google account
4. From the Projects menu, select "Start New Project"
5. Name your project "AITrainer"

### Step 2: Design the User Interface
1. Set the Screen properties:
   - BackgroundColor: Blue (#2196F3)
   - ScreenOrientation: Portrait
   - Title: "AI Trainer"

2. Add a VerticalArrangement:
   - Width: Fill parent
   - Height: Fill parent
   - AlignHorizontal: Center
   - AlignVertical: Center

3. Add a Label to the VerticalArrangement:
   - Text: "AI Trainer"
   - TextColor: White
   - FontSize: 24
   - FontBold: checked
   - Width: Fill parent
   - Height: Automatic
   - TextAlignment: Center
   - Margins: Top (20), Bottom (50)

4. Add three Button components to the VerticalArrangement:
   - Button1:
     - Text: "START TRAINING"
     - Width: 80% 
     - Height: Automatic
     - BackgroundColor: White
     - TextColor: Black
     - FontBold: checked
     - Shape: rounded (default)
     - Margins: Bottom (20)
   
   - Button2:
     - Text: "SETTINGS"
     - Width: 80% 
     - Height: Automatic
     - BackgroundColor: White
     - TextColor: Black
     - FontBold: checked
     - Shape: rounded (default)
     - Margins: Bottom (20)
   
   - Button3:
     - Text: "VIEW RESULTS"
     - Width: 80% 
     - Height: Automatic
     - BackgroundColor: White
     - TextColor: Black
     - FontBold: checked
     - Shape: rounded (default)

### Step 3: Add Basic Functionality

1. Click on the "Blocks" button in the top right corner to switch to the Blocks Editor

2. Add event handlers for each button:
   - For Button1 (START TRAINING):
     - When Button1.Click: show a notification "Starting Training Mode..."
   
   - For Button2 (SETTINGS):
     - When Button2.Click: show a notification "Opening Settings..."
   
   - For Button3 (VIEW RESULTS):
     - When Button3.Click: show a notification "Viewing Results..."

3. To add these blocks:
   - In the left panel, click on the button name (e.g., "Button1")
   - Find and drag the "when Button1.Click do" block to the workspace
   - In the left panel, click on "Notifier"
   - Drag the "call Notifier1.ShowAlert" block inside the Button click block
   - Add a text block with the appropriate message

### Step 4: Test Your App
1. Click on "Connect" in the top menu
2. Choose "AI Companion" 
3. Scan the QR code with the MIT AI2 Companion app on your device
4. Test all three buttons to ensure they show the correct notifications

### Step 5: Save and Export Your Project
1. From the Projects menu, select "Save Project"
2. To create an .aia file that you can share with others, go to Projects menu and select "Export project (.aia) to my computer"

## Next Development Steps

After completing the basic UI, you can continue development by:

1. Creating additional screens for Training, Settings, and Results
2. Implementing navigation between screens
3. Adding functionality specific to each screen
4. Connecting to external data sources or APIs as needed