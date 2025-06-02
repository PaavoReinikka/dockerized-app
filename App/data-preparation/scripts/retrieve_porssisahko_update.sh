#!/bin/bash

# downloads the xlsx file from the porssisahko API
curl https://porssisahko.net/api/internal/excel-export --output ../data/updated_porssisahko.xlsx

# checks if the file was downloaded successfully
if [ $? -ne 0 ]; then
    echo "Failed to download the file"
    exit 1
fi

input_file="../data/updated_porssisahko.xlsx"
# output filename is same as input file with .csv extension
output_file="${input_file%.*}.csv"

# ssconvert transforms the file to csv format in temp_file.csv
ssconvert "$input_file" temp_file.csv # for debugging

# removes first 3 rows from temp_file.csv
sed -i '1,3d' temp_file.csv

# save the modified file as output_file
mv temp_file.csv "$output_file"

echo "File converted and saved as $output_file"

# python script to process the csv file (nicer format with pandas and datetime)
python clean_porssisahko.py "$output_file"
# the new name has "_cleaned.csv" appended to the original name
rm -f "$output_file" # (comment for debugging)
mv "${output_file%.csv}_cleaned.csv" "$output_file"

# run the populate_porssisahko.py script
python populate_porssisahko.py "$output_file"
# print success message
echo "Table porssisahko populated from file $output_file"
# remove the original file
#rm -f "$input_file" # (comment for debugging)