HRLDAS Hourly to Daily Mean Conversion Script


This Python script processes hourly NetCDF files from the HRLDAS model output and computes daily mean values of Snow Water Equivalent (SNEQV). The final output is saved as a NetCDF file containing daily mean values over a specified date range.

Features Converts hourly HRLDAS NetCDF files into daily mean NetCDF files. Allows users to define custom start and end dates. Automatically selects the SNEQV variable for processing. Handles missing files and warns users.

Uses xarray for efficient NetCDF processing. Saves output in NetCDF format with proper time dimensions.
