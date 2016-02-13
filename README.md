# ArtSpeaker

##### Download the latest image

```
docker pull julietteTaka/artspeaker
```

##### Run the image
```
docker run -td --name artspi_cnt -p 8000:5000 -p 5001:5001 -p 27017:27017 -v $PWD:/opt/artspeaker_git -v /var/log/artspeaker:/var/log/artspeaker -v /opt/mongo-data:/opt/mongo-data juliettetaka/artspeaker:develop
```