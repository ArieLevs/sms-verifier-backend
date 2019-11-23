# sms-verifier-backend
SMS Verification App is a project that allows guests verify attendance to events,
Since the only option i had to send SMS messages was via and Android device,
This project will work only with [this project](https://github.com/ArieLevs/sms-verifier-android).

Create docker image   
```bash
docker build \
    -t sms-verifier/sms-verifier-backend \
    --build-arg PYPI_REPO=https://USERNAME:PASSWORD@nexus.nalkins.cloud/repository/pypi-repo/simple .
```  
