import sys
import google.googleimages as googleimages
import face_reco.face_reco as face_reco
import extractor.extractor as extractor

def usage():
    print("Usage:")
    print("python {} <username> <picture's filename>".format(sys.argv[0]))

def get_relative_images_and_url(user, ref_image_path, limit=25):
    #1 Get images from Google with username
    my_args = {"keywords": user, "limit": limit,
               "extract_metadata": True,
               "output_directory": "mesimages",
               "metadata_directory": "mesjson",
               "type": "photo"
               }

    googleimages.get_images_from_arguments(my_args)


    #2 Filter the gotten pictures with Face Recognition
    source_dir = "mesimages/{}".format(user)
    face_reco.pictures_filtering(ref_image_path, source_dir, user)

    #3 Extract the filtered pictures associated urls
    json_path="mesjson/{}.json".format(user)
    extractor.json_parsing(json_path, user)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        usage()
        sys.exit(1)

    user = sys.argv[1]
    ref_image_path = sys.argv[2]

    get_relative_images_and_url(user,ref_image_path)