# Extracting Multi-File Archives
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

1. **Fix the Archive:**
   - Use the following command to repair the archive:
     ```bash
     $ zip -FF data.zip --out data_single.zip
     ```
2. **Unzip the Result:**
   - After fixing the archive, you can extract its contents.
   - Execute the following command to unzip the repaired archive into a temporary directory (e.g., `./temp`):
     ```bash
     $ unzip data_single.zip -d 
     ```
   - The `-d` flag specifies the target directory where the extracted files will be placed.
---
