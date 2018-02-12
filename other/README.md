```
usage:  main.py [-h] 
        --clientId CLIENTID
        --clientSecret CLIENTSECRET 
        [--stepSnapshotFile STEPSNAPSHOTFILE] 
        [--importStep]
        [--uploadImage]
        [--lesson LESSON] 
        [--step STEP]
        [--image IMAGE_PATH,IMAGE_PATH_1,...]

optional arguments:
  -h, --help            show this help message and exit
  --clientId CLIENTID   oauth client id for stepic.org
  --clientSecret CLIENTSECRET
                        oauth client secret for stepic.org
  --stepSnapshotFile STEPSNAPSHOTFILE
                        step snapshot file path to import
  --importStep          perform step import --stepSnapshotFile, --lesson and
                        --step required
  --lesson LESSON       lesson id
  --step STEP           step number (starting from 1)
  --uploadImages        perform upload images to stepic related server(uploadcare.com), --images required
  --images IMAGES       paths to images (divided with coma). Example: '--images path1,path2,...'
```

Examples:
```bash
python main.py --clientId ID_OAUTH --clientSecret SECRET_OAUTH --stepSnapshotFile test_steps/test.step --importStep --lesson 40923 --step 1
python main.py --clientId ID_OAUTH --clientSecret SECRET_OAUTH --uploadImages --images IMAGE_PATH,IMAGE_PATH_1,...
```
