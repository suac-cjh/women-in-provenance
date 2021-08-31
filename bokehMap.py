'''
Name: bokehMap.py
Contact: Pauline Arnoud (parnoud@stanford.edu)

This file contains the code to create the bokeh Map which can filter
data based on citizenship, cause of death, inferred sex, and date of 
birth/death.

Depending on whether you want to output the map itself or the html code
for the map (to embed it into Omeka), please comment/uncomment the appropriate
lines at the very end of the code.

Make sure to activate the bokeh-env virtual environment before running the code
if you don't want to install all the libraries yourself.
'''

# importing libraries
from datetime import datetime, date
import pandas as pd
from bokeh.layouts import widgetbox, row
from bokeh.plotting import figure, output_file, show
from bokeh.models import (
    ColumnDataSource,
    CDSView,
    CustomJS,
    Select,
    IndexFilter,
    GroupFilter,
)
from bokeh.models.tools import HoverTool
from bokeh.models.widgets import DateRangeSlider
from bokeh.tile_providers import get_provider
from geopy.geocoders import Nominatim
from pyproj import Transformer

from bokeh.embed import components
from bokeh.resources import CDN
from bokeh.embed import file_html
from bokeh.layouts import row

# Setting the bokeh output file at which to display the finished map
output_file('bokeh_map.html')

# Defining two functions to convert location names to lat/lon and 
# eastern/northing coordinates (which are needed for bokeh plotting)
def Loc_to_LongLat(location):
    if location == "":
        return None, None
    address = location.split(";")
    address = address[-1]
    geolocator = Nominatim(user_agent="my_user_agent")
    loc = geolocator.geocode(address, timeout=None)
    try:
        return loc.longitude, loc.latitude
    except:
        return None, None

def LongLat_to_EN(lon, lat):
    try:
        transformer = Transformer.from_crs('epsg:4326', 'epsg:3857')
        easting, northing = transformer.transform(lat, lon)
        return easting, northing
    except:
        return None, None

# Creating the dataframe
df = pd.read_csv("all_people.csv")  
df = df.fillna("")

# Adding lat/long and eastern/northing coordinate columns in the dataframe
df["Birth_lon"], df["Birth_lat"] = zip(
    *df.apply(lambda x: Loc_to_LongLat(x["Place of Birth"]), axis=1))

df["Death_lon"], df["Death_lat"] = zip(
    *df.apply(lambda x: Loc_to_LongLat(x["Place of Death"]), axis=1))

df["Birth_E"], df["Birth_N"] = zip(
    *df.apply(lambda x: LongLat_to_EN(x['Birth_lon'], x['Birth_lat']), axis=1))

df["Death_E"], df["Death_N"] = zip(
    *df.apply(lambda x: LongLat_to_EN(x['Death_lon'], x['Death_lat']), axis=1))

# Changing some of the column names to remove the spaces and to convert date to datetimes
df = df.rename(columns={"Cause of Death":"deathcause"})
df = df.rename(columns={"Inferred Sex": "inferredsex"})
df["birthdate"] = pd.to_datetime(df["Date of Birth"])
df["deathdate"] = pd.to_datetime(df["Date of Death"])

# Defining the source from which bokeh will search for the data it uses
source = ColumnDataSource(df)

# Creating a figure and setting its background to a blank map
p = figure(plot_width=580, plot_height=450, title="WiP Interactive Map", 
           x_range = (-18706892.5544, 21289852.6142), y_range = (-7631472.9040, 12797393.0236))
provider = get_provider('CARTODBPOSITRON')
p.add_tile(provider)

# creating the citizenship filter by making a list of the different options, creating a Select
# widget with those options and its associated IndexFilter
citizenship_options = ["All"] + sorted(list(df["Citizenship"].unique()))
citizenship_options.remove("")
for elem in citizenship_options:
    if "/" in elem:
        split = elem.split("/")
        for citiz in split:
            if citiz not in citizenship_options:
                citizenship_options.append(citiz)
        citizenship_options.remove(elem)

citizenship_select = Select(
    title="Citizenship", value="All", options=citizenship_options
)

citizenship_filter = IndexFilter(indices=list(range(len(df))))

# creating the deathcause filter by making a list of the different options, creating a Select
# widget with those options and its associated IndexFilter
deathcause_options = ["All"] + sorted(list(df["deathcause"].unique()))
deathcause_options.remove("")
for elem in deathcause_options:
    if "/" in elem:
        split = elem.split("/")
        for cause in split:
            if cause not in deathcause_options:
                deathcause_options.append(cause)
        deathcause_options.remove(elem)

deathcause_select = Select(
    title="Cause of Death", value="All", options=deathcause_options
)
deathcause_filter = IndexFilter(indices=list(range(len(df))))

# creating the inferred sex filter by making a list of the different options, creating a Select
# widget with those options and its associated IndexFilter
sex_options = ["All"] + sorted(list(df["inferredsex"].unique()))
if "" in sex_options:
    sex_options.remove("")
sex_select = Select (
    title="Inferred Sex", value="All", options=sex_options
)
sex_filter = IndexFilter(indices=list(range(len(df))))

# creating the birthdate slider by defining the date range, creating a DateRangeSlider
# widget with those start/end dates and its associated IndexFilter.
start = date(1825, 1, 1)
end = date.today()

birthdate_slider = DateRangeSlider(title="Birth Between", start=start, 
                                   end=end, value=(start, end), step = 1)
birthdate_filter = IndexFilter(indices=list(range(len(df))))

# creating the deathdate slider by defining the date range, creating a DateRangeSlider
# widget with those start/end dates and its associated IndexFilter.
deathdate_slider = DateRangeSlider(title="Death Between", start=start, 
                                   end=end, value=(start, end), step = 1)
deathdate_filter = IndexFilter(indices=list(range(len(df))))

# defining the CDSView to select subsets of data based on the filters 
view = CDSView(source=source, filters=[deathcause_filter, citizenship_filter, 
                                       sex_filter, birthdate_filter, deathdate_filter])

# defining the JS callback to follow then the citizenship select bar value is changed 
citizenship_select.js_on_change(
    "value",
    CustomJS(
        args={"filter": citizenship_filter, "view": view, "source": source, "c_select": citizenship_select},
        code="""
        if (c_select.value === "All") {
            filter.indices = Object.values(source.data.index);
        } else {
            filter.indices = source.data.Citizenship.flatMap((c, i) => c.includes(c_select.value) ? i : []);
        }
        view.properties.filters.change.emit();
        """,
    ),
)

# defining the JS callback to follow then the deathcause select bar value is changed 
deathcause_select.js_on_change(
    "value",
    CustomJS(
        args={"filter": deathcause_filter, "view": view, "source": source, "d_select": deathcause_select},
        code="""
        if (d_select.value === "All") {
            filter.indices = Object.values(source.data.index);
        } else {
            filter.indices = source.data.deathcause.flatMap((c, i) => c.includes(d_select.value) ? i : []);
        }
        view.properties.filters.change.emit();
        """,
    ),
)

# defining the JS callback to follow then the inferred sex select bar value is changed 
sex_select.js_on_change(
    "value",
    CustomJS(
        args={"filter": deathcause_filter, "view": view, "source": source, "s_select": sex_select},
        code="""
        if (s_select.value === "All") {
            filter.indices = Object.values(source.data.index);
        } else {
            filter.indices = source.data.inferredsex.flatMap((c, i) => c.includes(s_select.value) ? i : []);
        }
        view.properties.filters.change.emit();
        """,
    ),
)

# defining the JS callback to follow then the start or end date value is changed on the birthdate slider
birthdate_slider.js_on_change(
    "value",
    CustomJS(
        args={"filter": birthdate_filter, "view": view, "source": source, "date_slider":birthdate_slider},
        code = """
            var indices = [];
            for (var i = 0, il=source.data.birthdate.length; i < il; i++) {
                if ((source.data.birthdate[i] > date_slider.value[0]) && (source.data.birthdate[i] < date_slider.value[1])){
                    indices.push(i)
                }
            }
            
            filter.indices = indices
            view.properties.filters.change.emit();
        """
    )
)

# defining the JS callback to follow then the start or end date value is changed on the deathdate slider
deathdate_slider.js_on_change(
    "value",
    CustomJS(
        args={"filter": deathdate_filter, "view": view, "source": source, "date_slider":deathdate_slider},
        code = """
            var indices = [];
            for (var i = 0, il=source.data.deathdate.length; i < il; i++) {
                if ((source.data.deathdate[i] > date_slider.value[0]) && (source.data.deathdate[i] < date_slider.value[1])){
                    indices.push(i)
                }
            }
            
            filter.indices = indices
            view.properties.filters.change.emit();
        """
    )
)

# Plotting the locations on the map as circles
p.circle(x='Birth_E', y='Birth_N', size=10,
         line_color='grey', fill_color='royalblue', legend_label="Place of Birth", source=source, view=view)
p.circle(x='Death_E', y='Death_N', size=10, 
         line_color='grey', fill_color='tomato', legend_label="Place of Death", source=source, view=view)

# Creating a hover tool to display additional information on the point everytime a mouse hovers over it.
hover = HoverTool()
hover.tooltips = [
    ("First", "@First"),
    ("Surname", "@Surname"),
    ("Profession", "@Profession"),
    ("Date of Birth", "@{Date of Birth}"),
    ("Date of Death", "@{Date of Death}")
    ]
hover.mode = 'mouse'
p.add_tools(hover)

p.axis.visible = False

# Displaying the map
inputs = widgetbox(citizenship_select, deathcause_select, sex_select, birthdate_slider, deathdate_slider)

'''
Depending on whether you want to display the map in an output html file or print out the html source
code for the map, you either want to comment out the show() command and uncomment the html and print lines
to print the html code or vice versa.

!! Make sure both options aren't uncommented at the same time !!
'''

# Uncomment this line to show the map directly in an html file.
show(row(inputs, p, width=300))

# Uncomment these two lines to output the html code for the map (used to embed the map in Omeka)
#html = file_html(row(inputs, p), CDN, "WiP Map")
#print(html)