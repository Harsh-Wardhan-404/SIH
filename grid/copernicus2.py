import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np

# Load your NetCDF dataset
ds = xr.open_dataset('C:/SIH/grid/cmems_mod_glo_wav_anfc_0.083deg_PT3H-i_1725368024903.nc', engine='netcdf4')

# Define specific time for the wave height
specific_time = '2024-09-16T04:00:00'
wave_height_at_time = ds['VHM0'].sel(time=specific_time, method='nearest')

# Get the bounds from the dataset
lon_min = ds['longitude'].min().item()
lon_max = ds['longitude'].max().item()
lat_min = ds['latitude'].min().item()
lat_max = ds['latitude'].max().item()

# Define grid resolution
grid_res = 1.0  # Adjust this value to change the grid size

# Define longitude and latitude bins based on the dataset's bounds
lon_bins = np.arange(lon_min, lon_max + grid_res, grid_res)
lat_bins = np.arange(lat_min, lat_max + grid_res, grid_res)
lon_centers = 0.5 * (lon_bins[:-1] + lon_bins[1:])
lat_centers = 0.5 * (lat_bins[:-1] + lat_bins[1:])

# Interpolate wave height data to the grid using 1D coordinates
gridded_wave_height = wave_height_at_time.interp(longitude=lon_centers, latitude=lat_centers)

# Create a figure and axis with a map projection
fig = plt.figure(figsize=(12, 6))
ax = plt.axes(projection=ccrs.PlateCarree())

# Add coastlines and other map features
ax.coastlines()
ax.add_feature(cfeature.BORDERS, linestyle=':')
ax.add_feature(cfeature.LAND, color='lightgray')

# Plot the gridded data
contour = plt.contourf(lon_centers, lat_centers, gridded_wave_height, cmap='viridis', transform=ccrs.PlateCarree())

# Add the grid to the map
for lon in lon_bins:
    ax.plot([lon, lon], [lat_bins[0], lat_bins[-1]], color='red', linewidth=0.5, transform=ccrs.PlateCarree())

for lat in lat_bins:
    ax.plot([lon_bins[0], lon_bins[-1]], [lat, lat], color='red', linewidth=0.5, transform=ccrs.PlateCarree())

# Add a color bar
plt.colorbar(label='Wave Height (VHM0)')

# Add a title
plt.title(f'Significant Wave Height (VHM0) on {specific_time}')

# Function to handle click events
def on_click(event):
    if event.inaxes is not None:
        # Get the clicked longitude and latitude
        clicked_lon, clicked_lat = event.xdata, event.ydata

        # Find the nearest grid cell center
        lon_idx = (np.abs(lon_centers - clicked_lon)).argmin()
        lat_idx = (np.abs(lat_centers - clicked_lat)).argmin()

        # Get the wave height for the nearest grid cell
        wave_height = gridded_wave_height[lat_idx, lon_idx].item()

        # Display the wave height
        print(f"Clicked at (Lon: {clicked_lon:.2f}, Lat: {clicked_lat:.2f}) - Wave Height: {wave_height:.2f} m")

        # Optionally, you can show this info on the plot
        ax.text(clicked_lon, clicked_lat, f'{wave_height:.2f} m', fontsize=12, color='black',
                bbox=dict(facecolor='white', alpha=0.6), transform=ccrs.PlateCarree())
        plt.draw()

# Connect the click event to the on_click function
cid = fig.canvas.mpl_connect('button_press_event', on_click)

# Show the plot
plt.show()
