# Municipality

### Description

This program takes a csv input file and processes 

### Python version

Make sure you have Python 3 installed.

### Requires the python library shapely to be installed

To install shapely run the command `pip install shapely` before running the program.

### Command line Arguments

You can supply some command line arguments to make processing the data easier -- most notabily is the `--lat` and `--long` commands for specifying column names for those two fields and '--threshold' for catching locations that are too close to the boundary line -- distance is in feet to the outer of the boundary.

```
usage: Municipality [-h] [--lat LAT] [--long LONG] [--out OUT] [--in IN]
                    [--threshold THRESHOLD]

optional arguments:
  -h, --help            show this help message and exit
  --lat LAT             Column name for latittude - default is 'LATITUDE'
  --long LONG           Column name for longitude - default is 'LONGITUDE'
  --out OUT             Output CSV file to write data to - default is
                        'output.csv'
  --in IN               Input CSV file with lat/long data - default is
                        'data.csv'
  --threshold THRESHOLD
                        Theshold sets the maximum distance (in feet) to the
                        boundary to tigger a manual entry - default is 1000
                        feet
```

