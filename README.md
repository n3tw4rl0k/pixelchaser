# Simple Game Automation

## Introduction

This project provides an example of using OpenCV for game automation. While it serves primarily for educational purposes, the technique used is "undetectable" by standard detection methods, offering potential for broader applications in gaming. For instance, it could be adapted to create a bot for basically any game on pc.

In essence, the provided code identifies specific patterns on the screen (based on the training) and simulates click actions on them.

## Prerequisites

1. Download and install OpenCV from [here](https://github.com/opencv/opencv/releases).

## Steps to Set Up

1. **Capture Screenshots**: 
   - Run `pixel_grabber.py` to take screenshots of the game. You will need both "positive" screenshots (those containing elements you want the bot to click on) and "negative" screenshots (which do not contain these elements).

2. **Annotate Positive Screenshots**: 
   - This step is crucial. The annotations help the model learn what to look for. For this, you can use the `opencv_annotation` executable found in the OpenCV installation directory (typically under `opencv/build/x64/vc15/bin`).
   - Command: 
     ```
     path_to_opencv_annotation.exe --annotations=pos.txt --images=path_to_positive_screenshots/
     ```

3. **Prepare and Augment Negative Screenshots with `pixel_classifier_util.py`**:
   - Run `pixel_classifier_util.py` to prepare and augment the negative screenshots. This tool offers image augmentation features like rotation, tinting, etc.
   - Command:
     ```
     python pixel_classifier_util.py --action=negative-images --generate-description
     ```
   - Additional arguments can be provided for tint colors, rotation angles, tint strength, etc.

4. **Train Your Model**:
   - Use the positive and negative screenshots to train your model. The better the training, the more accurate your bot will be.

5. **Deploy Your Bot with `pixel_chaser.py`**:
   - Once the model is trained, run `pixel_chaser.py` with the game's name as an argument.
   - Command:
     ```
     python pixel_chaser.py --name=YourGameName
     ```
   - The script will use the trained classifier to detect patterns on the game screen and click on them.
   - Of course, you can follow this pattern and build more complex bots.

## Note

Always remember that while this is an educational demonstration, using bots or any form of automation can violate the terms of service of most games. Ensure you are compliant with any terms and conditions before using such tools on any platform.
