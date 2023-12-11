from roboflow import Roboflow
from tqdm import tqdm
import json
import cv2
from circle import detect_circle
import argparse
from aruco import detect_aruco
from img_preproc import img_preprocess
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("--img_path", '-i',
                    type=str,
                    required=True,
                    help="Path to image.")
args = parser.parse_args()

def draw_points(img, bbox, center_x, center_y):

    X = bbox[0]
    Y = bbox[1]
    W = bbox[2]
    H = bbox[3]

    point_size = 1
    point_color = (0, 0, 255) # red
    thickness = 6

    # 要畫的點座標
    if center_x != 0 and center_y != 0:
        point = (int(X-(W/2)) + center_x, int(Y-(H/2)) + center_y)
    else:
        point = (int(X), int(Y))

    cv2.circle(img, point, point_size, point_color, thickness)

    return img, point

# load pre-trained model
rf = Roboflow(api_key="q8MrumMuB6fU2rqctKz4")
project = rf.workspace().project("poolgame")
model = project.version(6).model

# img_path = args.img_path

img = cv2.imread(args.img_path)
img_after_proc_path = "./proc_img.png"
img_preprocess(img)

data = model.predict(img_after_proc_path, confidence=50, overlap=30).json()

with open('bbox.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)


points = []

# Iterating through the json list
for i, obj in enumerate(data['predictions']):

    # only detect the bbox in higher confidence
    if obj['confidence'] > 0.5:
        
        print(obj['class'])

        x = int(obj['x'])
        y = int(obj['y'])
        width = int(obj['width'])
        height = int(obj['height'])

        bbox = [x, y, width, height]
        
        # crop object from original image.
        crop_image = img[int(y-(height/2)):int(y+(height/2)), int(x-(width/2)):int(x+(width/2))]
        # cv2.imwrite(f'{i}.png', crop_image)
        
        # find circle from cropped image.
        center_x, center_y = detect_circle(crop_image)

        # draw center of circle in original image.
        img, point = draw_points(img, bbox, center_x, center_y)

        points.append([obj['class'], point])

# write points' coordinate and ball number into .txt file
with open('./points.txt', 'w') as fp:
    for item in points:
        # write each item on a new line
        fp.write("%s\n" % item)
        
img = detect_aruco(img)

# saved image
cv2.imwrite('output.png', img)

print('Done')