# ICD10 to MySQL db 

Simple python script which parses the official systematic ICD10 data published by the Bundesinstitut für Arzneimittel und Medizinprodukte (BfArM) of Germany.

## Features

- Read  csv files (ICD-10-GM Version 2023 Metadaten TXT)
- Parse the data into a dictionary
- Load generated dictionary to database

## Prerequisite
### Datasets

To avoid using deprecated datasets, I recommend you download the original ICD10 dataset from the website fo BfArM. 
Source: https://www.bfarm.de/DE/Kodiersysteme/Services/Downloads/_node.html

Choose the following file package: ICD-10-GM Version 2023 Metadaten TXT (CSV)
> icd10gm2023syst-meta_20221206.zip

Unpack the archive and copy the following file from the folder named "Klassifikationsdateien"
> icd10gm2023syst_kodes_20221206.txt

Paste it in the root folder of "icd10ToMysql" and edit the filename in  "main.py" if necessary.

### Database

Create a table in your MySQL database with the following structure.

Table name: 
> icd10_keys

Columns:
> id [int(11), *Primary, AI)
> icd10_code [varchar(15)]
> icd10_alternative_code [varchar(15)]
> diagnose_text[varchar(200)]


##### MySQL credentials:
Open the main.py and change the host, user, password, database to your own data. After this step you should be ready to import the ICD10 in your databse by running:
> python main.py

##### Author: Martin Hocquel
##### License: MIT
