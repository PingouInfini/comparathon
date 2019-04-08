rm -rf ./docker/context/dockerdist/*
touch ./docker/context/dockerdist/README.md
mkdir -p ./docker/context/ && cp -Rf requirements.txt ./docker/context/
mkdir -p ./docker/context/dockerdist && cp -Rf *.py ./docker/context/dockerdist
mkdir -p ./docker/context/dockerdist/google/ && cp -Rf google/*.* ./docker/context/dockerdist/google/
mkdir -p ./docker/context/dockerdist/face_reco/ && cp -Rf face_reco/*.* ./docker/context/dockerdist/face_reco/
mkdir -p ./docker/context/dockerdist/extractor/ && cp -Rf extractor ./docker/context/dockerdist/extractor/
cd docker
docker-compose -f ./comparathon.yml up -d --build
