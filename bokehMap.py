import pandas as pd
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource, Range1d
from bokeh.layouts import layout
from bokeh.tile_providers import get_provider
from bokeh.models.tools import HoverTool
from geopy.geocoders import Nominatim
from pyproj import Transformer

output_file('birth_map.html')

def Loc_to_LongLat(location):
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

df = pd.read_csv("all_people.csv")
df = df.fillna("")

df["Birth_lon"], df["Birth_lat"] = zip(
    *df.apply(lambda x: Loc_to_LongLat(x["Place of Birth"]), axis=1))

df["Death_lon"], df["Death_lat"] = zip(
    *df.apply(lambda x: Loc_to_LongLat(x["Place of Death"]), axis=1))

df["Birth_E"], df["Birth_N"] = zip(
    *df.apply(lambda x: LongLat_to_EN(x['Birth_lon'], x['Birth_lat']), axis=1))

df["Death_E"], df["Death_N"] = zip(
    *df.apply(lambda x: LongLat_to_EN(x['Death_lon'], x['Death_lat']), axis=1))

grouped = df.groupby(['Birth_E', "Birth_N", "Death_E", "Death_N", "Profession", "Surname", "Date of Birth", "Date of Death"])["First"].sum().reset_index()
source = ColumnDataSource(grouped)

p = figure(plot_width=1000, plot_height=650)
provider = get_provider('CARTODBPOSITRON')
p.add_tile(provider)

p.circle(x='Birth_E', y='Birth_N', source=source, size=10, line_color='grey', fill_color='royalblue', legend_label="Place of Birth")
p.circle(x='Death_E', y='Death_N', source=source, size=10, line_color='grey', fill_color='tomato', legend_label="Place of Death")

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

show(p)
