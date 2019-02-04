import math
from datetime import datetime
import os

def eratosthenes(timestamp, height, shadow, alt, gha, bearing, dec):
    os.system('cls' if os.name == 'nt' else 'clear')
    day_of_year = timestamp.timetuple().tm_yday
    print("Day of the year", day_of_year)
    print("UTC Timestamp = ", timestamp)

    declination = dec  #direct calculate with this function: sun_decl(day_of_year)
    co_decl = 90 - declination

    print("Sun's declination = ", declination, " deg")
    #print("Sun's co-declination = ", co_decl, " deg")
    print("Sun's GHA = ", gha, " deg")
    print("Sun's Latitude = ", convert_to_deg_min_sec(declination))
    print("Sun's Longitude = ", convert_to_deg_min_sec(gha))

    alt = 2* math.pi * (3440.0647948 + alt)
    coH = math.atan2(shadow,height)
    coH = math.degrees(coH)
    H = 90 - coH
    #print("coH = ", coH, " deg")
    #print("H = ", H, " deg")
    r = (alt / 360) * coH
    print("Distance from sun's GP = ", r, " nm")

    [Latitude, n_or_s] = my_lat(bearing, coH, co_decl)
    co_lat = float(90-Latitude)
    [Longitude, e_or_w] = my_long(coH, bearing, gha, co_lat, co_decl)


    print("Lat = ", convert_to_deg_min_sec(Latitude), n_or_s)
    print("Lng = ", convert_to_deg_min_sec(Longitude), e_or_w)

def sextant(timestamp, H_angle, alt, gha, bearing, dec):
    os.system('cls' if os.name == 'nt' else 'clear')
    day_of_year = timestamp.timetuple().tm_yday
    print("Day of the year", day_of_year)
    print("UTC Timestamp = ", timestamp)

    declination = dec  #direct calculate with this function: sun_decl(day_of_year)
    co_decl = 90 - declination

    print("Sun's declination = ", declination, " deg")
    #print("Sun's co-declination = ", co_decl, " deg")
    print("Sun's GHA = ", gha, " deg")
    print("Sun's Latitude = ", convert_to_deg_min_sec(declination))
    print("Sun's Longitude = ", convert_to_deg_min_sec(gha))

    alt = 2* math.pi * (3440.0647948 + alt)
    #coH = math.atan2(shadow,height)
    #coH = math.degrees(coH)
    #H = 90 - coH
    coH = 90 - H_angle
    #print("coH = ", coH, " deg")
    #print("H = ", H, " deg")
    r = (alt / 360) * coH
    print("Distance from sun's GP = ", r, " nm")

    [Latitude, n_or_s] = my_lat(bearing, coH, co_decl)
    co_lat = float(90-Latitude)
    [Longitude, e_or_w] = my_long(coH, bearing, gha, co_lat, co_decl)


    print("Lat = ", convert_to_deg_min_sec(Latitude), n_or_s)
    print("Lng = ", convert_to_deg_min_sec(Longitude), e_or_w)

def my_lat(bearing, coH, co_decl):
    #A = unk, a= coH
    #B= unk, b = co_lat..unk
    #C = bearing, c = co_decl

    bearing = math.radians(bearing)
    coH = math.radians(coH)
    co_decl = math.radians(co_decl)

    #Law of Sines
    A = math.asin(math.sin(coH) * math.sin(bearing) / math.sin(co_decl) )
    #print(math.degrees(A))

    #Napier's Analogies
    co_lat = 2* math.atan( (math.tan((coH + co_decl) / 2) * math.cos((A+bearing)  / 2))/ ( math.cos( (A-bearing) /2) ))

    co_lat = math.degrees(co_lat)
    #print(co_lat)
    lat = 90 - co_lat
    #print("My latitude = ", lat)
    if lat < 0:
        n_or_s = "S"
    else: n_or_s = "N"
    return abs(lat), n_or_s

def my_long(coH, bearing, gha, co_lat, co_decl):
    cobearing = float(180-bearing)
    cobearing = math.radians(cobearing)
    coH = math.radians(coH)
    co_lat = math.radians(co_lat)
    co_decl = math.radians(co_decl)

    #Law of Sines
    #a = math.asin( math.sin(cobearing) * math.sin(coH) / math.sin(math.radians(90)) )
    #a = math.asin(math.sin(cobearing) * math.sin(coH) / math.sin(co_lat))
    
    #Law of Cosines
    num = math.cos(co_lat)*math.cos(co_decl)
    den = math.sin(co_lat) * math.sin(co_decl)
    lha = math.acos(((math.cos(coH) - num) / den )) 
    lha = math.degrees(lha)
    print("LHA = ", lha)

    #East West of Observer Meridian Check
    check = input("If ths sun is East of your meridian, enter 1.  If it's West, enter 2: ")
    if check == "1":
        Longitude = lha + gha + 360
        if Longitude > 360:
            Longitude = Longitude - 360
    else:
        Longitude = gha - lha + 360
        if Longitude > 360:
            Longitude = Longitude - 360
    
    #Observer E or West of Prime Meridian?
    if Longitude > 180:
        Longitude = 360 - Longitude
        long_e_or_w = "E"
    else: long_e_or_w = "W"

    return Longitude, long_e_or_w

def sun_decl(day_of_year):

    step1 = (day_of_year - 2) * (360/365.24219)
    step1 = math.radians(step1)

    step2 = (day_of_year + 10)  * (360/365.24219)
    step2 = math.radians(step2)

    step3 = step2 + math.radians(360/math.pi)*math.radians(.0167)*math.sin(step1)
    step4 = math.cos(step3) *math.sin(math.radians(-23.44))
    step5 = math.asin(step4)

    declination = math.degrees(step5)

    #Approximations:
    #declination = math.radians(-23.44)*math.cos(math.radians((360/365) + day_of_year + 10))
    #declination = math.degrees(declination)
    #or this one:
    #declination = math.asin(math.radians(.39795) * math.cos(math.radians(0.98563) * math.radians(day_of_year - 273)) )
    #or this one:
    day_angle = 2 *math.pi * (day_of_year - 1) / 365
    declination2 = .006918 - .399912*math.cos(day_angle) + .070257 * math.sin(day_angle) - .006758*math.cos(2*day_angle) + .000907 * math.sin(2*day_angle) - .002697 * math.cos(3*day_angle) + .001480*math.sin(3*day_angle)
    print("Alternate Declination 1 = ", declination)
    print ("Alternate Declination 2= ", math.degrees(declination2))

    return declination

def convert_to_deg_min_sec(decimal_value):
    degrees = math.trunc(decimal_value)
    number_dec = decimal_value % 1
    mnt = number_dec * 60
    minutes = math.trunc(mnt)
    sec = (mnt % 1) * 60
    seconds = math.trunc(sec)
    total = str(degrees) + "deg " + str(minutes) + "min " + str(seconds) + "sec "
    return total

def sun_posit(timestamp):
    # See Pub 249 table 4 for reference and method.  Tables will need to be updated in AD 2037.

    os.system('cls' if os.name == 'nt' else 'clear')
                    # Rows are days of the month
                    # Jan            FEB      MAR    APR     MAY     JUN     JUL     AUG    SEP     OCT     NOV    DEC
    table_4_ot =  [ [ [4,12,-22,3],  [1,38,-17,16], [1,53], [3,58], [5,42], [5,35], [4,5], [3,24], [4,56], [7,31], [9,6], [7,50] ], 
                    [ [4,5,-22,58],  [1,36,-16,59], [1,56], [4,3], [5,44], [5,32], [4,2], [3,25], [5,1], [7,36], [9,7], [7,44] ],
                    [ [3,58,-22,52], [1,35,-16,41], [1,59], [4,7], [5,46], [5,30], [3,59], [3,26], [5,6], [7,41], [9,7], [7,38] ],
                    [ [3,52,-22,47], [1,33,-16,24], [2,2], [4,12], [5,47], [5,28], [3,56], [3,28], [5,11], [7,46], [9,7], [7,33] ],    
                    [ [3,45,-22,40], [1,32,-16,6], [2,5], [4,16], [5,49], [5,25], [3,53], [3,29], [5,16], [7,50], [9,7], [7,27] ],
                    
                    [ [3,38,-22,34], [1,30,-15,48], [2,9], [4,20], [5,20], [5,22], [3,51], [3,30], [5,21], [7,55], [9,6], [7,20] ],
                    [ [3,31,-22,26], [1,29,-15,29], [2,12], [4,25], [5,51], [5,20], [3,48], [3,32], [5,26], [7,59], [9,6], [7,14] ],    
                    [ [3,25,-22,19], [1,28],-15,11, [2,16], [4,29], [5,52], [5,17], [3,46], [3,34], [5,31], [8,3], [9,5], [7,8] ],   
                    [ [3,19,-22,11], [1,28,-14,52], [2,19], [4,33], [5,53], [5,14], [3,44], [3,36], [5,36], [8,8], [9,4], [7,1] ],  
                    [ [3,12,-22,2],  [1,27,-14,32], [2,23], [4,37], [5,54], [5,11], [3,41], [3,38], [5,41], [8,12], [9,3], [6,54] ],  
                    
                    [ [3,6,-21,53],  [1,27,-14,13], [2,27], [4,41], [5,54], [5,8], [3,39], [3,40], [5,46], [8,16], [9,1], [6,47] ], 
                    [ [3,0,-21,44],  [1,27,-13,53], [2,31], [4,45], [5,55], [5,5], [3,37], [3,42], [5,52], [8,20], [9,0], [6,41] ],
                    [ [2,55,-21,34], [1,27,-13,33], [2,35], [4,39], [5,55], [5,2], [3,35], [3,45], [5,57], [8,23], [8,58], [6,34] ],
                    [ [2,49,-21,24], [1,28,-13,13], [2,39], [4,53], [5,55], [4,59], [3,33], [3,48], [6,2], [8,27], [8,56], [6,27] ],                    
                    [ [2,43,-21,14], [1,28,-12,53], [2,43], [4,57], [5,55], [4,56], [3,32], [3,50], [6,7], [8,31], [8,53], [6,19] ],                    

                    [ [2,38,-21,3],  [1,29,-12,32], [2,47], [5,0], [5,55], [4,52], [3,30], [3,53], [6,13], [8,34], [8,51], [6,12] ],  
                    [ [2,33,-20,51], [1,30,-12,11], [2,51], [5,4], [5,55], [4,49], [3,29], [3,56], [6,18], [8,37], [8,48], [6,5] ],
                    [ [2,28,-20,39], [1,31,-11,50], [2,56], [5,7], [5,54], [4,46], [3,27], [3,59], [6,23], [8,40], [8,45], [5,58] ],
                    [ [2,23,-20,27], [1,32,-11,29], [3,0], [5,11], [5,54], [4,43], [3,26], [4,3], [6,29], [8,43], [8,42], [5,50] ],
                    [ [2,19,-20,15], [1,33,-11,8], [3,4], [5,14], [5,53], [4,39], [3,25], [4,6], [6,34], [8,46], [8,39], [5,43] ],
                    
                    [ [2,14,-20,2],  [1,35,-10,46], [3,9], [5,17], [5,52], [4,36], [3,24], [4,10], [6,40], [8,49], [8,35], [5,35] ],
                    [ [2,10,-19,48], [1,36,-10,25], [3,13], [5,20], [5,51], [4,33], [3,24], [4,13], [6,45], [8,51], [8,32], [5,28] ],
                    [ [2,6,-19,35],  [1,38,-10,3], [3,18], [5,23], [5,50], [4,29], [3,23], [4,17], [6,50], [8,53], [8,28], [5,21] ],
                    [ [2,2,-19,21],  [1,40,-9,41], [3,22], [5,26], [5,49], [4,26], [3,23], [4,21], [6,55], [8,56], [8,24], [5,13] ],
                    [ [1,58,-19,6],  [1,43,-9,19], [3,27], [5,28], [5,47], [4,23], [3,22], [4,25], [7,1], [8,58], [8,19], [5,6] ],

                    [ [1,55,-18,51], [1,45,-8,56], [3,31], [5,31], [5,46], [4,20], [3,22], [4,29], [7,6], [8,59], [8,15], [4,58] ],
                    [ [1,52,-18,36], [1,47,-8,34], [3,36], [5,34], [5,44], [4,17], [3,22], [4,34], [7,11], [9,1], [8,10], [4,51] ],
                    [ [1,48,-18,21], [1,50,-8,11], [3,40], [5,36], [5,43], [4,14], [3,22], [4,38], [7,16], [9,2], [8,5], [4,44] ],
                    [ [1,46-18,5],   [1,53,-7,49], [3,45], [5,38], [5,41], [4,11], [3,23], [4,42], [7,21], [9,4], [8,0], [4,36] ],
                    [ [1,43-17,49],  ["NULL","NULL"], [3,49], [5,40], [5,39], [4,8], [3,23], [4,47], [7,26], [9,5], [7,55], [4,29] ],

                    [ [1,41,-17,33], ["NULL","NULL"], [3,54], ["NULL","NULL"], [5,37], ["NULL","NULL"], [3,24], [4,52], ["NULL","NULL"], [9,5], ["NULL","NULL"], [4,22] ],
    ]
    
    table_4a = [ [2019,2],
                [2020,-4], #+20 after Feb 29th
                [2021,14],
                [2022,8],
                [2023,3],
                [2024,-3]
    ]
            
            # the differences between consecutive values of E are the horizontal argument
            # the number of hours of OT as the vertical argument.
    table_4b = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ],
            [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2 ],
            [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3 ],
            [0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4 ],
            [0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 5, 5, 5 ],
            [0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6 ],
            [0, 1, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 6, 6, 6, 6, 7, 7 ],
            [0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 7, 7, 7, 8, 8 ],
            [0, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 5, 5, 5, 6, 6, 6, 7, 7, 8, 8, 8, 9, 9 ],
            [0, 1, 1, 2, 2, 3, 3, 3, 4, 4, 5, 5, 5, 6, 6, 7, 7, 8, 8, 8, 9, 9, 10, 10 ],
            [0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10, 11, 11 ],
            [1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10, 11, 11, 12, 12],
            [1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 7, 7, 8, 8, 9, 9, 10, 10, 11, 11, 12, 12, 13],
            [1, 1, 2, 2, 3, 4, 4, 5, 5, 6, 6, 7, 8, 8, 9, 9, 10, 11, 11, 12, 12, 13, 13, 14],
            [1, 1, 2, 3, 3, 4, 4, 5, 6, 6, 7, 8, 8, 9, 9, 10, 11, 11, 12, 13, 13, 14, 14, 15],
            [1, 1, 2, 3, 3, 4, 5, 5, 6, 7, 7, 8, 9, 9, 10, 11, 11, 12, 13, 13, 14, 15, 15, 16],
            [1, 1, 2, 3, 4, 4, 5, 6, 6, 7, 8, 9, 9, 10, 11, 11, 12, 13, 13, 14, 15, 16, 16, 17],
            [1, 2, 2, 3, 4, 5, 5, 6, 7, 8, 8, 9, 10, 11, 11, 12, 13, 14, 14, 15, 16, 17, 17, 18],
            [1, 2, 2, 3, 4, 5, 6, 6, 7, 8, 9, 10, 10, 11, 12, 13, 13, 14, 15, 16, 17, 17, 18, 19],
            [1, 2, 3, 3, 4, 5, 6, 7, 8, 8, 9, 10, 11, 12, 13, 13, 14, 15, 16, 17, 18, 18, 19, 20],
            [1, 2, 3, 4, 4, 5, 6, 7, 8, 9, 10, 11, 11, 12, 13, 14, 15, 16, 17, 18, 18, 19, 20, 21],
            [1, 2, 3, 4, 5, 6, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 17, 18, 19, 20, 21, 22],
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
    ]

    # Rows = GMT Hour
    # Columns = 00m     10m     20m         30m         40m         50m
    table_4c =  [
        [[175, 00], [177, 30], [180, 00], [182, 30], [185, 00], [187, 30]],
        [[190, 00], [192, 30], [195, 00], [197, 30], [200, 00], [202, 30]],
        [[205, 00], [207, 30], [210, 00], [212, 30], [215, 00], [217, 30]],
        [[220, 00], [222, 30], [225, 00], [227, 30], [230, 00], [232, 30]],
        [[235, 00], [237, 30], [240, 00], [242, 30], [245, 00], [247, 30]],
        [[250, 00], [252, 30], [255, 00], [257, 30], [260, 00], [262, 30]],
        [[265, 00], [267, 30], [270, 00], [272, 30], [275, 00], [277, 30]],
        [[280, 00], [282, 30], [285, 00], [287, 30], [290, 00], [292, 30]],
        [[295, 00], [297, 30], [300, 00], [302, 30], [305, 00], [307, 30]],
        [[310, 00], [312, 30], [315, 00], [317, 30], [320, 00], [322, 30]],
        [[325, 00], [327, 30], [330, 00], [332, 30], [335, 00], [337, 30]],
        [[340, 00], [342, 30], [345, 00], [347, 30], [350, 00], [352, 30]],
        [[355, 00], [357, 30], [0, 00], [2, 30], [5, 00], [7, 30]],
        [[10, 00], [12, 30], [15, 00], [17, 30], [20, 00], [22, 30]],
        [[25, 00], [27, 30], [30, 00], [32, 30], [35, 00], [37, 30]],
        [[40, 00], [42, 30], [45, 00], [47, 30], [50, 00], [52, 30]],
        [[55, 00], [57, 30], [60, 00], [62, 30], [65, 00], [67, 30]],
        [[70, 00], [72, 30], [75, 00], [77, 30], [80, 00], [82, 30]],
        [[85, 00], [87, 30], [90, 00], [92, 30], [95, 00], [97, 30]],
        [[100, 00], [102, 30], [105, 00], [107, 30], [110, 00], [112, 30]],
        [[115, 00], [117, 30], [120, 00], [122, 30], [125, 00], [127, 30]],
        [[130, 00], [132, 30], [135, 00], [137, 30], [140, 00], [142, 30]],
        [[145, 00], [147, 30], [150, 00], [152, 30], [155, 00], [157, 30]],
        [[160, 00], [162, 30], [165, 00], [167, 30], [170, 00], [172, 30]]
        ]

    # row = 10's of minues.
    # colums =        01       05      09      13      17      21      25      29      33      37      41      45      49      53      57  
    table_4d = [
                [[0,0],  [0,1],  [0,2],  [0,3],  [0,4],  [0,5],  [0,6],  [0,7],  [0,8],  [0,9],  [0,10], [0,11], [0,12], [0,13], [0,14]   ],
                [[0,15], [0,16], [0,17], [0,18], [0,19], [0,20], [0,21], [0,22], [0,23], [0,24], [0,25], [0,26], [0,27], [0,28], [0,29]   ],
                [[0,30], [0,31], [0,32], [0,33], [0,34], [0,35], [0,36], [0,37], [0,38], [0,39], [0,40], [0,41], [0,42], [0,43], [0,44]   ],
                [[0,45], [0,46], [0,47], [0,48], [0,49], [0,50], [0,51], [0,52], [0,53], [0,54], [0,55], [0,56], [0,57], [0,58], [0,59]   ],
                [[1,0],  [1,1],  [1,2],  [1,3],  [1,4],  [1,5],  [1,6],  [1,7],  [1,8],  [1,9],  [1,10], [1,11], [1,12], [1,13], [1,14]   ],
                [[1,15], [1,16], [1,17], [1,18], [1,19], [1,20], [1,21], [1,22], [1,23], [1,24], [1,25], [1,26], [1,27], [1,28], [1,29]   ],                
                [[1,30], [1,31], [1,32], [1,33], [1,34], [1,35], [1,36], [1,37], [1,38], [1,39], [1,40], [1,41], [1,42], [1,43], [1,44]   ], 
                [[1,45], [1,46], [1,47], [1,48], [1,49], [1,50], [1,51], [1,52], [1,53], [1,54], [1,55], [1,56], [1,57], [1,58], [1,59]   ], 
                [[2,00], [2,1],  [2,2],  [2,3],  [2,4],  [2,5],  [2,6],  [2,7],  [2,8],  [2,9],  [2,10], [2,11], [2,12], [2,13], [2,14]   ],     
                [[2,15], [2,16], [2,17], [2,18], [2,19], [2,20], [2,21], [2,22], [2,23], [2,24], [2,25], [2,26], [2,27], [2,28], [2,29]   ],  
                [[2,30]]     
    
    ]


    year = timestamp.year - 1
    month = timestamp.month - 1
    day = timestamp.day - 1
    hour = timestamp.hour - 1
    minute = timestamp.minute - 1
    second = timestamp.second - 1

    a = table_4a[0][1]
    print("From table a = ", a)

    if timestamp.minute > 30:
        ot_hour = hour + 2 + a
    else: ot_hour = hour + a
    
    if ot_hour >= 24:
        ot_hour = 0
        day = day +1
    else: pass
    
    print(timestamp)
    print("OT Hour from main table = ", ot_hour)

    if (timestamp.month == 4) or (timestamp.month == 6) or (timestamp.month == 9) or (timestamp.month == 11):
        days_in_month = 30
    elif (timestamp.month == 1) or (timestamp.month == 3) or (timestamp.month == 5) or (timestamp.month == 7) or (timestamp.month == 8) or (timestamp.month == 10) or (timestamp.month == 12):
        days_in_month = 31
    elif timestamp.month == 2:
        days_in_month = 29

    


    E = (table_4_ot[day][month][0] + (table_4_ot[day][month][1]/60) )
    if (table_4_ot[day][month][2] <0):
        E_decl = (table_4_ot[day][month][2] - (table_4_ot[day][month][3]/60) )
    else:
        E_decl = (table_4_ot[day][month][2] + (table_4_ot[day][month][3]/60) )
    
    print("E = ", E)
    print("E Declination - ", E_decl)

    if (day + 1) >= days_in_month:
        day = -1
        month = month + 1
    else: pass

    print("Days in month = ", days_in_month)
    print(".month = ", month)
    print("day = ", day)

    next_E = table_4_ot[day+1][month][0] + (table_4_ot[day+1][month][1]/60)

    if (table_4_ot[day+1][month][2] < 0):
        next_E_decl = table_4_ot[day+1][month][2] - (table_4_ot[day+1][month][3]/60)
    else:
        next_E_decl = table_4_ot[day+1][month][2] + (table_4_ot[day+1][month][3]/60)

    print("Next E = ", next_E)
    print("Next E declination = ", next_E_decl)

    E_diff = round(60*(E - next_E))
    E_diff_decl = abs(round(60*(E_decl - next_E_decl)))
    print("Difference in consecutive E's = ", E_diff)
    print("Difference in Decl's = ", E_diff_decl)


    b = table_4b[ot_hour][E_diff]
    b_decl = table_4b[ot_hour][E_diff_decl-1]
    print("From table b = ", b)
    print("b_decl = ", b_decl)

    #print(timestamp.minute % 10)
    discard = timestamp.minute % 10
    if discard < 5:
        rounded_minute =  timestamp.minute - discard
    else: rounded_minute = 10 - discard + timestamp.minute

    if rounded_minute >= 60:
        rounded_minute = 0
    #rounded_minute = round(timestamp.minute)
    #print(timestamp.hour, (rounded_minute/10))
    print("Rounded minute = ", rounded_minute)


    c = table_4c[timestamp.hour][int(rounded_minute/10)][0] + (table_4c[timestamp.hour][int(rounded_minute/10)][1]/60)
    print("From table c = ", c)

    if (timestamp.second >= 57) or (timestamp.second < 1) :
        index = 0
    elif (timestamp.second >= 1) and (timestamp.second < 5) :
        index = 1
    elif (timestamp.second >= 5) and (timestamp.second < 9) :
        index = 2
    elif (timestamp.second >= 9) and (timestamp.second < 13) :
        index = 3
    elif (timestamp.second >= 13) and (timestamp.second < 17) :
        index = 4
    elif (timestamp.second >= 17) and (timestamp.second < 21) :
        index = 5
    elif (timestamp.second >= 21) and (timestamp.second < 25) :
        index = 6
    elif (timestamp.second >= 25) and (timestamp.second < 29) :
        index = 7
    elif (timestamp.second >= 29) and (timestamp.second < 33) :
        index = 8
    elif (timestamp.second >= 33) and (timestamp.second < 37) :
        index = 9
    elif (timestamp.second >= 37) and (timestamp.second < 41) :
        index = 10
    elif (timestamp.second >= 41) and (timestamp.second < 45) :
        index = 11
    elif (timestamp.second >= 45) and (timestamp.second < 49) :
        index = 12
    elif (timestamp.second >= 49) and (timestamp.second < 53) :
        index = 13
    elif (timestamp.second >= 53) and (timestamp.second < 57) :
        index = 14

    print("index = ", index)
    print("minute = ", timestamp.minute)
    print(table_4d[(timestamp.minute % 10)][index])
    d = table_4d[(timestamp.minute % 10)][index][0] + (table_4d[(timestamp.minute % 10)][index][1]/60)
    print("minute = ", timestamp.minute)
    print("second = ", timestamp.second)
    print(d)

    gha = E - (b/60) + c + d
    if (E_decl < 0):
        declination = E_decl + (b_decl/60)
    else:
        declination = E_decl - (b_decl/60)
    print("GHA = ", gha)
    print("Table Declination = ", declination)

    #print (month)
    #print(timestamp)
    #print(table_4_ot[1][0][1])
    #[ 4+(12/60), 1+(38/60), 1+(53/60), 3+(58/60), 5+(42/60, 5+(35/60), 4+(5/60, 3+(24/60), 4+(56/60), 7+(31/60), 9+(6/60), 7+(50/60) ]


    return gha, declination

os.system('cls' if os.name == 'nt' else 'clear')
print("MAIN MENU")
select = input("1) Use Eratosthenes Method \n2) Use Sextant \nEnter Selection: ")

if select == "1":
    input("Press Enter to mark the time of your observation: ")
    timestamp = datetime.utcnow()
    height = input("Enter the height of your object: ")
    shadow = input("Enter the length of the shadow: ")
    alt = input("Enger your altitude in nm: ")
    day_of_year = timestamp.timetuple().tm_yday
    gha, dec = sun_posit(timestamp)            #input("Enter the sun's GHA from tables in decimal form: ")
    sun_decl(day_of_year)
    bearing = input("Enter the magnetic bearing to the sun: ")
    eratosthenes(timestamp, float(height), float(shadow), float(alt), float(gha), float(bearing), float(dec))
else: 
    input("Press Enter to mark the time of your observation: ")
    timestamp = datetime.utcnow()
    body = input("Enter the name of the celestial body for your sight: ")
    alt = input("Enger your altitude in nm: ")
    gha, dec = sun_posit(timestamp) 
    bearing = input("Enter the magnetic bearing to the sun: ")
    H_angle = input("Enter the angle from your sextant sight: ")
    sextant(timestamp, float(H_angle), float(alt), float(gha), float(bearing), float(dec))
