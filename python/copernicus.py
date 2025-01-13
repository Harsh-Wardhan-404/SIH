# import copernicusmarine
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np


ds = xr.open_dataset('C:/SIH/python/data/cmems_mod_glo_wav_anfc_0.083deg_PT3H-i_202311/2024/08/mfwamglocep_2024081500_R20240816_00H.nc', engine='netcdf4')



specific_time = '2024-08-16T00:00:00'
wave_height_at_time = ds['VHM0'].sel(time=specific_time, method='nearest')
grid_res = 1.0
# print(ds.VHM0)

# specific_time = '2024-08-28T13:00:00'
# wave_height_at_time = ds['VHM0'].sel(time=specific_time, method='nearest')

# # Create a figure and axis with a map projection
# fig = plt.figure(figsize=(12, 6))
# ax = plt.axes(projection=ccrs.PlateCarree())

# # Add coastlines and other map features
# ax.coastlines()
# ax.add_feature(cfeature.BORDERS, linestyle=':')
# ax.add_feature(cfeature.LAND, color='lightgray')

# # Plot the data
# wave_height_at_time.plot(ax=ax, cmap='viridis', transform=ccrs.PlateCarree())

# # Add a title with the specific date
# plt.title(f'Significant Wave Height (VHM0) on {specific_time}')

# # Show the plot
# plt.show()

# Select the data for a specific time
lon_bins = np.arange(-180, 180 + grid_res, grid_res)
lat_bins = np.arange(-90, 90 + grid_res, grid_res)
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
plt.contourf(lon_centers, lat_centers, gridded_wave_height, cmap='viridis', transform=ccrs.PlateCarree())

# Add a color bar
plt.colorbar(label='Wave Height (VHM0)')

# Add a title
plt.title(f'Significant Wave Height (VHM0) on {specific_time}')

# Show the plot
plt.show()