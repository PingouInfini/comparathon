import sys
import google.googleimages as googleimages

def usage():
    print("Usage:")
    print("python {} <username>".format(sys.argv[0]))


if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
        sys.exit(1)

    user = sys.argv[1]

    #1 get google img from username
    my_args = {"keywords": user, "limit": 1,
                "extract_metadata": True,
                "output_directory": "mesimages",
                "metadata_directory": "mesjson",
                "type": "photo"
                }
    googleimages.get_images_from_arguments(my_args)


    #2 filter img and get utils URLs
