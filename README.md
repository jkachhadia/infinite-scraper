# Infinite Scraper

A PyQt application to scrape all residential buy/rental data from platforms like magicbricks(Infinite scrolling) and 99acres and save it in any format you want.

![alt text](http://i.imgur.com/bUeIgld.png)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

You should have a Python3 installed in your system along with the following libraries like selenium, bs4, PyQt5, pandas and numpy. You should preferably install Pycharm Community edition as it comes with PyQt5 package installed.

# Usage of the application

As shown in the GUI, application generally consists of two line-edits:
* **City input box** - Input the name of city for which you want to get data.
* **Locality input box** - Input the name of city's locality whose data you want to fetch.
It also consists of two drop down buttons:
* **Output file type** - CSV, Excel or JSON data formats available.
* **Data type** - Buy/Rent
It has two buttons for fetching data from two different platforms:
* magicbricks
* 99acres

It has one button called **Convert** which will save your fetched data in desired output type.

# Gist of the application

It tackles an important problem of infinite scrolling which is faced in websites like facebook, twitter, etc. Magic breaks has a similar kind of architecture which enables infinite scrolling after querying a search.
the following snippet of code shows how to find and end of the infinite scrolling page.
```
lastHeight = driver.execute_script("return document.body.scrollHeight")
while True:
   driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
   time.sleep(2)
   newHeight = driver.execute_script("return document.body.scrollHeight")
   if newHeight == lastHeight:
       break
   lastHeight = newHeight
```


## Built With

* [PyQt5](http://pyqt.sourceforge.net/Docs/PyQt5/) -  Python bindings for the Qt cross-platform GUI
* [Selenium](http://selenium-python.readthedocs.io/) - Python bindings for browser automation
* [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) - Python library for pulling data out of HTML and XML files
* [Pandas](http://pandas.pydata.org/pandas-docs/stable/) - Python package providing fast, flexible, and expressive data structures for data analysis
