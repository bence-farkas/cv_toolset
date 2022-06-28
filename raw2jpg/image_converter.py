import os
import argparse
import rawpy
import cv2

parser = argparse.ArgumentParser()
parser.add_argument("--i", type=str, default=os.getcwd() ,help="Input image directory")
args = parser.parse_args()

images = os.listdir(args.i)
output_folder = os.path.join(args.i, "converted")
if not os.path.isdir(output_folder):
    os.makedirs(output_folder)

for image in images:
    if image.endswith(".CR2"):
        input_img_path = os.path.join(args.i, image)
        print("Reading: " + input_img_path)
        raw = rawpy.imread(input_img_path)
        rgb = raw.postprocess()  # a numpy RGB array
        out_img_path = os.path.join(output_folder, image[:-4] + ".jpg")
        out_image = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
        cv2.imwrite(out_img_path, out_image)
        print("Converted to: " + out_img_path)


