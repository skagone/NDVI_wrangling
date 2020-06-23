# Import system modules
import arcpy
from arcpy.sa import *
from arcpy import env
from ftplib import FTP
import sys, os, traceback, datetime, time
from datetime import date
from time import localtime, strftime
import string, glob
from shutil import copyfile
arcpy.CheckOutExtension("Spatial")

#year = str(sys.argv[1])
#arcpy.env.workspace = r'D:\Stornext\fewspsnfs2\WaterSmart\Data\NDVI\ASP_NDVI\V006_Terra' +os.sep+ str(year)
#arcpy.env.workspace = r'W:\Data\NDVI\USA\V006_250m' +os.sep+ str(year)
#arcpy.env.workspace = r'W:\Data\NDVI\USA\V006_1km_update' +os.sep+ str(year)
arcpy.env.workspace = r'W:\Projects\Veg_ET\USA_data\NDVI_daily_1_km\MEDIAN\Med_0119_filled'
rasterList = arcpy.ListRasters('*', 'TIF')

#rasterList.sort()

jd = str(sys.argv[1])
#file_in1 = arcpy.env.workspace +os.sep+ year+jd +'.250_m_16_days_NDVI.tif'
#file_in1 = arcpy.env.workspace +os.sep+ year+jd +'.1_km_16_days_NDVI.tif'
file_in1 = arcpy.env.workspace + os.sep + 'med' + jd + '.1_km_16_days_NDVI.tif'
je = str(sys.argv[2])
#file_in2 = arcpy.env.workspace +os.sep+ year+je +'.250_m_16_days_NDVI.tif'
#file_in2 = arcpy.env.workspace +os.sep+ year+je +'.1_km_16_days_NDVI.tif'
file_in2 = arcpy.env.workspace + os.sep + 'med' + je + '.1_km_16_days_NDVI.tif'
jf = jd

f = int(sys.argv[3]) #16
a = range(0,f)

#out_dir = r'W:\Projects\Veg_ET\USA_data\NDVI_daily\NDVI_interpolated\{}'.format(year)
out_dir = r'W:\Projects\Veg_ET\USA_data\NDVI_daily_1_km\MEDIAN\Med_0119_filled_interpolated'
if not os.path.exists(out_dir):
    os.makedirs(out_dir)


for b in a:
    print b
    d = (Float(file_in2) - Float(file_in1)) / f
    e = Float(file_in1) + (b*d)
    e_new = Float(e)/10000
    c = int(jf) + b
    cc = ('00' + str(c))[-3:]
    print cc
    #file_out = out_dir +os.sep+ year+ cc +'.250_m_NDVI.tif'
    #file_out = out_dir + os.sep + year + cc + '.1_km_16_days_NDVI.tif'
    file_out = out_dir + os.sep + 'med' + cc + '.1_km_16_days_NDVI.tif'
    e_new.save(file_out)
    print('-----')


