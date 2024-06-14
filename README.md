# Extracting Multi-File Archives

1. **Fix the Archive:**
   - Use the following command to repair the archive:
     ```bash
     $ zip -FF data.zip --out data_single.zip
     ```
2. **Unzip the Result:**
   - After fixing the archive, you can extract its contents.
   - Execute the following command to unzip the repaired archive into a temporary directory (e.g., `./temp`):
     ```bash
     $ unzip data_single.zip -d /data
     ```
   - The `-d` flag specifies the target directory where the extracted files will be placed.
---
