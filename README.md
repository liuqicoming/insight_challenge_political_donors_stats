# Table of Contents
1. [Introduction](README.md#introduction)
2. [Input file](README.md#input-file)
3. [Data processing](README.md#data-processing)
4. [Output files](README.md#output-files)
5. [Example](README.md#example)
6. [Repo directory structure](README.md#repo-directory-structure)


# Introduction
This project is for the assigned challenge from Insight Data Engineering Bootcamp program. This project reads the input text file in the "input" folder, processes the data, then outputs two files into the output folder. Description of the input file, data processing, and output files and be found below.

# Input file
Input file is a text file "itcont.txt" published by The Federal Election Commission [(download here)](http://classic.fec.gov/finance/disclosure/ftpdet.shtml). This file lists political campaign contributions by individual donors

# Data Processing
As required by the challenge, the execution file in the src folder reads the input file and distill it into two output files. The potential role of this process is to work on the data pipleline that can hand off the information to the front-end. The fields of interest are the zip code associated with the donor, amount contributed, date of the transaction and ID of the recipient. This code processes through each input file line, calculatea the running median of contributions, total number of transactions and total amount of contributions streaming in so far for that recipient and zip code. The calculated fields then are formatted into a pipe-delimited line and written to an output file named `medianvals_by_zip.txt` in the same order as the input line appeared in the input file. 

This program also writes to a second output file named `medianvals_by_date.txt`. Each line of this second output file lists every unique combination of date and recipient from the input file and then the calculated total contributions and median contribution for that combination of date and recipient. The fields on each pipe-delimited line of `medianvals_by_date.txt` are recipient, date, medium contribution, total number of transactions, and total amount of contributions. The second output file have lines sorted alphabetical by recipient and then chronologically by date.

Also, unlike the first output file, every line in the `medianvals_by_date.txt` file should be represented by a unique combination of day and recipient -- there is no duplicates. 

Below are the ones that you¡¯ll need to complete this challenge:

* `CMTE_ID`: identifies the flier, which for our purposes is the recipient of this contribution
* `ZIP_CODE`:  zip code of the contributor (we only want the first five digits/characters)
* `TRANSACTION_DT`: date of the transaction
* `TRANSACTION_AMT`: amount of the transaction
* `OTHER_ID`: a field that denotes whether contribution came from a person or an entity 

# Output files

1. `medianvals_by_zip.txt`: contains a calculated running median, total dollar amount and total number of contributions by recipient and zip code

2. `medianvals_by_date.txt`: has the calculated median, total dollar amount and total number of contributions by recipient and date.

# Example
Here's an example of a few lines in the input file.

> **C00629618**|N|TER|P|201701230300133512|15C|IND|PEREZ, JOHN A|LOS ANGELES|CA|**90017**|PRINCIPAL|DOUBLE NICKEL ADVISORS|**01032017**|**40**|**H6CA34245**|SA01251735122|1141239|||2012520171368850783

> **C00177436**|N|M2|P|201702039042410894|15|IND|DEEHAN, WILLIAM N|ALPHARETTA|GA|**300047357**|UNUM|SVP, SALES, CL|**01312017**|**384**||PR2283873845050|1147350||P/R DEDUCTION ($192.00 BI-WEEKLY)|4020820171370029337

> **C00384818**|N|M2|P|201702039042412112|15|IND|ABBOTT, JOSEPH|WOONSOCKET|RI|**028956146**|CVS HEALTH|VP, RETAIL PHARMACY OPS|**01122017**|**250**||2017020211435-887|1147467|||4020820171370030285

> **C00177436**|N|M2|P|201702039042410893|15|IND|SABOURIN, JAMES|LOOKOUT MOUNTAIN|GA|**307502818**|UNUM|SVP, CORPORATE COMMUNICATIONS|**01312017**|**230**||PR1890575345050|1147350||P/R DEDUCTION ($115.00 BI-WEEKLY)|4020820171370029335

> **C00177436**|N|M2|P|201702039042410895|15|IND|JEROME, CHRISTOPHER|FALMOUTH|ME|**041051896**|UNUM|EVP, GLOBAL SERVICES|**01312017**|**384**||PR2283905245050|1147350||P/R DEDUCTION ($192.00 BI-WEEKLY)|4020820171370029342

> **C00384818**|N|M2|P|201702039042412112|15|IND|BAKER, SCOTT|WOONSOCKET|RI|**028956146**|CVS HEALTH|EVP, HEAD OF RETAIL OPERATIONS|**01122017**|**333**||2017020211435-910|1147467|||4020820171370030287

> **C00177436**|N|M2|P|201702039042410894|15|IND|FOLEY, JOSEPH|FALMOUTH|ME|**041051935**|UNUM|SVP, CORP MKTG & PUBLIC RELAT.|**01312017**|**384**||PR2283904845050|1147350||P/R DEDUCTION ($192.00 BI-WEEKLY)|4020820171370029339

Processing all of the input lines, the entire contents of `medianvals_by_zip.txt` would be:

    C00177436|30004|384|1|384
    C00384818|02895|250|1|250
    C00177436|30750|230|1|230
    C00177436|04105|384|1|384
    C00384818|02895|292|2|583
    C00177436|04105|384|2|768

 `medianvals_by_date.txt` would contain these lines in this order:

    C00177436|01312017|384|4|1382
    C00384818|01122017|292|2|583


