del ".\docker\context\dockerdist\*" /s /f /q
echo "" > README.md
xcopy "requirements.txt" ".\docker\context\" /Y /F
xcopy "*.py" ".\docker\context\dockerdist" /Y /F
xcopy "google\*.*" ".\docker\context\dockerdist\google\" /Y /F
xcopy "face_reco\*.*" ".\docker\context\dockerdist\face_reco\" /Y /F
xcopy "extractor" ".\docker\context\dockerdist\extractor\" /Y /E
cd docker
docker-compose.exe -f .\comparathon.yml up -d --build