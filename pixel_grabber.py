import os
import sys
import time
import argparse
from PIL import ImageGrab
from logger import logger
from pynput import keyboard

__version__ = '1.0.0'


positive_directory = 'screenshots_positive'
negative_directory = 'screenshots_negative'

if not os.path.exists(positive_directory):
    try:
        os.makedirs(positive_directory)
        
    except Exception as err:
        logger.error(f'Error occurred when trying to make dir: {err}')


if not os.path.exists(negative_directory):
    try:
        os.makedirs(negative_directory)
        
    except Exception as err:
        logger.error(f'Error occurred when trying to make dir: {err}')


def take_screenshot(save_directory):
    timestamp = int(time.time())
    save_path = os.path.join(save_directory, f'ss_{timestamp}.png')
    
    try:
        screenshot = ImageGrab.grab()
        screenshot.save(save_path)
        logger.info(f'Screenshot saved to {save_path}')
        
    except Exception as ss_err:
        logger.error(f'Error occurred when trying to save screenshot: {ss_err}')


def main():
    parser = argparse.ArgumentParser(description='Image Screen Grabber For Classifier')
    parser.add_argument('--positive-hotkey', default='7', dest='positive_key',
                        help="Hotkey to capture positive screenshots")
    parser.add_argument('--negative-hotkey', default='8', dest='negative_key',
                        help="Hotkey to capture negative screenshots")
    parser.add_argument('--exit-hotkey', default='9', dest='exit_key',
                        help="Hotkey to exit the script")
    args = parser.parse_args()
    
    def on_key_release(key):
        try:
            if key.char == args.positive_key:
                take_screenshot(positive_directory)
            elif key.char == args.negative_key:
                take_screenshot(negative_directory)
            elif key.char == args.exit_key:
                logger.info("Exiting script...")
                sys.exit(0)
        except Exception as key_err:
            logger.error(f'error occured when pressing a key {err}')
    
    logger.info(
        f"Started monitoring for screenshots. Press '{args.positive_key}' for positive, '{args.negative_key}' for negative, and '{args.exit_key}' to exit.")
    
    with keyboard.Listener(on_release=on_key_release) as listener:
        listener.join()


if __name__ == '__main__':
    main()
