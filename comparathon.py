import sys
import google.googleimages as googleimages
import face_reco.face_reco as face_reco

def usage():
    print("Usage:")
    print("python {} <username> <picture's filename>".format(sys.argv[0]))


if __name__ == '__main__':
    if len(sys.argv) != 3:
        usage()
        sys.exit(1)

    user = sys.argv[1]

    #1 get google img from username
    my_args = {"keywords": user, "limit": 10,
                "extract_metadata": True,
                "output_directory": "mesimages",
                "metadata_directory": "mesjson",
                "type": "photo"
                }
    googleimages.get_images_from_arguments(my_args)


    #2 filter img and get utils URLs

    ref_image_path = sys.argv[2]
    source_dir = "mesimages/{}".format(user)
    face_reco.pictures_filtering(ref_image_path, source_dir, user)

