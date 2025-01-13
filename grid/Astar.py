# import xarray as xr
# import numpy as np
# import matplotlib.pyplot as plt
# from mpl_toolkits.basemap import Basemap

# # Load your NetCDF dataset
# ds = xr.open_dataset('C:/SIH/grid/cmems_mod_glo_wav_anfc_0.083deg_PT3H-i_1725368024903.nc', engine='netcdf4')

# # Define specific time for the wave height
# specific_time = '2024-09-16T04:00:00'
# wave_height_at_time = ds['VHM0'].sel(time=specific_time, method='nearest')

# # Define longitude and latitude bins based on the dataset's bounds
# lon_centers = wave_height_at_time['longitude'].values
# lat_centers = wave_height_at_time['latitude'].values

# # Convert to 2D grid (since the dataset is already gridded, this is straightforward)
# wave_height_grid = wave_height_at_time.values

# # Create a heatmap
# plt.figure(figsize=(10, 8))
# plt.pcolormesh(lon_centers, lat_centers, wave_height_grid, shading='auto', cmap='viridis')
# plt.colorbar(label='Wave Height (m)')
# plt.xlabel('Longitude')
# plt.ylabel('Latitude')
# plt.title('Wave Height Heatmap')
# plt.show()


#--------------------------------------------------------------------------------------Above code return lat, long, cost --------------------------------------------------------------------------

import xarray as xr
import numpy as np
import heapq
import folium

# Load your NetCDF dataset
ds = xr.open_dataset('C:/SIH/grid/cmems_mod_glo_wav_anfc_0.083deg_PT3H-i_1725368024903.nc', engine='netcdf4')

# Define specific time for the wave height
specific_time = '2024-09-16T04:00:00'
wave_height_at_time = ds['VHM0'].sel(time=specific_time, method='nearest')

# Extract grid information
wave_height_grid = wave_height_at_time.values
lat_centers = wave_height_at_time['latitude'].values
lon_centers = wave_height_at_time['longitude'].values

# Source and Destination Coordinates
source_lat, source_lon = 5.21, 78.42  # Replace with your source coordinates
dest_lat, dest_lon = -24.07, 111.92  # Replace with your destination coordinates

# Function to find the nearest grid index
def find_nearest_index(array, value):
    return np.abs(array - value).argmin()

# Get the grid indices for the source and destination
start_y = find_nearest_index(lat_centers, source_lat)
start_x = find_nearest_index(lon_centers, source_lon)
end_y = find_nearest_index(lat_centers, dest_lat)
end_x = find_nearest_index(lon_centers, dest_lon)

# Custom A* Implementation
def heuristic(a, b):
    return np.linalg.norm(np.array(a) - np.array(b))

def astar(array, start, goal):
    neighbors = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    close_set = set()
    came_from = {}
    gscore = {start: 0}
    fscore = {start: heuristic(start, goal)}
    oheap = []

    heapq.heappush(oheap, (fscore[start], start))

    while oheap:
        current = heapq.heappop(oheap)[1]

        if current == goal:
            data = []
            while current in came_from:
                data.append(current)
                current = came_from[current]
            return data

        close_set.add(current)
        for i, j in neighbors:
            neighbor = current[0] + i, current[1] + j            
            tentative_g_score = gscore[current] + array[neighbor[0]][neighbor[1]]
            if 0 <= neighbor[0] < array.shape[0]:
                if 0 <= neighbor[1] < array.shape[1]:                
                    if neighbor in close_set:
                        continue
                    if neighbor not in [i[1] for i in oheap]:
                        came_from[neighbor] = current
                        gscore[neighbor] = tentative_g_score
                        fscore[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                        heapq.heappush(oheap, (fscore[neighbor], neighbor))
                    elif tentative_g_score >= gscore.get(neighbor, 0):
                        continue

    return False

# Run the custom A* algorithm
start = (start_y, start_x)
end = (end_y, end_x)
path = astar(wave_height_grid, start, end)

# Extract the lat/lon of the path
if path:
    path_coords = [(lat_centers[y], lon_centers[x]) for y, x in path]

    # Create a Folium map centered on the middle of the path
    map_center = [np.mean([coord[0] for coord in path_coords]), np.mean([coord[1] for coord in path_coords])]
    m = folium.Map(location=map_center, zoom_start=6)

    # Add the path to the map
    folium.PolyLine(locations=path_coords, color='red', weight=5, opacity=0.8).add_to(m)

    # Display the map
    m.save("optimal_path_map.html")
    m
else:
    print("No path found!")
