import folium
import geopandas as gpd
from shapely.geometry import box
import numpy as np
import matplotlib.pyplot as plt

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

# Example: Assigning a value to each grid cell based on some algorithm
# Here we will use a simple count of how many features intersect with the grid cell
grid_gdf['value'] = 0

for idx, grid in grid_gdf.iterrows():
    intersecting_features = gdf[gdf.geometry.intersects(grid.geometry)]
    # You can replace this with any calculation based on your algorithm
    grid_gdf.at[idx, 'value'] = len(intersecting_features)

# Normalize values for color mapping
min_value = grid_gdf['value'].min()
max_value = grid_gdf['value'].max()

# Create a base map centered around the area of interest
m = folium.Map(location=[(miny + maxy) / 2, (minx + maxx) / 2], zoom_start=6)

# Add the GeoJSON data to the map
folium.GeoJson(gdf).add_to(m)

# Add the grid to the map with color representation based on value
for _, row in grid_gdf.iterrows():
    bounds = list(row['geometry'].bounds)
    color = plt.cm.viridis((row['value'] - min_value) / (max_value - min_value))[:3]
    color = f'#{int(color[0]*255):02x}{int(color[1]*255):02x}{int(color[2]*255):02x}'

    folium.Rectangle(
        bounds=[(bounds[1], bounds[0]), (bounds[3], bounds[2])],
        color=color, fill=True, fill_opacity=0.6, popup=f'Value: {row["value"]}'
    ).add_to(m)

# Display the map
m.save("interactive_grid_map.html")

