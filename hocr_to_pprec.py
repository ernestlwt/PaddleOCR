import os
import glob
import json

import cv2

from bs4 import BeautifulSoup


# def extract_hocr_bboxes(hocr_file, output_file):
#     with open(hocr_file, 'r', encoding='utf-8') as f:
#         soup = BeautifulSoup(f, 'html.parser')

#     with open(output_file, 'w', encoding='utf-8') as out:
#         for word in soup.find_all('span', class_='ocrx_word'):
#             text = word.get_text(strip=True)
#             title = word.get('title')
#             if text and title and 'bbox' in title:
#                 bbox_part = title.split(';')[0]  # e.g., 'bbox 100 200 150 220'
#                 coords = bbox_part.replace('bbox', '').strip()
#                 x1, y1, x2, y2 = map(int, coords.split())
#                 # out.write(f'Text: "{text}"\nBounding box: ({x1}, {y1}, {x2}, {y2})\n\n')
#                 # 377,117,463,117,465,130,378,130,Genaxis Theatre
#                 out.write("{},{},{},{},{},{},{},{},{}\n".format(x1,y1,x2,y1,x1,y2,x2,y2,text))

def get_filename_without_extension(file_path):
    filename_with_extension = os.path.basename(file_path)
    filename_without_extension = os.path.splitext(filename_with_extension)[0]
    return filename_without_extension

def hocr_to_pprec(image_folder, hocr_folder, annotation_filepath, output_folder):
    image_filepaths = glob.glob("{}/*.jpg".format(image_folder))

    annotations_contents = ""

    image_count = 0
    for image_filepath in image_filepaths:
        filename = get_filename_without_extension(image_filepath)
        # check hocr file exist
        hocr_filepath = "{}/{}.hocr".format(hocr_folder, filename)
        if not os.path.exists(hocr_filepath):
            print("HOCR file does not exist for image")
            exit()

        image = cv2.imread(image_filepath)

        # read hocr
        with open(hocr_filepath, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')

        word_count = 0
        for word in soup.find_all('span', class_='ocrx_word'):
            text = word.get_text(strip=True)
            title = word.get('title')
            if text and title and 'bbox' in title:
                bbox_part = title.split(';')[0]  # e.g., 'bbox 100 200 150 220'
                coords = bbox_part.replace('bbox', '').strip()
                x1, y1, x2, y2 = map(int, coords.split())
                # out.write(f'Text: "{text}"\nBounding box: ({x1}, {y1}, {x2}, {y2})\n\n')
                # 377,117,463,117,465,130,378,130,Genaxis Theatre
                cropped_image = image[y1:y2, x1:x2]
                output_image_filepath = "{}/{}_{}.jpg".format(output_folder, filename, word_count)
                cv2.imwrite(output_image_filepath, cropped_image)
                word_count += 1
                annotations_contents += output_image_filepath + "\t" + text + "\n"
        image_count += 1
        if image_count > 10:
            break

    with open(annotation_filepath, "w") as f:
        f.write(annotations_contents)

hocr_to_pprec("data/ao/images/train", "data/ao/hocr", "data/ao_rec/train.txt", "data/ao_rec/images/train")
# hocr_to_pprec("data/ao/images/test", "data/ao/hocr", "data/ao_rec/test.txt", "data/ao_rec/images/test")
