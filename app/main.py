
import pandas as pd
import numpy as np
from bokeh.models import ColumnDataSource, HoverTool, Range1d, Div
from bokeh.plotting import figure, curdoc
from bokeh.layouts import column, row, widgetbox
from bokeh.models.widgets import Select, Slider
import os


"""
This code uses Bokeh and Pandas to display the top sellers based upon category for a bookstore

TODO: add time series plot of top sellers
"""

def category_selector(attr, old, new):
    '''Update the plot when the category selection, date range, or number of top sellers is changed'''

    day_min = "2015-11-" + str(30 - day_slider.value).zfill(2)
    if cat_select.value == 'All':
        top_sales = sales[(sales["Invoice Date"] > day_min) & (sales["Invoice Date"] <= day_max)]['Title'].value_counts()[0:n_slider.value]
    else:
        top_sales = sales[(sales["Invoice Date"] > day_min) & (sales["Invoice Date"] <= day_max)]['Title'][sales.Category == cat_select.value].value_counts()[0:n_slider.value]

    top_sales = top_sales.to_frame()
    top_sales.reset_index(inplace=True)
    top_sales.rename(columns={'index': 'title', 'Title': 'sales'}, inplace=True)
    top_sales['short_title'] = top_sales['title'].apply(trim_title)
    top_counts_plot.y_range.factors = top_sales.short_title.values.tolist()
    top_counts_plot.x_range.end =  np.max(top_sales.sales) + 1
    top_sales_cds.data = ColumnDataSource(data=dict(titles=top_sales.short_title, counts=top_sales.sales,
                                                    fulltitle=top_sales.title)).data

def trim_title(str_x):
    '''Checks if string is longer than 30 characters, if it is it trims it to 27 and adds '...' '''

    if len(str_x) > 30:
        str_x = str_x[0:27] + '...'
        return str_x
    else:
        return str_x

div = Div(text="""<h1>Bookstore Dashboard</h1> This interactively displays the top selling books by category for a 
                    bookstore over a number of days.  
                    <h3>To use:</h3> 
                    <ol>
                      <li>Select the category you wish to display from the drop-down menu</li>
                      <li>Use the slider to select the number of days over which you want to determine the top-sellers. 
                      <i>Note: This is not currently dynamic, and will display the top-sellers over N days prior to November 30th 2015</i></li>
                      <li>Use the slider to select the number of top-sellers you want to display (1-25)</li>
                    </ol>
                    Changing any of these will update the plots to reflect the new selections.  If the full title is not displayed, hover the mouse
                    over the bar to display the full title.
                    <i>Note: In order to anonymize the sales data the words in the book titles were randomly replaced, thus the titles are just jibberish.</i>
                    """,
          width=600, height=255)


## Load the sales file
sales_file = os.path.join(os.path.dirname(__file__), 'data', 'bookstore_clean_dataset.csv')
sales = pd.read_csv(sales_file, parse_dates=['Invoice Date'], dayfirst=True)

## set up some selection widgets
# Select by category
options = ['All'] + sales['Category'].unique().tolist()
cat_select = Select(title="Category:", value="All", options=options)
cat_select.on_change('value', category_selector)

#Select the number of days over which to display
day_slider = Slider(start=1, end=29, value=29, step=1, title="Last N Days")
day_slider.on_change('value', category_selector)
day_max = "2015-11-30" #make this dynamic
day_min = "2015-11-" + str(30 - day_slider.value).zfill(2)

#Select the number of top-sellers to display
n_slider = Slider(start=1, end=25, value=10, step=1, title="Number of Top Sellers")
n_slider.on_change('value', category_selector)

## Calculate top sellers
top_sales = sales[(sales["Invoice Date"] > day_min) & (sales["Invoice Date"] <= day_max)]['Title'].value_counts()[0:n_slider.value]
top_sales = top_sales.to_frame()
top_sales.reset_index(inplace=True)
top_sales.rename(columns={'index':'title', 'Title':'sales'}, inplace=True)
top_sales['short_title'] = top_sales['title'].apply(trim_title)

top_sales_cds = ColumnDataSource(data=dict(titles=top_sales.short_title, counts=top_sales.sales,
                                           fulltitle=top_sales.title))

hover = HoverTool(
        tooltips=[("Title", "@fulltitle"),
                    ("Sales", "@counts")])

top_counts_plot = figure(title="Top Sellers", x_axis_label='Sales', tools=[hover], toolbar_location='right',
            y_range=top_sales.short_title.values.tolist(), x_range=[0,np.max(top_sales.sales) + 5])


top_counts_plot.hbar(y='titles', height=0.3, left=0, right='counts', source=top_sales_cds, color="deepskyblue" )

layout = column(widgetbox(div),
                row(widgetbox(cat_select, width=200),
                widgetbox(day_slider, width=200),
                widgetbox(n_slider, width=200)),
                top_counts_plot)

curdoc().add_root(layout)
curdoc().title = "Bookstore Dashboard"
