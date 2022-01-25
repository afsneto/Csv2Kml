# -*- coding: utf-8 -*-
"""
Spyder Editor

Este é um arquivo de script temporário.
"""

# Convert UTM coordinates points to kml file

import csv
import simplekml
import math as mt
from tqdm import tqdm


class convertgeo:
    def __init__(self):
        self.Datums = {'WGS84': {'a': 6378137, 'b': 6356752.3142,
                                 'f': 0.00335281066474748, '1/f': 298.257223563}}

    def utm2geodeg(self, x, y, zone, point_name='ID', datum='WGS84'):
        # Datum constants for WGS 84
        # e = eccentricity
        e = mt.sqrt(1 - (self.Datums[datum]['b'] /
                         self.Datums[datum]['a']) ** 2)
        e2 = e*e/(1-e*e)
        k0 = 0.9996
        if zone < 0:
            northing = 10000000 - y
        else:
            northing = y
        easting = x
        if zone >= 1 or zone <= 60:
            zone_cm = 6 * abs(zone) - 183
        else:
            zone_cm = 3  # for zone = 31

        # Calculate footprint latitude
        arc_length = northing/k0
        mu = arc_length / \
            (self.Datums[datum]['a'] * (1 - e ** 2 /
                                        4 - 3 * e ** 4 / 64 - 5 * e ** 6 / 256))
        e1 = (1-(1-e*e)**(1/2))/(1+(1-e*e)**(1/2))
        C1 = 3*e1/2-27*e1**3/32
        C2 = 21*e1**2/16-55*e1**4/32
        C3 = 151*e1**3/96
        C4 = 1097*e1**4/512
        footprint_lat = mu+C1 * \
            mt.sin(2*mu)+C2*mt.sin(4*mu)+C3*mt.sin(6*mu)+C4*mt.sin(8*mu)

        # Constants for formulas
        Q0 = e2*mt.cos(footprint_lat)**2
        t0 = mt.tan(footprint_lat)**2
        n0 = self.Datums[datum]['a'] / \
            (1 - (e2 * mt.sin(footprint_lat) ** 2)) ** (1 / 2)
        r0 = self.Datums[datum]['a'] * (1 - e2 * e2) / \
            (1 - (e2 * mt.sin(footprint_lat)) ** 2) ** (3 / 2)
        dd0 = (500000-easting)/(n0*k0)

        # Coefficients for Calculating Latitude
        fact1 = n0*mt.tan(footprint_lat)/r0
        fact2 = dd0*dd0/2
        fact3 = (5+3*t0+10*Q0-4*Q0*Q0-9*e2)*dd0**4/24
        fact4 = (61+90*t0+298*Q0+45*t0*t0-252*e2-3*Q0*Q0)*dd0**6/720

        # Coefficients for Calculating Longitude
        lof1 = dd0
        lof2 = (1+2*t0+Q0)*dd0**3/6
        lof3 = (5-2*Q0+28*t0-3*Q0**2+8*e2+24*t0**2)*dd0**5/120

        # Geographic decimal
        delta_long = (lof1-lof2+lof3)/mt.cos(footprint_lat)
        delta_long_dec = mt.degrees(delta_long)
        if zone < 0:
            latitude = -(mt.degrees(footprint_lat-fact1*(fact2+fact3+fact4)))
        else:
            latitude = mt.degrees(footprint_lat-fact1*(fact2+fact3+fact4))
        longitude = zone_cm - delta_long_dec

        return point_name, latitude, longitude

    # print(utm2geodeg(170847.624, 9197028.368, -25, 'ID', 'WGS 84'))

    # Reading csv file

    def csv2kml(self, file_input, file_output, tl_name, datum='WGS84'):
        input_file = csv.reader(open(file_input + '.csv', 'r'))
        # input_file = csv.reader(open(file_input, 'r'))
        points = []
        for row in input_file:
            points.append(self.utm2geodeg(float(row[1]), float(
                row[2]), float(row[3]), str(row[0]), datum))

        # Building kml file
        kml = simplekml.Kml()
        points2ls = []

        style = simplekml.Style()
        style.iconstyle.icon.href = "http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png"

        for point in tqdm(points):
            pnt = kml.newpoint(name=point[0], coords=[(point[2], point[1])])
            points2ls.append((point[2], point[1]))
            pnt.style = style

        ls = kml.newlinestring(name=tl_name, coords=points2ls)
        ls.style.linestyle.width = 2
        ls.style.linestyle.color = simplekml.Color.blue

        kml.save(file_output+'.kml')

    def justpoints(self, file_input, file_output, tl_name, datum='WGS84'):
        input_file = csv.reader(open(file_input, 'r'))
        points = []
        for row in input_file:
            points.append(self.utm2geodeg(float(row[1]), float(
                row[2]), float(row[3]), str(row[0]), datum))

        # Building kml file
        kml = simplekml.Kml()
        style = simplekml.Style()
        style.iconstyle.icon.href = "http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png"
        for point in tqdm(points):
            pnt = kml.newpoint(name=point[0], coords=[(point[2], point[1])])
            pnt.style = style

        kml.save(file_output+'.kml')
