# Bookstore Dashboard

My mum owns a bookstore and wanted a better way to visualise the top selling books in her bookstore.  So this is my attempt. 

This code uses Bokeh and Pandas to display the top selling books.  The number of top-sellers, the category, and the number of prior days over which to determine the top-sellers. Only one month of (anonymized) sales data is provided so the date range starting point is 30/11/2015. 

## Requirements

* Python 2.7
* Bokeh 
* Pandas  
* numpy


## Usage
###To run locally:

Download the repo.


To run the tool enter: `bokeh serve --show app` into the command line from the parent directory.

This will launch a web browser and display the top-sellers.  Use the widgets to change the selections.

###To access via the internet:

The app is running on Heroku and can be accessed  at <https://rocky-shelf-31398.herokuapp.com/app>
 
