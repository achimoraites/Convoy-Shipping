# Convoy-Shipping

Practicing data handling using Pandas, XML, JSON, SQLite and implementing Scoring Machines


## Context

Our imaginary company is working towards it's digital transformation and management needs a way to evaluate their fleet.

This is where our scoring machine comes to shine ✨, it will evaluate each vehicle based on
- Fuel consumption
- Cargo capacity
- Pit-stops for re-fueling


in general the more points a vehicle gets the better 🤖


We will work with a variety of files:
- .xlsx
- .csv
- .s3db (SQLite database)
- .xml
- .json

## Workflows

### Excel

1. Convert the Excel to a CSV file
2. Clean up the data
3. Store the cleaned up data in another CSV (adds the `[CHECKED].csv` at the end of the file name) to allow for later inspection 
4. Create a SQLite database to store the data and their scores
5. Read the database
6. For vehicles that have a score > 3 we will export the data to a JSON file
7. For the vehicles that scored 3 or less we will export them to an XML file

### CSV

1. Clean up the data
2. Store the cleaned up data in another CSV (adds the `[CHECKED].csv` at the end of the file name) to allow for later inspection 
3. Create a SQLite database to store the data and their scores
4. Read the database
5. For vehicles that have a score > 3 we will export the data to a JSON file
6. For the vehicles that scored 3 or less we will export them to an XML file

### SQLite
1. Read the database
2. For vehicles that have a score > 3 we will export the data to a JSON file
3. For the vehicles that scored 3 or less we will export them to an XML file

