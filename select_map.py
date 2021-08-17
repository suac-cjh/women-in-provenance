import pandas as pd
from bokeh.layouts import gridplot
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource, CDSView, BooleanFilter
from bokeh.models.tools import HoverTool
from bokeh.tile_providers import get_provider
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

df = pd.read_csv("main.csv")
df = df.fillna("")

df["Birth_lon"], df["Birth_lat"] = zip(
    *df.apply(lambda x: Loc_to_LongLat(x["Place of Birth"]), axis=1))

df["Death_lon"], df["Death_lat"] = zip(
    *df.apply(lambda x: Loc_to_LongLat(x["Place of Death"]), axis=1))

df["Birth_E"], df["Birth_N"] = zip(
    *df.apply(lambda x: LongLat_to_EN(x['Birth_lon'], x['Birth_lat']), axis=1))

df["Death_E"], df["Death_N"] = zip(
    *df.apply(lambda x: LongLat_to_EN(x['Death_lon'], x['Death_lat']), axis=1))

source = ColumnDataSource(df)

booleans = [True if "Greece" in Citizenship_val else False for Citizenship_val in source.data["Citizenship"]]
view = CDSView(source=source, filters=[BooleanFilter(booleans)])

p = figure(plot_width=1000, plot_height=650, title="Map", 
	x_range = (-18706892.5544, 21289852.6142), y_range = (-7631472.9040, 12797393.0236))
provider = get_provider('CARTODBPOSITRON')
p.add_tile(provider)
p.circle(x='Birth_E', y='Birth_N', size=10, 
         line_color='grey', fill_color='royalblue', legend_label="Place of Birth", source=source, view=view)

p2 = figure(plot_width=1000, plot_height=650, title="Map", 
	x_range = (-18706892.5544, 21289852.6142), y_range = (-7631472.9040, 12797393.0236))
provider = get_provider('CARTODBPOSITRON')
p2.add_tile(provider)

p2.circle(x='Birth_E', y='Birth_N', size=10, 
         line_color='grey', fill_color='royalblue', legend_label="Place of Birth", source=source)

hover = HoverTool()
hover.tooltips = [
    ("First", "@First"),
    ("Citizenship", "@Citizenship")
    ]
hover.mode = 'mouse'
p.add_tools(hover)
p2.add_tools(hover)

show(gridplot([[p, p2]]))