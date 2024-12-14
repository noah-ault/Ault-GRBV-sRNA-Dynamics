# This python script is designed to parse a table of exported nucleotide sequences from CLC Genomics Workbench v21.0.5, where the 4th column contains the length of each sequence
# Before running, prepare a directory containing only this script and input files
# When running this script, run it from this prepared directory
import os
import csv
from collections import defaultdict

# Set the directory containing the .csv files to working directory
input_directory = os.getcwd()
output_file = "LengthCounts.csv"

# Define the range of nucleotide length to count
number_range = range(18, 29)  # Numbers 18 to 28

# Initialize a dictionary to hold counts for each nucleotide length across files
counts = {num: defaultdict(int) for num in number_range}

# Parse each .csv file in the directory
for file_name in os.listdir(input_directory):
    if file_name.endswith(".csv"):
        file_path = os.path.join(input_directory, file_name)
        try:
            # Open and read the CSV file
            with open(file_path, mode="r", newline="") as f:
                reader = csv.reader(f)
                for row in reader:
                    try:
                        # Ensure the row has at least 4 columns
                        if len(row) >= 4:
                            value = int(row[3])  # Extract the 4th column
                            if value in number_range:
                                counts[value][file_name] += 1
                    except ValueError:
                        # Skip rows where the 4th column isn't a valid integer
                        continue
        except Exception as e:
            print(f"Error processing file {file_name}: {e}")

# Write the output to a CSV file
with open(output_file, mode="w", newline="") as f:
    writer = csv.writer(f)
    
    # Write the header row
    header = ["Length"] + sorted(os.listdir(input_directory))
    writer.writerow(header)
    
    # Write the counts for each length
    for num in number_range:
        row = [num] + [counts[num].get(file_name, 0) for file_name in sorted(os.listdir(input_directory))]
        writer.writerow(row)

print(f"Output saved to {output_file}")