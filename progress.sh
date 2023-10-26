#!/bin/bash

# Check if a file path is provided as an argument
if [ $# -ne 1 ]; then
    echo "Usage: $0 <text_file>"
    exit 1
fi

# Get the text file path from the command line argument
txt_file="$1"

# Check if the text file exists
if [ ! -f "$txt_file" ]; then
    echo "Error: The specified text file does not exist."
    exit 1
fi

# Count the total number of lines in the text file
total_lines=$(wc -l < "$txt_file")

# Define the path to the directory
audio_directory="audio"

# Count the number of files in the "audio" directory
num_files=$(find "$audio_directory" -type f | wc -l)

# Calculate the percentage
percentage=$(bc  <<< "scale=3; $num_files / $total_lines * 100")

# Print the results
echo "Total lines in $txt_file: $total_lines"
echo "Number of files in $audio_directory: $num_files"
echo "Percentage: $percentage%"
