# Extracting The Multi-File Archived Files
```
zipped_files
│
├───data
│   │   data.z01
│   │   data.z02
│   │   ...
|   |   data.zip
│
└───models
    |   model_split.z01
    |   model_split.z02
    |   ...
    |   model_split.zip
```
From the project folder run do the follwoing steps to unzip the `data` and `model` directories:
1. Give excute rights:
   ```
   chmod 744 fix_and_unzip.sh
   ```
2. run script
   ```
   ./fix_and_unzip.sh
   ```
