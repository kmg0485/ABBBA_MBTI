
import json
import csv

# Opening JSON file and loading the data
# into the variable data
with open(r'C:\Users\USER\Desktop\MBTI\movies\movie_movie.json', 'r', encoding = 'utf-8') as json_file:
    jsondata = json.load(json_file)
 
# now we will open a file for writing
data_file = open('movies/movie_movie.csv', 'w', newline='')

# create the csv writer object
csv_writer = csv.writer(data_file)
 
 
# Counter variable used for writing
# headers to the CSV file
count = 0
for data in jsondata:
    if count == 0:
        # Writing headers of CSV file
        header = data.keys()
        csv_writer.writerow(["movie_id", "title", "description", "poster"])
        count += 1
        
    # Writing data of CSV file
    csv_writer.writerow(data["fields"].values())
 
data_file.close()
