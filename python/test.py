import folium
import geopandas as gpd
from shapely.geometry import box
import numpy as np

# Load the GeoJSON data
gdf = gpd.read_file('test.json')

# Define the bounding box for the grid (xmin, ymin, xmax, ymax)
minx, miny, maxx, maxy = gdf.total_bounds

# Define the grid size
grid_size = 0.5  # Adjust the grid size (in degrees) as needed

# Generate grid cells
grid_cells = []
x_range = np.arange(minx, maxx, grid_size)
y_range = np.arange(miny, maxy, grid_size)
for x in x_range:
    for y in y_range:
        grid_cells.append(box(x, y, x + grid_size, y + grid_size))

# Convert grid cells to a GeoDataFrame
grid_gdf = gpd.GeoDataFrame({'geometry': grid_cells}, crs=gdf.crs)

# Create a base map centered around the area of interest
m = folium.Map(location=[(miny + maxy) / 2, (minx + maxx) / 2], zoom_start=6)

# Add the GeoJSON data to the map
folium.GeoJson(gdf).add_to(m)

# Add the grid to the map
for _, row in grid_gdf.iterrows():
    bounds = list(row['geometry'].bounds)
    folium.Rectangle(
        bounds=[(bounds[1], bounds[0]), (bounds[3], bounds[2])],
        color='red', fill=False
    ).add_to(m)

# Display the map
m.save("map_with_grid.html")

