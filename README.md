# Computer Vision Visualizer

This application, built using the Streamlit library, is designed for various computer vision tasks. It offers a range of functionalities, including face recognition, hand recognition, finger counting, and the ability to capture images from video streams using specific hand gestures.

## Functionalities

### Face Mesh Detection
- Utilizes the FaceMesh model from the mediapipe library to detect and draw landmarks on faces in real-time video streams.

### Hand Detection
- Utilizes the Hands model from mediapipe to detect and draw landmarks on hands in real-time video streams.

### Finger Counting
- Implements a finger counting system by tracking hand landmarks and determining the number of fingers extended.

### Take Picture
- Allows the user to capture an image from the video stream by performing a specific hand gesture.

## Usage

To get started with the Computer Vision Visualizer, follow these steps:

1. Clone this repository:

   ```bash
   git clone https://github.com/sergiobriito/computer-vision.git

2. Install the required libraries:

   ```bash
   pip install -r requirements.txt

3. Run the application::

   ```bash
   streamlit run App.py

