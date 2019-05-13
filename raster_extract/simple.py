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
            item['geometry']['coordinates'] = [item['geometry']['coordinates']]
            item['geometry']['type'] = 'MultiPolygon'
            yield item


def main(filename, column, start, end):
    """
    Iterate over features and run reduceRegion
    """
    ee.Initialize()
    image = medoid_image(start)
    first = True
    for feature in shapefile_generator(filename):
        res = image.reduceRegion(
            ee.Reducer.mean(), ee.Geometry(feature['geometry'])
            ).getInfo()
        if first:
            header = [column] + [item for item in res]
            print(','.join(header))
            first = False
        line = [
            feature['properties'][column]] + [res[item] for item in res]
        line = [str(item) for item in line]
        print(','.join(line))


if __name__ == '__main__':
    desc = 'Extract zonal stats by an image name and a shapefile'
    parser = ArgumentParser(description=desc)
    parser.add_argument(
        '-f', '--shapefilename', help='Shapefile name', type=str,
        default='example.shp')
    parser.add_argument(
        '-c', '--column', help='Feature identifying column', type=str,
        default='polygon_id')
    parser.add_argument(
        '-s', '--start', help='Start year', type=int, default=2009)
    parser.add_argument(
        '-e', '--end', help='End year', type=int, default=2018)
    args = parser.parse_args()
    main(args.shapefilename, args.column, args.start, args.end)
