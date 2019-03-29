import extractor.extractor_process as extractionprocess

def json_parsing(json_path, candidate):

    #Class instantiation
    response = extractionprocess.extractor_process()

    #Json parsing for urls extraction
    response.extract_urls_from_json(json_path, candidate)