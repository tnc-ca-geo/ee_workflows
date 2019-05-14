"""
Split a shapefile in smaller parts
"""
# standard library
from argparse import ArgumentParser
import os
import shutil
from zipfile import ZipFile
# third party
import fiona


def ensure_directories(dirname):
    try:
        os.makedirs(dirname)
    except FileExistsError:
        pass


def get_meta(filename):
    """
    Return meta data from shapefile
    """
    with fiona.open(filename) as collection:
        return collection.meta


def get_new_filename(old_filename, index, directory):
    """
    Creates the new filename
    """
    snippet = os.path.splitext(os.path.basename(old_filename))[0]
    new_name = '{}_{:03d}.shp'.format(snippet, index)
    new_dir = os.path.join(directory, snippet)
    ensure_directories(new_dir)
    return os.path.join(new_dir, new_name)


def remove_old_output(filename, directory):
    snippet = os.path.splitext(os.path.basename(filename))[0]
    new_dir = os.path.join(directory, snippet)
    try:
        shutil.rmtree(new_dir)
    except FileNotFoundError:
        pass


def zip_shapefile(mainpartname):
    directory, basename = os.path.split(mainpartname)
    snippet, extension = os.path.splitext(basename)
    zipfilename = os.path.join(directory, snippet + '.zip')
    with ZipFile(zipfilename, 'w') as zipf:
        for item in ['cpg', 'dbf', 'prj', 'shp', 'shx']:
            basename = '{}.{}'.format(snippet, item)
            part = os.path.join(directory, basename)
            zipf.write(part, arcname=basename)
            os.remove(part)
    print(zipfilename, 'created')


def main(filename, outdir, number):
    remove_old_output(filename, outdir)
    meta = get_meta(filename)
    index = 0
    ct = 0
    file_index = -1
    out = None
    with fiona.open(filename) as collection:
        for item in collection:
            if not out or not ct % number:
                if out:
                    out.close()
                    zip_shapefile(out_path)
                file_index += 1
                out_path = get_new_filename(filename, file_index, outdir)
                out = fiona.open(out_path, 'w', **collection.meta)
            out.write(item)
            ct += 1
    # wrap up unfinished business
    out.close()
    zip_shapefile(out_path)


if __name__ == '__main__':
    default_output_location = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', '..', 'ee_data'))
    desc = 'Break a shapefile in smaller parts'
    parser = ArgumentParser(description=desc)
    parser.add_argument(
        '-f', '--shapefilename', help='Shapefile name', type=str,
        default='example.shp')
    parser.add_argument(
        '-o', '--outputfolder', help='Folder for output files',
        type=str, default=default_output_location)
    parser.add_argument(
        '-n', '--number', help='Maximum number of features in new files',
        type=int, default=2)
    args = parser.parse_args()
    main(args.shapefilename, args.outputfolder, args.number)
