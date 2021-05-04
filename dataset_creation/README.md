# Generating Dataset from MIMIC-III Data

Steps to create v1 of the MIMIC-III dataset for discharge summary predictions
* Change `DATA_PATH` variable in `params.py` to point to the `NOTEEVENTS.csv` file inside MIMIC-III data folder
  (note: you might need to extract the csv file from the compressed `csv.gz` file)
  
* Run the `data_preparation.py` file. Should take a few minutes to run. The output csv file will be stored as `prepared_dataset.csv`

