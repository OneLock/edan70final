#!/bin/bash

# Check if 'zip' is installed
if ! command -v zip &> /dev/null; then
    echo "The 'zip' command is not installed. Please install it."
    echo "Or use another program of your choice that unzip can unzip multi-archived files."
    exit 1
fi


# Function to fix and unzip a multipart ZIP file
fix_and_unzip() {
    local input_zip="$1"
    local output_dir=$(pwd)

    # Fix the multipart ZIP file using zip -FF
    zip -FF "$input_zip" --out "${input_zip%.zip}_single.zip"

    # Unzip the fixed single ZIP file
    unzip "${input_zip%.zip}_single.zip" "$output_dir"
}

# Navigate to the directory containing the zipped files
cd zipped_files/data

# Fix and unzip data.zip
fix_and_unzip data.zip
mv data ../../

# Navigate to the models directory
cd ../models

# Fix and unzip model_split.zip
fix_and_unzip model_split.zip
mv model ../../

cd ../../
rm -rf zipped_files
