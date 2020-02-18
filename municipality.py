import json
import csv
import argparse

from shapely.geometry import shape, Point
from decimal import Decimal


DEGREES_TO_MILES = 69
THRESHOLD = 0.189394  #1000 feet converted into miles

parser = argparse.ArgumentParser(prog='Municipality')
parser.add_argument('--lat', default="LATITUDE", help="Column name for latittude - default is 'LATITUDE'")
parser.add_argument('--long', default="LONGITUDE", help="Column name for longitude - default is 'LONGITUDE'")
parser.add_argument('--out', default="output.csv", help="Output CSV file to write data to - default is 'output.csv'")
parser.add_argument('--in', default="data.csv", help="Input CSV file with lat/long data - default is 'data.csv'")
parser.add_argument('--threshold', default=1000, help="Theshold sets the maximum distance (in feet) to the boundary to tigger a manual entry - default is 1000 feet")

args = vars(parser.parse_args())

LATITUDE = args['lat']
LONGITUDE = args['long']
IN_FILE = args['in']
OUT_FILE = args['out']
THRESHOLD =  Decimal(args['threshold']) / Decimal(5280)

def coordinatesConvert(point):
    '''Params: point - tuple of long, lat'''
    f = open('./Municipality.geojson', 'r')
    js = json.load(f)
    f.close()
    for boundary in js['features']:
        test = shape(boundary['geometry'])
        if Point(point).within(test):
            return (boundary['properties']['NAME'], test.exterior.distance(Point(point)))
    return ()


def coordToCode(latitude, longitude):
    result = coordinatesConvert( (longitude, latitude) )
    if result is ():
        return {'error': "NOT FOUND"}
    code, distance = result
    if distance * DEGREES_TO_MILES > THRESHOLD:
        return {'success': code}
    else:
        return {'success': "MANUAL ENTRY"}


def readAndWriteCSV():
    NONE_COUNT = 0
    TOO_CLOSE_TO_CALL_COUNT = 0
    TOTAL_RECORDS = 0
    with open(OUT_FILE, 'w') as outfile:
        outfile_writer = csv.DictWriter(outfile, fieldnames="")
        with open(IN_FILE) as csvfile:
            reader = csv.DictReader(csvfile)
            header = reader.fieldnames
            header.append("COUNTY CODE")
            outfile_writer.fieldnames = header
            outfile_writer.writeheader()
            for row in reader:
                TOTAL_RECORDS = TOTAL_RECORDS + 1
                latitude = Decimal(row[LATITUDE].strip())
                longitude = Decimal(row[LONGITUDE].strip())
                result = coordToCode(latitude, longitude)
                if 'error' in result.keys():
                    row['COUNTY CODE'] = "NOT FOUND"
                    NONE_COUNT = NONE_COUNT + 1
                if 'success' in result.keys():
                    row['COUNTY CODE'] = result['success']
                    if result['success'] == 'MANUAL ENTRY':
                        TOO_CLOSE_TO_CALL_COUNT = TOO_CLOSE_TO_CALL_COUNT + 1
                outfile_writer.writerow(row)
            
            print("FINISHED READING FROM FILE")
            print("Total Records Read: ", TOTAL_RECORDS)
            print("Records not in Centre County: ", NONE_COUNT)
            print("Too Close to Call: ", TOO_CLOSE_TO_CALL_COUNT)






readAndWriteCSV()