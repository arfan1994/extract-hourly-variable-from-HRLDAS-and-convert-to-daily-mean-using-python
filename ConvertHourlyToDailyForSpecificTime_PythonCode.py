# -*- coding: utf-8 -*-
import xarray as xr
import numpy as np
import pandas as pd
import os
import glob

# Define the start and end date (YYYYMMDD format)
start_date = "20171101"  # Modify as needed
end_date = "20180131"    # Modify as needed

# Path to the directory containing the input hourly NetCDF files
input_dir = "/glade/derecho/scratch/aarshad/HRLDASOUT/CONUS404_ronnierun/"

# Path to save the final output daily NetCDF file
output_nc = f"{input_dir}/SNEQV_daily_WY2018.nc"

# Generate list of dates within range
date_range = pd.date_range(start=start_date, end=end_date, freq="D").strftime("%Y%m%d")

# List to store daily datasets
daily_datasets = []

# Process each day by grouping all hourly files (24 expected)
for date in date_range:
    print(f"Processing date: {date}...")

    # Find all hourly files for the given date
    daily_files = sorted(glob.glob(f"{input_dir}{date}??.LDASOUT_DOMAIN1"))  # ?? ensures 00-23 format

    if len(daily_files) < 1:  # Ensure we have at least some files
        print(f"? Warning: No files found for {date}. Skipping...")
        continue

    print(f"? Found {len(daily_files)} files for {date}")

    # Open all available hourly files (use combine='nested' for time stacking)
    try:
        ds = xr.open_mfdataset(daily_files, combine="nested", concat_dim="Time", engine="netcdf4")
    except Exception as e:
        print(f"? Error opening files for {date}: {e}")
        continue

    # Select only the SNEQV variable
    if "SNEQV" not in ds.variables:
        print(f"? Warning: 'SNEQV' variable not found in files for {date}. Skipping...")
        continue

    sneqv = ds["SNEQV"]

    # Compute daily mean over available hourly steps
    sneqv_daily_mean = sneqv.mean(dim="Time")

    # Assign correct time coordinate
    date_obj = pd.to_datetime(date, format="%Y%m%d")
    sneqv_daily_mean = sneqv_daily_mean.expand_dims(dim="time")  # Add time dimension
    sneqv_daily_mean = sneqv_daily_mean.assign_coords(time=[date_obj])

    # Append to list
    daily_datasets.append(sneqv_daily_mean)

# Combine all daily datasets along the time dimension
if daily_datasets:
    final_ds = xr.concat(daily_datasets, dim="time")

    # Update attributes
    final_ds.attrs["description"] = "Daily mean of Snow Water Equivalent (SNEQV)"
    final_ds.attrs["units"] = "mm"

    # Save to NetCDF file
    final_ds.to_netcdf(output_nc)
    print(f"? Final Daily Mean File Saved: {output_nc}")
else:
    print("? No valid files found. No NetCDF file was generated.")
