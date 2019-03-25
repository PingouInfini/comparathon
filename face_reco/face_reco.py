import face_reco.facerecognition_process as facerecognition_process


# Find allowed args on {https://github.com/hardikvasa/google-images-download#arguments}
def pictures_filtering(ref_image, source_dir, candidate):

    # class instantiation
    response = facerecognition_process.facerecognition_process()

    # passing the arguments to the function
    response.fill_results_dir_with_valid_pictures(ref_image, source_dir, candidate)

