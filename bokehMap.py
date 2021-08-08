import pandas as pd
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource, Range1d
from bokeh.layouts import layout
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

df["lon"], df["lat"] = zip(
    *df.apply(lambda x: Loc_to_LongLat(x["Place of Birth"]), axis=1))

df["E"], df["N"] = zip(
    *df.apply(lambda x: LongLat_to_EN(x['lon'], x['lat']), axis=1))

grouped = df.groupby(['E', "N"])["First"].sum().reset_index()
source = ColumnDataSource(grouped)

p = figure(plot_width=1000, plot_height=650)
provider = get_provider('CARTODBPOSITRON')
p.add_tile(provider)

p.circle(x='E', y='N', source=source, size=10, line_color='grey', fill_color='lightblue')

p.axis.visible = False

show(p)
