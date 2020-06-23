
# Import system modules
import calendar
import datetime
import glob
import math
import os
import re
import shutil
import stat
import string
import sys
import tarfile
import time
import traceback
import urllib
# import urllib2
# from urllib2 import urlopen
from datetime import date
from time import localtime, strftime

import arcpy
from arcpy import env
from arcpy.sa import *


arcpy.CheckOutExtension("Spatial")
arcpy.gp.overwriteOutput = True
arcpy.rasterstatistics = "STATISTICS"

try:

#download NDVI

    area_txtfile = r'C:\WaterSmart\Data\NDVI\Global\USA.txt'  #Global11.txt'
    year = '2019' #sys.argv[1]
    outPath = r'C:\WaterSmart\Data\NDVI\Global\V006'
    product = '1_km_16_days_NDVI.tif'
    sizecel = 0.00965199992061
    HDFnum = '0' 
    #change product below

    if os.path.exists(outPath +os.sep+ 'scrap11'):
        shutil.rmtree(outPath +os.sep+ 'scrap11')
        #"RMDIR "+ outPath +os.sep+ 'scrap' +" /s /q"
        print('deleted ' + outPath +os.sep+ 'scrap11')
        os.makedirs(outPath +os.sep+ 'scrap11')
    else:
        print("Directory does not exist!")
        os.makedirs(outPath +os.sep+ 'scrap11')

    #check for last LST created and run script when new LST period is available for download
    t1 = datetime.datetime.now()

    lsttifpath = outPath +os.sep+ str(year)
    if not os.path.exists(lsttifpath):
        os.makedirs(lsttifpath)
    env.workspace = lsttifpath
    lsttifs = arcpy.ListRasters()
    lsttifs.sort()

    outPathscrap = outPath +os.sep+ 'scrap11'


    if lsttifs == []:
        lstnext = 9
        print("Last 8day period started on: 361")
    else:
        lsttifs.sort()
        lstjdate1 = lsttifs[-1][4:7]
        lstnext = int(lstjdate1) + 16
        print("Last 8day period started on: " + lstjdate1)

        if lstnext == 369:
            print("Last 8day period of the year started on: " + lstjdate1)
      
    jdateb = "00" + str(lstnext)
    jdate = jdateb[-3:]

    intjdate = int(jdate)
    if type(year) == 'int':
        date = str(datetime.date(year, 1, 1) + datetime.timedelta(intjdate - 1)) #output 2010-04-23
    else:
        intyear = int(year)
        date = str(datetime.date(intyear, 1, 1) + datetime.timedelta(intjdate - 1)) #output 2010-04-23

    print("Next 16day period should start on " + jdate + " = " + date)

    t1 = datetime.datetime.now()
    
    fileIN = open(area_txtfile, 'r')
    tiles = fileIN.read()
    tilesList = []
    tilesList = tiles.split(";")
    print(tilesList)
    directory = "MOLA"
    productdir = "MYD13A2.006"
    lstname1 = productdir[:-3]
    lstname2 = productdir[:-4]
    dateList = date.split("-")
    Year = dateList[0]
    Month = dateList[1]
    Day = dateList[2]
    print(dateList)
    dateLpdaac = str(Year) + "." + str(Month) + "." + str(Day)

    #url = 'http://e4ftl01.cr.usgs.gov/'+ directory + '/' + productdir +'/' + dateLpdaac
    outHdf = outPathscrap +os.sep+ dateLpdaac
    if not os.path.exists(outHdf):
        os.makedirs(outHdf)
    outHdfa = outHdf.replace('\\', '/')

    root = 'https://e4ftl01.cr.usgs.gov/'
    teil1 = directory
    teil2 = productdir
    url = os.path.join(root,teil1,teil2).replace('\\', '/')
    print("parentURL: " + str(url))
    data = dateLpdaac
    urlpath = os.path.join(url,data).replace('\\', '/') +'/'

    username = 'sbohms'
    password = 'Data4ET1'

    # wget_tool_exe = r'D:\FEWS\DataPortal\utilities\wget-1.19.1\wget.exe'
    wget_tool_exe = r'C:\WaterSmart\Users\Olena\Projects\utilities\wget-1.19.4-win64\wget.exe'

    os.chdir(outPathscrap)
    print(os.getcwd())

    #Files = 1 #'couple'
    Files = 2 #'a lot'
    
    if Files == 1:

        # for tile in tilesList:
        #     print tile
        #     raw_extension = '*'+str(tile)+'*.hdf'
        #     wget_command = "%s -r -l1 --no-host-directories --no-parent --no-check-certificate --http-user=%s --http-password=%s -A%s %s" %(wget_tool_exe, username, password, raw_extension, urlpath)
        #     print wget_command
        #     os.system(wget_command)
        #
        # #Select only the tiles needed for the USA and copy to temp/date folder
        # download_dir = outPathscrap+os.sep+directory+os.sep+productdir+os.sep+dateLpdaac
        # if os.path.exists(download_dir):
        #     nof = len(os.walk(download_dir).next()[2])
        #     if nof == 0:
        #         print 'Input files are not available!'
        #         print 'INFO: Exit Script'
        #         sys.exit(0)
        #     else:
        #         print 'Input files are downloaded!'
        #         hdffiles = os.listdir(download_dir)
        #         for hdff in hdffiles:
        #             shutil.copy2(download_dir+os.sep+hdff,outHdf+os.sep+hdff)
        #             print 'Copied data!!!!!!!'
        #
        # t2 = datetime.datetime.now()
        # t3 = (t2 - t1)
        # print "Processing time:" + str(t3)
        # fileIN.close()
        #
        # print "-----Conservation from hdf to tif "
        #
        # Output_LocationGrid = outPathscrap +os.sep+ str(jdate) + 'NDVIgrids'
        # if not os.path.exists(Output_LocationGrid):
        #     os.makedirs(Output_LocationGrid)
        #
        # env.workspace = outHdf
        # InputHDFs = arcpy.ListRasters()
        # list = []
        # i = 10
        # HDFnum = '0'
        # for InputHDF in InputHDFs:
        #     OutputTIF = Output_LocationGrid +os.sep+ str(jdate) + str(i)  # gridfile   outHdf + "\\" +
        #     print OutputTIF
        #     # Process: Extract Subdataset...
        #     arcpy.ExtractSubDataset_management(InputHDF,OutputTIF, HDFnum)
        #     list.append(OutputTIF)
        #     i = i + 1
        #
        # NDVI = str(year) + str(jdate) + "." + str(product)
        # print NDVI
        # Coordsystem = r'C:\Users\Olena\Projects\ArcGIS\WGS 1984.prj'
        # arcpy.CreateFileGDB_management(outPathscrap,"lst11.gdb","CURRENT")
        # arcpy.CreateMosaicDataset_management(outPathscrap+os.sep+"lst11.gdb", "lst11", Coordsystem, "1", "16_BIT_SIGNED", "NONE", "")
        # mosimg = arcpy.AddRastersToMosaicDataset_management(outPathscrap+os.sep+"lst1.gdb"+os.sep+"lst11", "Raster Dataset", Output_LocationGrid, "UPDATE_CELL_SIZES", "UPDATE_BOUNDARY", "NO_OVERVIEWS", "#", "0", "1500","#","#","SUBFOLDERS","OVERWRITE_DUPLICATES","BUILD_PYRAMIDS","CALCULATE_STATISTICS","NO_THUMBNAILS","#","NO_FORCE_SPATIAL_REFERENCE")
        # arcpy.CopyRaster_management(mosimg, lsttifpath +os.sep+ NDVI)
        print("done")


    elif Files == 2:

        raw_extension = '.hdf'
        wget_command = "%s -r -l1 --no-host-directories --no-parent --no-check-certificate " \
                       "--http-user=%s --http-password=%s -A%s %s" \
                       %(wget_tool_exe, username, password, raw_extension, urlpath)
        print(wget_command)
        os.system(wget_command)

        #Select only the tiles needed for the USA and copy to temp/date folder
        download_dir = outPathscrap+os.sep+directory+os.sep+productdir+os.sep+dateLpdaac
        if os.path.exists(download_dir):
            nof = len(os.walk(download_dir).next()[2])
            if nof == 0:
                print('Input files are not available!')
                print('INFO: Exit Script')
                sys.exit(0)
            else:
                print('Input files are downloaded!')
                hdffiles = os.listdir(download_dir)
                for tile in tilesList:
                    print(tile)
                    for hdff in hdffiles:                        
                        if str(hdff.split('.')[2]) == str(tile):
                            print(hdff)
                            shutil.copy2(download_dir+os.sep+hdff,outHdf+os.sep+hdff)
                            # print('Copied data!!!!!!!')
      
        t2 = datetime.datetime.now()
        t3 = (t2 - t1)
        print("Processing time:" + str(t3))
        fileIN.close()
        
        print("-----Conservation from hdf to tif ")
        
        Output_LocationGrid = outPathscrap + os.sep + str(jdate) + 'NDVIgrids'
        if not os.path.exists(Output_LocationGrid):
            os.makedirs(Output_LocationGrid)

        env.workspace = outHdf
        InputHDFs = arcpy.ListRasters()
        list = []        
        i = 10
        HDFnum = '0'
        for InputHDF in InputHDFs:
            OutputTIF = Output_LocationGrid +os.sep+ str(jdate) + str(i)  # gridfile   outHdf + "\\" + 
            print(OutputTIF)
            # Process: Extract Subdataset...
            arcpy.ExtractSubDataset_management(InputHDF, OutputTIF, HDFnum)
            list.append(OutputTIF)
            i = i + 1

        NDVI = str(year) + str(jdate) + "." + str(product)
        print(NDVI)
        Coordsystem = r'C:\WaterSmart\Users\Olena\Projects\ArcGIS\WGS 1984.prj'
        arcpy.CreateFileGDB_management(outPathscrap,"lst.gdb","CURRENT")
        arcpy.CreateMosaicDataset_management(outPathscrap+os.sep+"lst.gdb", "lst2", Coordsystem, "1", "16_BIT_SIGNED", "NONE", "")
        mosimg = arcpy.AddRastersToMosaicDataset_management(outPathscrap+os.sep+"lst.gdb"+os.sep+"lst2", "Raster Dataset", Output_LocationGrid, "UPDATE_CELL_SIZES", "UPDATE_BOUNDARY", "NO_OVERVIEWS", "#", "0", "1500","#","#","SUBFOLDERS","OVERWRITE_DUPLICATES","BUILD_PYRAMIDS","CALCULATE_STATISTICS","NO_THUMBNAILS","#","NO_FORCE_SPATIAL_REFERENCE")
        arcpy.CopyRaster_management(mosimg, lsttifpath + os.sep + NDVI)
        print("done")

    else:
        print('not the right input for Files var!')


except:
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]
    pymsg = "PYTHON ERRORS:\nTraceback Info:\n" + tbinfo + "\nError Info:\n    " + str(sys.exc_type)+ ": " + str(sys.exc_value) + "\n"
    arcpy.AddError(pymsg)
    print(pymsg)
