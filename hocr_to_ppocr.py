import os
import glob
import json

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

def hocr_to_pp(image_folder, hocr_folder, annotation_filepath):
    image_filepaths = glob.glob("{}/*.jpg".format(image_folder))

    annotations_contents = ""

    for image_filepath in image_filepaths:
        filename = get_filename_without_extension(image_filepath)
        # check hocr file exist
        hocr_filepath = "{}/{}.hocr".format(hocr_folder, filename)
        if not os.path.exists(hocr_filepath):
            print("HOCR file does not exist for image")
            exit()

        # read hocr
        with open(hocr_filepath, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')

        annotations = []
        for word in soup.find_all('span', class_='ocrx_word'):
            text = word.get_text(strip=True)
            title = word.get('title')
            if text and title and 'bbox' in title:
                bbox_part = title.split(';')[0]  # e.g., 'bbox 100 200 150 220'
                coords = bbox_part.replace('bbox', '').strip()
                x1, y1, x2, y2 = map(int, coords.split())
                # out.write(f'Text: "{text}"\nBounding box: ({x1}, {y1}, {x2}, {y2})\n\n')
                # 377,117,463,117,465,130,378,130,Genaxis Theatre
                annotations.append({
                    "transcription": text,
                    "points": [[x1,y1], [x2,y1], [x2,y2], [x2,y1]]
                })
        # print(image_filepath + "\t" + json.dumps(annotations) + "\n")
        # exit()
        annotations_contents += image_filepath + "\t" + json.dumps(annotations) + "\n"

    with open(annotation_filepath, "w") as f:
        f.write(annotations_contents)

# hocr_to_pp("data/ao/images/train", "data/ao/hocr", "data/ao/train.txt")
hocr_to_pp("data/ao/images/test", "data/ao/hocr", "data/ao/test.txt")

    
        
