# Object Detection and Counting API

--------------------------------

To run the files in the docker environment please use the following command
```python
docker-compose up -d # To run in detached mode
```

Now please send a POST request to the localhost:8001/segment with the following JSON Payload
```json
{
    "path": "_____image_path_____" # this can be a local path or a URL
}
```

To check the health of the API, send a GET request to the `localhost:8001/health`

And to get the Detections for the Image requested, send a GET request to the `localhost:8001/static/<id>.png`