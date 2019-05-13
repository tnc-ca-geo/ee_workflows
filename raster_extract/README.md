# Extract zonal statistics using a local shapefile and an EarthEngine image

[Setup and activate environment](../README.md)

An important reason for this somewhat convoluted workflow is to get around some
of Earthengine's rate limit by reducing the size of single requests. The major
limits to the EarthEngine are:

- max 3 requests per second
- max 5000 features for reductions over features
- max 1MB internal memory usage
- max 15 Gbytes storage for assets

A) Simple extract

The simple extract iterates over a local shapefile, serializes the geometry to a GeoJSON
and requests statistics one by one. Only 2 to 3 features can be processed in a second. An
advantage is that no assets need to be created and most processing can be done without even 
going to the EE website. Just run:

```
simple.py -f shapefilename.shp -c columnname
```

Arguments:

  -f, --shapefilename, default=example.shp
  
  -c, --column, default=gde
  
  -s, --start, default=2009
  
  -e, --end, default=2018

