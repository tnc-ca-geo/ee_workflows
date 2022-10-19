"""
Simple extract of zonal statistics from Google EarthEngine. This script
can only process two to three features per second due to EarthEngine
rate limits. On the other hand it is very easy to use and does not depend
on any setup on the EarthEngine itself.
"""
# standard library
from argparse import ArgumentParser
import json
import time
# third party
import ee
import fiona
from fiona.transform import transform_geom
# project
from images import medoid_image


def shapefile_generator(filename):
    """
    A generator that iterates over records in a shapefile
    """
    with fiona.open(filename) as collection:
        for item in collection:
            item['geometry'] = transform_geom(
                collection.meta['crs'], 'epsg:4326', item['geometry'])
            yield item


def main(filename, column, startyear, endyear):
    """
    For each year in range, iterate over features and run reduceRegion
    """
    ee.Initialize()
    first = True
    year_range = list(range(startyear, endyear + 1))
    for year in year_range:
        image_med = medoid_image(year)
        for feature in shapefile_generator(filename):
            invocation_med = image_med.reduceRegion(
                ee.Reducer.mean(), ee.Geometry(feature['geometry']), scale=30)
            res_med = invocation_med.getInfo()
            if first:
                header = [column] + [item for item in res_med] + ['year']
                print(','.join(header))
                first = False
            line = [
                feature['properties'][column]] + [res_med[item] for item in res_med] + [year]
            line = [str(item) for item in line]
            print(','.join(line))
    #print_metadata
    image_meta = medoid_image(startyear)
    properties = image_meta.propertyNames()
    print('Metadata properties:',properties.getInfo()) #ee.List of metadata properties


if __name__ == '__main__':
    desc = 'Extract zonal stats by an image name and a shapefile'
    parser = ArgumentParser(description=desc)
    parser.add_argument(
        '-f', '--shapefilename', help='Shapefile name', type=str,
        default='example.shp')
    parser.add_argument(
        '-c', '--column', help='Feature identifying column', type=str,
        default='MapNo')
    parser.add_argument(
        '-s', '--startyear', help='Start year', type=int, default=2018)
    parser.add_argument(
        '-e', '--endyear', help='End year', type=int, default=2020)
    args = parser.parse_args()
    main(args.shapefilename, args.column, args.startyear, args.endyear)
