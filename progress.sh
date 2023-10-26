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

# Define the character to split lines on
split_char='。'

# Split lines on the specified character and remove empty items
total_items=$(awk -v RS='\n' -F"$split_char" '{ for (i=1; i<=NF; i++) if ($i != "") items++; } END { print items }' "$txt_file")

# Define the path to the directory
audio_directory="audio"

# Count the number of files in the "audio" directory
num_files=$(find "$audio_directory" -type f | wc -l)

# Calculate the percentage rounded to the nearest decimal place
percentage=$(bc -l <<< "$num_files / $total_items * 100")

# Print the results
echo "Total items in the list: $total_items"
echo "Number of files in $audio_directory: $num_files"
echo "Percentage: $percentage%"

