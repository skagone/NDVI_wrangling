import os
import shutil
import calendar
from datetime import datetime, timedelta, date

area_txtfile = r'test_area'
outPath = r'C:\WaterSmart\Projects\NDVI_wrangling'
product = '250_m_16_days_NDVI.tif'
sizecel = 0.00965199992061
HDFnum = '0'

t1 = datetime.datetime.now()

if os.path.exists(os.path.join(outPath, 'scrap')):
    shutil.rmtree(os.path.join(outPath, 'scrap'))
    print('deleted ' + outPath + os.sep + 'scrap')
    os.makedirs((os.path.join(outPath, 'scrap')))
else:
    print("Directory does not exist!")
    os.makedirs(os.path.join(outPath, 'scrap'))
outPathscrap = (os.path.join(outPath, 'scrap'))

start_year = '2014'
end_year = '2014'
start_day = '274'
end_day = '299'

start_date = datetime.strptime(f"{start_year}{start_day}",'%Y%j')
end_date = datetime.strptime(f"{end_year}{end_day}",'%Y%j')
print("The NDVI will be downloaded between " + start_date + " and " + end_date)

time_interval = end_date - start_date
num_days = time_interval.days


tilepath = os.path.join(outPath, 'ndvitiles')
if not os.path.exists(tilepath):
    os.makedirs(tilepath)

# create list with all tiles needed for download to cover desired study area
fileIN = open(area_txtfile, 'r')
tiles = fileIN.read()
tilesList = []
tilesList = tiles.split(";")
print(tilesList)

# MODIS product
# MOD13Q1.006.A2020049.h11v05.006.2020058051610.hdf
# Terra - MOD13Q1.006  starts at day 1 with 16 days gap
# Aqua - MYD13Q1.006   starts at day 9 with 16 days gap


# loop for determining the right data directory to download from the website - Aqua or Terra directories
for i in range(num_days + 1):

    root = 'https://e4ftl01.cr.usgs.gov/'
    vers = '006'
    #Terra
    directory = 'MOLT'
    product = 'MOD13Q1'
    # Aqua
    directory = 'MOLA'
    product = 'MYD13Q1'

    for tilename in tilesList:
        print(tilename)
        # CONCEPTUAL

productName = '{}.A{}{}.{}.{}.{}'.format(product, year, jdate, tilename, vers, wildcard)
url = '{}/{}/{}/{}'.format(root, directory, productName)


# wget_tool_exe = r'D:\FEWS\DataPortal\utilities\wget-1.19.1\wget.exe'
wget_tool_exe = r'C:\WaterSmart\Users\Olena\Projects\utilities\wget-1.19.4-win64\wget.exe'

os.chdir(outPathscrap)
print(os.getcwd())


raw_extension = '.hdf'
wget_command = "%s -r -l1 --no-host-directories --no-parent --no-check-certificate " \
               "--http-user=%s --http-password=%s -A%s %s" \ %(wget_tool_exe, username, password, raw_extension, urlpath)
print(wget_command)
os.system(wget_command)

# Select only the tiles needed for the USA and copy to temp/date folder
download_dir = outPathscrap+os.sep+directo r y+os.s e p+product d ir+os. s ep+dateLpd a ac
if os .path.exists(download_dir):
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
                    shutil.copy2(download_dir+os.sep+hdff,out H df+os. s ep+hd ff)
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
    #arcpy.ExtractSubDataset_management(InputHDF, OutputTIF, HDFnum)
    list.append(OutputTIF)
    i = i + 1