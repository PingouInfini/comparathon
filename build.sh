rm -rf ./docker/context/dockerdist/*
touch ./docker/context/dockerdist/README.md
mkdir -p ./docker/context/ && cp -Rf requirements.txt ./docker/context/
mkdir -p ./docker/context/dockerdist && cp -Rf *.py ./docker/context/dockerdist
cp -Rf entrypoint.sh ./docker/context/dockerdist
mkdir -p ./docker/context/dockerdist/google/ && cp -Rf google/*.* ./docker/context/dockerdist/google/
docker-compose -f ./docker/comparathon.yml up -d --build
