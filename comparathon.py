import sys
import google.googleimages as googleimages
import face_reco.face_reco as face_reco
import time
import extractor.extractor as extractor

def usage():
    print("Usage:")
    print("python {} <username> <picture's filename>".format(sys.argv[0]))


if __name__ == '__main__':
    t0 = time.time()
    if len(sys.argv) != 3:
        usage()
        sys.exit(1)

    user = sys.argv[1]

    #1 Get images from Google with username
    #t1 = time.time()
    #print ("START 1st STEP " + str(d1))
    my_args = {"keywords": user, "limit": 25,
                "extract_metadata": True,
                "output_directory": "mesimages",
                "metadata_directory": "mesjson",
                "type": "photo"
                }
    googleimages.get_images_from_arguments(my_args)


    #2 Filter the gotten pictures with Face Recognition
    #t2 = time.time()
    #d1 = (t1-t0)
    #d2 = (t2-t1)
    #print("START 2nd STEP " + str(d2))
    ref_image_path = sys.argv[2]
    source_dir = "mesimages/{}".format(user)
    face_reco.pictures_filtering(ref_image_path, source_dir, user)
    #t3 = time.time()
    #d3 = (t3-t2)
    #print("START 3rd STEP " + str(d3))

    #3 Extract the filtered pictures associated urls

    json_path="mesjson/{}.json".format(user)
    extractor.json_parsing(json_path, user)



