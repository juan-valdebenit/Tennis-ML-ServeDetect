# Tennis Video Analysis
This repository basically analysis tennis video and segment it. 
Mian objective of this project is user will upload a video via frontend, 
Backend receive this video and segment and generate new segment videos based on 
player ball serve. 

## How to run
**Importent** first install ['ffmpeg'](https://ffmpeg.org/), for linux: sudo apt install ffmpeg
1. create  python virtual env.
User python version 3.10

``python -m venv venv``

2. Activate venv [use os based command]

``source venv/bin/active`` [Linux]

3. Install packages

``pip install -r requirements.txt``

4. if 'package 'lap' not found' [Optional]

``pip install lap``

5. Run project

``python main.py``

6. Default url:

``localhost:8000 or 0.0.0.0:8000``


### But before run set .env
Create a '.env' file in project root dir. then add below variables with valid values. 
```angular2html
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_access_kay
AWS_REGION=which_region your bucket located
IS_UPLOAD_TO_S3=true | false
IS_CLEAN_LOCAL_VIDEOS=false | true
AWS_S3_BUCKET_INPUT=your_bucket_name
AWS_S3_BUCKET_OUTPUT=your_bucket_name
```
IS_UPLOAD_TO_S3 - 
    - true: cut clip would be uploaded in s3

IS_CLEAN_LOCAL_VIDEOS:
    - true: local saved clip will be removed. 

### Local saved location:
```
project_root:
    static:
        - uploads
        - thumbnails
        
```
This uploads file contain locally saved clip. 
I you set 
IS_CLEAN_LOCAL_VIDEOS = true, it will clean this folder
otherwise it will keep. 


## Model 
Download model from given link in release note and
keep on bellow folders. 
```angular2html
project_root:
    - models
```
