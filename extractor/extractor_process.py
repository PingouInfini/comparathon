# coding=utf-8
import json
import os

class extractor_process:
    def __init__(self):
        pass

    def extract_urls_from_json(self, json_path, candidate):
        filtered_dir = "filtered_pictures/{}".format(candidate)
        list_txt = "Associated_Urls_to{}.txt".format(candidate)
        try:
            with open(json_path) as json_file:
                metadatas = json.load(json_file)
                written_file = open(list_txt, "w")
                pictures_list = os.listdir(filtered_dir)
                for picture in pictures_list :
                    for metadata in metadatas :
                        if (metadata['image_filename'] == picture):
                            written_file.write(metadata['image_filename'] + '\n')
                            written_file.write(metadata['image_link'] + '\n')
                            written_file.write(metadata['image_source'] + '\n' + '\n')
                written_file.close()

        except:
                print("kk")
                quit()