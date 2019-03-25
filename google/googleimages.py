import google.google_images_download as google_images_download


# Find allowed args on {https://github.com/hardikvasa/google-images-download#arguments}
def get_images_from_arguments(arguments):

    # class instantiation
    response = google_images_download.googleimagesdownload()

    # passing the arguments to the function
    response.download(arguments)



