# lds-mailing-labels

# pre-requisites
https://pypi.org/project/pylabels/
1. pip install pylabels

2. install chrome HTML-Table Scraper
https://chrome.google.com/webstore/detail/html-table-scraper/ncphhmcjgbpglahiijnaaaaneoijlmkj/related?hl=en

# how to use
1. Turn off all options in the table scraper, set it to comma separate values
2. create a report that looks like the report_format.png
![report format ](https://github.com/adamulrich/lds-mailing-labels/blob/main/report_format.png)
3. preview the report.
4. right click in the table and choose the html table scraper and save it to a file label_data.csv in this folder.
5. review the data and remove any lines that you don't want to print.
6. run python create_labels.py.

results in:
* labels.pdf file in this directory.

If you encounter asserts when running the code, you have data quality issues. Read the messages and debug. I ran into:

* Missing city, state and zip codes
* Extra commas in the data, such as "123 main st, apt 10". Apt 10 should be in Address 2.

