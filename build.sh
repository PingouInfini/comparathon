rm -rf ./docker/context/dockerdist/*.py
cp -Rf requirements.txt ./docker/context/
cp -Rf *.py ./docker/context/dockerdist
cp -Rf google/*.* ./docker/context/dockerdist/google/
cp -Rf face_reco/*.* ./docker/context/dockerdist/face_reco/
cp -Rf extractor ./docker/context/dockerdist/extractor/
cd docker
docker-compose.exe -f ./comparathon.yml up -d --build