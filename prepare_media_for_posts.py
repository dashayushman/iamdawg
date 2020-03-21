import json
import ntpath
from pathlib import Path
import glob, os
import cv2
from PIL import ImageFont, Image, ImageDraw
from tqdm import tqdm
from random import shuffle
import numpy as np

import random

random.seed(42)

fontpath = "./Helvetica.ttc"
font = ImageFont.truetype(fontpath, 32)

def prepare_image(image_path, text):
    #path = './data/3888471.jpg'

    # Reading an image in grayscale mode
    image = cv2.imread(image_path, 1)

    r = 1080.0 / image.shape[1]
    dim = (1080, int(image.shape[0] * r))


    # perform the actual resizing of the image and show it
    resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)


    box_x =  int(resized.shape[0] * 0.90)
    box_y = 0
    print(resized.shape[0], box_x, box_y)
    #resized = cv2.rectangle(resized, (0, box_x), (1080, resized.shape[1]),
    #                        (255, 255, 255), -1)

    resized = cv2.rectangle(resized, (0, box_x), (resized.shape[1], resized.shape[0]),
                            (255, 255, 255), -1)

    #text = "I don't like morning people, or mornings, or people."
    #print("text_len", len(text))
    # setup text
    #font = cv2.FONT_HERSHEY_DUPLEX
    # get boundary of this text
    #textsize = cv2.getTextSize(text, font, 1, 2)[0]
    textsize = font.getsize(text)
    # get coords based on boundary
    textX = (resized.shape[1] - textsize[0]) // 2
    textY = (resized.shape[0] + textsize[1]) // 2 + (box_x // 2) - (textsize[1])

    #print(resized.shape[1], textsize[0])
    #print(resized.shape[0], textsize[1])
    # add text centered on image




    img_pil = Image.fromarray(resized)
    draw = ImageDraw.Draw(img_pil)

    draw.text((textX, textY), text, font=font, fill=(0, 0, 0))
    img = np.array(img_pil)

    #cv2.putText(resized, text, (textX, textY ), font, 1, (0, 0, 0), 2, lineType=cv2.LINE_AA, font_height=60)
    return img


def clean_caption_text(caption_text):
    caption_text = caption_text.replace("—", "-")


def prepare_description(caption_text, hashtags, metadata):

    description = f"{caption_text}\n.\n.\n.\nPC: {metadata['photographer']}\n{metadata['photo_url']}"
    description += "\n." * 3
    description += f"\n{hashtags}"
    return description

image_dir = Path("/Users/dash/Pictures/iamdawg/data")
metadata_dir = Path("/Users/dash/Pictures/iamdawg/metadata")
captions_path = Path("captions.txt")
hashtags_path = Path("hashtags.txt")
output_dir = Path("./pics")
stories_dir = Path("./stories")

caption_th = 65
hashtags = open(str(hashtags_path), "r").read().strip()

all_images = []

print("getting all files")
for file in tqdm(glob.glob(str(image_dir / "*.jpg"))):
    all_images.append(image_dir / file)
    print(image_dir / file)

print("getting all captions")
all_captions = [line.strip() for line in open(str(captions_path), "r").readlines()]
shuffle(all_captions)

print("preparing all images")

shuffle(all_images)

for image_id, image_file in tqdm(enumerate(all_images)):
    file_name = ntpath.basename(image_file)
    file_name = file_name.split(".")[0] + ".json"
    metadata_path = metadata_dir / file_name

    metadata = json.load(open(str(metadata_path), "r"))

    if all_captions:
        while all_captions:
            selected_captions = all_captions.pop()
            if len(selected_captions) > caption_th:
                continue
            else:

                description = prepare_description(selected_captions, hashtags, metadata)
                prepared_image = prepare_image(str(image_file), selected_captions)

                output_image_name = f"{image_id}-{image_id}.jpg"
                description_file_name = f"{image_id}.txt"

                if (prepared_image.shape[0] / prepared_image.shape[1]) > 1.0:
                    print(prepared_image.shape)
                    print("pushing to stories")
                    image_output_path = stories_dir / output_image_name
                    desc_output_path = stories_dir / description_file_name
                    cv2.imwrite(str(image_output_path), prepared_image)
                    with open(str(desc_output_path), "w") as f:
                        f.write(description)
                        break

                image_output_path = output_dir / output_image_name
                desc_output_path = output_dir / description_file_name

                cv2.imwrite(str(image_output_path), prepared_image)
                with open(str(desc_output_path), "w") as f:
                    f.write(description)
                break
    else:
        break