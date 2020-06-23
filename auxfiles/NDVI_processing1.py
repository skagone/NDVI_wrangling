# Import system modules
import arcpy
from arcpy.sa import *
from arcpy import env
import sys, os, traceback, datetime, time, tarfile, calendar
from datetime import date
from time import localtime, strftime
import string, glob, math, stat
import shutil
arcpy.CheckOutExtension("Spatial")
arcpy.gp.overwriteOutput = True
arcpy.rasterstatistics = "STATISTICS"

# manually copy the full extent rasters (073 - 273) to folder 'Global_NDVI\V006_step2\2018'


try:

    year = '2019'  #sys.argv[1]
    inPath = r'C:\WaterSmart\Data\NDVI\Global\V006' +os.sep+ year+'_orig'
    product = '.1_km_16_days_NDVI.tif'
    beg_list = ['009','025','041','057','281','297','313','329','345','361']
    beg_val = r'C:\WaterSmart\Data\NDVI\Global\NDVI_val-500.tif'


    outPath = r'C:\WaterSmart\Data\NDVI\Global\V006_step2' +os.sep+ year
    if not os.path.exists(outPath):
        os.makedirs(outPath)

    #Mosaic e.g. period 001 file to period 073 so the missing extent received the values of period 073  
    for beg in beg_list:
        beg_file1 = year+beg+product
        beg_file2 = beg_val
        inputs = beg_file2 +';'+ inPath+os.sep+beg_file1
        print inputs
        arcpy.MosaicToNewRaster_management(inputs, outPath, year+beg+product, coordinate_system_for_the_raster="",
                                           pixel_type="16_BIT_SIGNED", cellsize="", number_of_bands="1", mosaic_method="LAST", mosaic_colormap_mode="FIRST")

    del beg_list
    
    #Create 8-day time steps by dividing the 2 neighboring periods (001+016/2 = 009)

    inPath = r'C:\WaterSmart\Data\NDVI\Global\V006_step2' +os.sep+ year
    outPath = r'C:\WaterSmart\Data\NDVI\Global\V006_step2' +os.sep+ year+'all'
    if not os.path.exists(outPath):
        os.makedirs(outPath)

    day8_list = ['001','017','033','049','065','081','097','113','129','145','161','177','193','209','225','241','257','273','289','305','321','337','353']
    day16_list = ['009','025','041','057','073','089','105','121','137','153','169','185','201','217','233','249','265','281','297','313','329','345','361']

    m = 0
    n = 0

    for d,dd in zip(day8_list,day16_list):
        print d
        print dd
                        
        if d == '001': #first period
            file1 = inPath +os.sep+ year+dd+product
            print file1
            out1 = outPath +os.sep+ year+d+product
            print 'out1: ' + out1
            out2 = outPath +os.sep+ year+dd+product
            print 'out2: ' +out2
            shutil.copy(file1,out1) #copy 009 as 001 to folder
            shutil.copy(file1,out2) #copy 009 to new folder   
            m += 1
            n += 1
        else:
            file1 = inPath +os.sep+ year+day16_list[m-1]+product
            print file1
            file2 = inPath +os.sep+ year+(dd)+product
            print file2
            out11 = Int(Float(file1) + Float(file2) / 2.0)
            out1 =  Con(out11 > 10000, 10000, out11)
            out2 = outPath +os.sep+ year+d+product
            print 'out_mean: ' +out2
            out1.save(out2) #copy calculation as 017 to new folder
            out3 = inPath +os.sep+ year+dd+product
            print out3
            out4 = outPath +os.sep+ year+dd+product
            print 'out4: ' +out4
            shutil.copy(out3,out4) #copy 025 as 025 to new folder

            m += 1
            n += 1
            

    #Reassign 8-day periods to dekadal time steps by ignoring periods 017, 057, 097, 137, 177, 209, 241, 281, 321, 361
    # set NoData values to 0 --> needed for ET calculation using NDVI as a condition for water

    outPath1 = r'C:\WaterSmart\Data\NDVI\Global\V006' +os.sep+ year
    if not os.path.exists(outPath1):
        os.makedirs(outPath1)

    day8_list = ['001','009','025','033','041','049','065','073','081','089','105','113','121','129','145','153','161','169',
                 '185','193','201','217','225','233','249','257','265','273','289','297','305','313','329','337','345','353']
    dek_list = ['011','012','013','021','022','023','031','032','033','041','042','043','051','052','053','061','062','063',
                '071','072','073','081','082','083','091','092','093','101','102','103','111','112','113','121','122','123']

    cell_s = 0.0096519999
    snapR = r'C:\WaterSmart\Data\Temperature\Global\LST\V006\2017\lst17011.tif'

    for s, ss in zip(day8_list,dek_list):
        print s
        print ss
        file11 = outPath +os.sep+ year+s+product
        print file11
        file12 = Con(IsNull(file11), 0, file11)
        file22 = outPath1 +os.sep+ year+ss+product
        print file22
        #arcpy.CopyRaster_management(file12,file22, "#", "#", "#", "#", "#", "16_BIT_SIGNED")
        #Add: Resampling to match pixels with MODIS LST data
        env.snapRaster = snapR
        arcpy.Resample_management(in_raster=file12, out_raster=file22, cell_size = cell_s, resampling_type="NEAREST")

except:
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]
    pymsg = "PYTHON ERRORS:\nTraceback Info:\n" + tbinfo + "\nError Info:\n    " + str(sys.exc_type)+ ": " + str(sys.exc_value) + "\n"
    arcpy.AddError(pymsg)
    print pymsg