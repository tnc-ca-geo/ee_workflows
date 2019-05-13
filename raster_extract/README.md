# Extract zonal statistics using a local shapefile and an EarthEngine image

[Setup and activate environment](../README.md)

An important reason for this somewhat convoluted workflow is to get around some
of Earthengine's rate limit by reducing the size of single requests. The major
limits to the EarthEngine are:

- max 3 requests per second
- max 5000 features for reductions over features
- max 1MB internal memory usage
- max 15 Gbytes storage for assets

#### Step 1 (both variants): Authenticate against the EarthEngine

- in the terminal and the conda environment activated type

  ```
  earthengine authenticate
  ```
  
  A browser window should open and ask you to look in into Google. You need to use an 
  Google account that is authorized to use Google Earthengine. You can obtain this access
  relative easily: https://signup.earthengine.google.com/#!/
  
  However, the GDE images rely on assets by Ian Housman that are shared with carogis.tnc@gmail.com. 
  For this reason you need to use this account to run the examples in this repository. I will 
  provide the password on a different channel. 

  Once you logged in, you should see an authorization code to copy in the dialog on the command line.
  Now your machine is authorized to use Google Earthengine.


A) Simple extract

The simple extract iterates over a local shapefile, serializes the geometry to a GeoJSON
and requests statistics one by one. Only 2 to 3 features can be processed in a second. An
advantage is that no assets need to be created and most processing can be done without even 
going to the EE website. Just run:

```
simple.py -f shapefilename.shp -c columnname
```

Arguments:

  -f, --shapefilename, default=example.shp: A shapefile name
  
  -c, --column, default=gde: An feature identifying column that will appear in CSV
  
  -s, --start, default=2009: A start date, only used when the image can be crated for a time range
  
  -e, --end, default=2018: An end date (unused in the image used in the example)
  
  -h, --help: simple help
