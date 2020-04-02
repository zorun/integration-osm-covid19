#!/usr/bin/env python3

import csv
import os
import sys

def usage():
    print("usage: {} <dokomaps-data.csv> [all-cities.txt]\n".format(sys.argv[0]), file=sys.stderr)
    print("Split the data according to their city name as provided in the data set.", file=sys.stderr)
    print("Output are 'dokomaps-data-<city>.csv' files in the same place as the input.", file=sys.stderr)
    print("If a second argument is given, we write down all city names to this filename.", file=sys.stderr)

def main():
    if len(sys.argv) <= 1:
        usage()
        exit(-1)
    in_filename = sys.argv[1]
    # Map city name to list of rows
    subdata = dict()
    with open(in_filename) as f:
        csv_in = csv.reader(f)
        header = next(csv_in)
        for row in csv_in:
            city = row[0]
            if city not in subdata:
                subdata[city] = []
            subdata[city].append(row)
    # Prepend header to all subdata lists
    for city in subdata:
        subdata[city].insert(0, header)
    # Write down CSV for each city
    for city, rows in subdata.items():
        out_filename = os.path.splitext(in_filename)[0] + "-{}.csv".format(city)
        print("Writing {:4} rows to {}".format(len(rows)-1, out_filename), file=sys.stderr)
        with open(out_filename, "w") as out_f:
            csv_out = csv.writer(out_f)
            csv_out.writerows(rows)
    if len(sys.argv) >= 3:
        print("Writing list of cities to", sys.argv[2])
        with open(sys.argv[2], "w") as city_list:
            for city in subdata.keys():
                city_list.write(city + "\n")

if __name__ == '__main__':
    main()
