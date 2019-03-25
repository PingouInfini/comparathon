# coding=utf-8
import face_recognition
import glob, os, datetime, shutil
import time

class facerecognition_process:
    def __init__(self):
        pass

    def fill_results_dir_with_valid_pictures(self, ref_image_path, source_dir, candidate):
        try:
            # Chemin de l'image de référence
            ref_image = face_recognition.load_image_file(ref_image_path)

            # list_of_unknown_image = []
            # list_of_unknown_face_encoding = []

            ref_encoding = face_recognition.face_encodings(ref_image)[0]

            known_faces = [
                ref_encoding
            ]

            dest_dir = "filtered_pictures/{}".format(candidate)
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)


            at_least_one_true = False

            index =0

            for picture in os.listdir(source_dir):
                index+=1
                t0 = time.time()
                try:

                    # La commande ci-dessous ajoute la personne, si elle n'est pas connue à une liste de personnes inconnues
                    # list_of_unknown_face_encoding.append(face_recognition.face_encodings(face_recognition.load_image_file(file))[0])

                    # results is an array of True/False telling if the unknown face matched anyone in the known_faces array

                    image = face_recognition.load_image_file(os.path.join(source_dir, picture))
                    # face_locations = face_recognition.face_locations(image)
                    #
                    # if (len(face_locations) > 0):
                    tolerance = 0.6
                    results = face_recognition.compare_faces(known_faces, face_recognition.face_encodings(image)[0], tolerance)

                    if results[0] == True:
                        shutil.copy2(os.path.join(source_dir, picture), dest_dir)
                        at_least_one_true = True

                    # else:
                    #     print("No face was detected on this picture")
                except:
                    pass

                t1= time.time()
                delta =(t1-t0)
                print ("### image n°"+ str(index)+ " : "+str(delta)+" sec");

            if (at_least_one_true == True):
                print("The candidate was observed at least on one picture")

                # print("Is the unknown face a picture of Obama? {}".format(results[1]))
                # print("Is the unknown face a new person that we've never seen before? {}".format(not True in results))

        # Get the face encodings for each face in each image file
        # Since there could be more than one face in each image, it returns a list of encodings.
        # But since I know each image only has one face, I only care about the first encoding in each image, so I grab index 0.


        except IndexError:
            print("I wasn't able to locate any faces in at least one of the images. Check the image files. Aborting...")
            quit()
