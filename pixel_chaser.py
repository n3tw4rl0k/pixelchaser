import os
import cv2
import time
import random
import argparse
import threading
import keyboard
import pyautogui
import numpy as np
import pygetwindow as gw
from logger import logger
from PIL import Image, ImageGrab
from pystray import Icon, Menu, MenuItem

__version__ = '1.0.0'


class GameAutomator:
    def __init__(self, game_window_title, classifier_path, key_to_press='=', detection_interval=20,
                 take_screenshots=False):
        self.game_window_title = game_window_title
        self.classifier = cv2.CascadeClassifier(classifier_path)
        self.key_to_press = key_to_press
        self.detection_interval = detection_interval
        keyboard.add_hotkey('ctrl+shift+p', self.stop)
        self.running = True
        self.take_screen = take_screenshots
    
    def stop(self):
        logger.info("Hotkey detected, stopping...")
        self.running = False
    
    def is_game_window_active(self):
        try:
            window = gw.getWindowsWithTitle(self.game_window_title)[0]
            if window.isActive and window.visible:
                logger.info(f'{self.game_window_title} is active and visible.')
                return True
            else:
                logger.info(f'{self.game_window_title} is not active or not visible.')
                return False
        except IndexError:
            logger.info(f'{self.game_window_title} is not running.')
            return False
    
    def press_key(self):
        logger.info(f'Pressing key: {self.key_to_press}')
        pyautogui.press(self.key_to_press)
    
    def detect_object(self, grayscale_image, original_image):
        objects = self.classifier.detectMultiScale(grayscale_image, scaleFactor=1.1, minNeighbors=5)
        if len(objects) != 0:
            logger.info("Object detected.")
            if self.take_screen:
                for (x, y, w, h) in objects:
                    cv2.rectangle(original_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.imwrite(os.path.join('screenshots', f'{time.time()}.png'), original_image)
            return True, objects
        else:
            logger.info("No object detected.")
            return False, None
    
    @staticmethod
    def move_and_click(object_position):
        x, y, w, h = object_position
        center_x = x + w // 2
        center_y = y + h // 2
        logger.info(f'Moving mouse to position: {center_x}, {center_y}')
        pyautogui.moveTo(center_x, center_y, duration=0.6)
        logger.info("Right click.")
        pyautogui.click(button='right')
    
    def run(self):
        while self.running:
            if not self.is_game_window_active():
                time.sleep(0.1)
                continue
            
            self.press_key()
            start_time = time.time()
            
            while time.time() - start_time < self.detection_interval:
                try:
                    image = ImageGrab.grab()
                    original_image = np.array(image)
                    grayscale_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
                    
                    detected, objects = self.detect_object(grayscale_image, original_image)
                    
                    if detected:
                        for object_position in objects:
                            self.move_and_click(object_position)
                            time.sleep(1 + random.random())
                        break
                except Exception as e:
                    logger.error(f"Error during detection: {e}")
                    break


class Application:
    def __init__(self):
        self.game_automator = None
        self.icon = None
        parser = argparse.ArgumentParser(description='Game Automator Script')
        parser.add_argument('--game_window_title', default='GameName', help='Name of the game window to detect.',
                            required=True)
        parser.add_argument('--classifier_path', default='cascade.xml', help='Path to the classifier xml.')
        parser.add_argument('--detection_interval', type=int, default=25,
                            help='Interval in seconds for object detection.')
        
        self.args = parser.parse_args()
    
    def start_automation(self):
        try:
            self.game_automator = GameAutomator(
                game_window_title=self.args.game_window_title,
                classifier_path=self.args.classifier_path,
                detection_interval=self.args.detection_interval
            )
            self.game_automator.run()
        except Exception as e:
            logger.error(f'Error starting fishing automation: {e}')
            raise Exception(e)
    
    def on_start(self, icon, item):
        threading.Thread(target=self.start_automation).start()
    
    def on_stop(self, icon, item):
        if self.game_automator:
            self.game_automator.stop()
    
    def run(self):
        image = Image.open('robot.png')
        menu = Menu(
            MenuItem('Start', self.on_start),
            MenuItem('Stop', self.on_stop)
        )
        self.icon = Icon('MyApp', image, 'MyApp', menu)
        self.icon.run()


if __name__ == "__main__":
    app = Application()
    app.run()
