import os
import argparse
from logger import logger
from PIL import Image, ImageOps

__version__ = '1.0.0'


def rotate_image(image, angle):
    return image.rotate(angle)


def tint_image(image, color, factor):
    try:
        image_rgb = image.convert('RGB')
        alpha = image.split()[3] if image.mode == 'RGBA' else None
        
        colored_image = ImageOps.colorize(image_rgb.convert('L'), '#000000', color)
        blended_image = Image.blend(image_rgb, colored_image, factor)
        
        if alpha:
            blended_image.putalpha(alpha)
        return blended_image
    except Exception as err:
        logger.error(f'error occured while tinting image: {err}')


def process_images(input_folder, output_folder, tint_colors, rotation_angles, tint_strength):
    if not os.path.exists(output_folder):
        try:
            os.makedirs(output_folder)
            logger.info(f'directory created: {output_folder}')
        except Exception as err:
            logger.info(f'directory creation failed: {err}')

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.jpg', '.png')):
            img_path = os.path.join(input_folder, filename)
            
            try:
                with Image.open(img_path) as img:
                    for angle in rotation_angles:
                        rotated_img = rotate_image(img, angle)
                        rotated_img.save(os.path.join(output_folder, f'rotated_{angle}_{filename}'))
                        logger.info(f'rotated image: {img_path}')
                    
                    for color in tint_colors:
                        tinted_img = tint_image(img, color, tint_strength)
                        tinted_img.save(os.path.join(output_folder, f'tinted_{color[1:]}_{filename}'))
                        logger.info(f'tinted image: {img_path}')
                        
            except Exception as err:
                logger.error(f'image processing failed: {err}')
                

def generate_negative_description_file():
    list_files = os.listdir('screenshots_negative_augmented')
    try:
        with open('negative_aug.txt', 'w') as f:
            for fn in list_files:
                f.write('screenshots_negative_augmented/' + fn + '\n')
                logger.info(f'added image - {fn} - to negative image list')
                
    except Exception as err:
        logger.info(f'error while creating the negative images description list: {err}')


def main():
    parser = argparse.ArgumentParser(description='Image Augmentation Script')
    
    parser.add_argument('--action', choices=['positive-images', 'negative-images', 'all-images'], default=None,
                        help='Specify which images to augment')
    
    parser.add_argument('--generate-description', action='store_true',
                        help='Generate the negative description file')
    parser.add_argument('--tint_colors', nargs='+', default=['#ff0000', '#00ff00', '#0000ff'],
                        help='List of tint colors')
    parser.add_argument('--rotation_angles', nargs='+', type=int, default=[90, 180, 270], help='Angles for rotation')
    parser.add_argument('--tint_strength', type=float, default=0.35, help='Strength for tinting (between 0 and 1)')
    
    args = parser.parse_args()
    
    if not args.action and not args.generate_description:
        parser.print_help()
        return
    
    if args.action in ['positive-images', 'all-images']:
        process_images('screenshots_positive', 'screenshots_positive_augmented', args.tint_colors, args.rotation_angles,
                       args.tint_strength)
    
    if args.action in ['negative-images', 'all-images']:
        process_images('screenshots_negative', 'screenshots_negative_augmented', args.tint_colors, args.rotation_angles,
                       args.tint_strength)
    
    if args.generate_description:
        generate_negative_description_file()


if __name__ == '__main__':
    main()
