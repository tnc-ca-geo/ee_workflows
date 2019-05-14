"""
Exctract zonal statistics from an EarthEngine image using features stored as
assets in the same account
"""
# third party
from argparse import ArgumentParser
import ee
# project
from images import medoid_image


def get_header(res, column):
    fields = res['features'][0]['properties'].copy()
    fields.pop(column)
    return [column] + [field for field in fields]


def format(res, header):
    """
    Format Earthengine result to CSV
    """
    for item in res['features']:
        props = item['properties']
        yield [str(props[item]) for item in header]


def main(assetfolder, column, year):
    ee.Initialize()
    assets = ee.data.getList({'id': assetfolder})
    header = None
    for item in assets:
        fc = ee.FeatureCollection(item['id']).select(column)
        res = medoid_image(
            year).reduceRegions(
                collection=fc, reducer=ee.Reducer.mean(), scale=30).getInfo()
        if not header:
            header = get_header(res, column)
            print(','.join(header))
        for item in format(res, header):
            print(','.join(item))


if __name__ == '__main__':
    desc = 'Extract zonal stats by an image name and a feature asset'
    parser = ArgumentParser(description=desc)
    parser.add_argument(
        '-a', '--assetfolder', help='An asset folder', type=str,
        default='users/carogistnc/example')
    parser.add_argument(
        '-c', '--column', help='Feature identifying column', type=str,
        default='polygon_id')
    parser.add_argument(
        '-y', '--year', help='Start year', type=int, default=2018)
    args = parser.parse_args()
    main(args.assetfolder, args.column, args.year)
