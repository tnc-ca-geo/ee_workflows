# Extract zonal statistics using a local shapefile and an EarthEngine image

[Setup and activate environment](../README.md)

An important reason for these somewhat convoluted workflows is getting around
Earthengine's rate limits by reducing the size of single requests, memory required 
by the resulting calculations, or limits on the response size. The EarthEngine is a 
RESTful API after all. The major limits to the EarthEngine are:

- max 3 requests per second
- max 5000 features for reductions
- max 1GB internal memory usage
- max 15 Gbytes storage for assets
- max 1MB response size

If one of these limits is hit, the request will fail. In other words, 5000
features can be still too much if the resulting EarthEngine operations will
hit the memory limit or the response is too large. 

### Step 1 (both variants): Authenticate against the EarthEngine

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


## A) Simple extract

The simple extract iterates over a local shapefile, serializes the geometry to GeoJSON
and requests statistics one by one. Only 2 to 3 features can be processed per second due to 
the limit on the number of request. The good news is that the EarthEngine Python API will 
manage this rate itself and automatically perform backoff. An advantage of this approach is 
that no assets need to be created and most of the processing can be done without even 
logging on to the EE website. 

You just need to run:

```
python simple.py -f {shapefilename}.shp -c {columnname}
```

Arguments:

  -f, --shapefilename, default=example.shp: A shapefile name
  
  -c, --column, default=gde: An feature identifying column that will appear in CSV
  
  -s, --start, default=2009: A start date, only used when the image can be crated for a time range
  
  -e, --end, default=2018: An end date (unused in the image used in the example)
  
  -h, --help: simple help


If you want to store the resulting output to a file use a simple carrot (```>```):

```
python simple.py -f example.shp > output.csv
```

The output format will be CSV with the value of the identifying column in the first column 
and all bands of the image provided as CSV columns.

## B) Extract using feature assets

### Step 2) Divide the input shape in smaller pieces and zip for upload

If the input shapefile has more than 5000 features it needs to be divided up to work 
with the ```.reduceRegions``` method of EarthEngine. It could be also necessary to use even
lower feature counts if the EarthEngine runs out of memory or the response would be too big. 
All three cases would cause an error message.

In order to do so run:

```
python split_shapefile.py -f {shapefilename}.shp -n {number of features per file}
```

Arguments:

-f, --shapefilename, default=example.shp: A shapefile name

-n, --number, default=2, number of features in the output files

-o, outputfolder, default='../../ee_data/', Output folder. By default a folder ee_data will be created next to the folder that contains the github repo

The default number of features is very low (2) so that the script can be test run with the provided example file.

```
python split_shapefile.py -f example.shp
```

Should create a folder structure like this

raster_extract

```
| --- raster_extract
|     | --- you are here
|
| --- ee_data
      | --- example
            | --- example_000.zip
            | --- example_001.zip
            | --- example_002.zip
            | --- example_003.zip
            | --- example_004.zip
```

### Step 3: Upload to Google Earthengine

#### Step 3a: Manual upload

Log into the Google Earthengine using the same account used for running the scripts: https://code.earthengine.google.com/.
In the asset tabb on the left side, create a new asset folder. This is important since the script will pick up all assets in that folder to run the extraction. It is also important to provide the asset location on the command line. Finally, it makes it easer to clean up the assets in order to preserve space with the 15GB storage limit. **Please double check that this location does not conflict with existing assets in the account**.

The scripts following the convention to name that folder after the shapefile without the .shp extension. For the example file provided in the repository and our Earthengine account the asset folder would be ```user/carogistnc/example``` 







