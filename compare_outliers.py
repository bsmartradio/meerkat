import numpy as np
import glob
import matplotlib.pyplot as plt
import math
import argparse
from numpy.linalg import norm
from astropy.io import fits
from matplotlib.colors import LogNorm
from matplotlib.backends.backend_pdf import PdfPages
from meerMod import *
from astropy.wcs import WCS
from astropy.io.votable.tree import VOTableFile, Resource, Table, Field
from astropy.table import QTable, Table, Column


#The purpose of this program is to take neighboring cubes from MeerKAT and the Aegean 
#source catalogues and identify overlapping sources, then check how well the sources
#match each other positionally and how close their photometry output is

#A catalogue of matching points is made, then a table of how well each channel matches is created

#Possibly need to split this program into two seperate ones?????

def find_neighbor(location,folder):
    glob.glob(location+"phot_table*.npy")
    return neighbors

def fit_deviation(valuesOne,valuesTwo):
    p1=np.array([0.0,0.0])
    p2=np.array([10.0,10.0])
    p3=np.empty([len(valuesOne),2])
    p3[:,0]=valuesOne
    p3[:,1]=valuesTwo
    matchedArr=np.cross(p2-p1,p3-p1)/norm(p2-p1)
    return matchedArr

def plot_channels(cubes,cubeNames,overlap_index_center,overlap_index_neighbor,positions,valuesArr):
    
    plt.rcParams["axes.grid"] = False
    plt.rcParams['xtick.labelsize']=8
    plt.rcParams['ytick.labelsize']=8
    for channel in range(14):
        f, axarr = plt.subplots(1,3,sharey=True,gridspec_kw = {'wspace':0, 'hspace':0})
        for im in range(3,0,-1):
            image_data=get_image(cubes[im-1]+'/'+cubeNames[im-1]+"_Mosaic_chan"+"{:02d}".format(channel+1)+".fits")
            print(image_data[0][0].any())
            if valuesArr[channel]:
                axarr[3-im].imshow(image_data[0], cmap='gray',vmin=-.004, vmax=.004)
                if im ==1:                
                    #print('')
                    axarr[3-im].scatter(positions[0][overlap_index_neighbor[0][0][valuesArr[channel][3]],0], positions[0][overlap_index_neighbor[0][0][valuesArr[channel][3]],1],s=1)
                if im ==2:   
                    axarr[3-im].scatter(positions[1][overlap_index_center[1][0][valuesArr[channel][7]],0],positions[1][overlap_index_center[1][0][valuesArr[channel][7]],1],s=1)
                    axarr[3-im].scatter(positions[1][overlap_index_center[0][0][valuesArr[channel][3]],0],positions[1][overlap_index_center[0][0][valuesArr[channel][3]],1],s=1)
                if im ==3:                
                    axarr[3-im].scatter(positions[2][overlap_index_neighbor[1][0][valuesArr[channel][7]],0],positions[2][overlap_index_neighbor[1][0][valuesArr[channel][7]],1],s=1)
        f.subplots_adjust(hspace=0)
        for ay in axarr:
            ay.label_outer()
        plt.savefig('/Volumes/200GB/MeerKAT/'+cubeNames[1]+'/'+cubeNames[1]+"chan"+"{:02d}".format(channel+1)+"_outliers.png",dpi=600)
        plt.show()
        plt.close(f)
        
def load_neighbors(names,folder):
    vot_mid=read_info(folder+'/'+names[1]+'_Mosaic_Mom0_comp.vot')
    vot_left=read_info(folder+'/'+names[0]+'_Mosaic_Mom0_comp.vot')
    vot_right=read_info(folder+'/'+names[2]+'_Mosaic_Mom0_comp.vot')
    
    vot_list=[vot_left,vot_mid,vot_right]
    
    return vot_list

def overlap_check(center_vot,neighbor_vot,overlap_lon,overlap_lat,overlap_index,center_lon,neighbor_lon):
    #Here I should mark both if it is in the overlap region and if it is marked as too close
    #to the edge
    if max(center_lon) > max(neighbor_lon):
        lon=neighbor_vot['lon'][np.where(  neighbor_vot['lon'] > min(center_lon))]
        index=np.where(  neighbor_vot['lon'] > min(center_lon)) 
        lat=neighbor_vot['lat'][np.where(  neighbor_vot['lon'] > min(center_lon))]
     
    else:
        lon=neighbor_vot['lon'][np.where( neighbor_vot['lon'] < max(center_lon))]
        index=np.where(  neighbor_vot['lon'] < max(center_lon))
        lat=neighbor_vot['lat'][np.where(  neighbor_vot['lon'] < max(center_lon) )]
        
    overlap_lon.append(lon)
    overlap_lat.append(lat)
    overlap_index.append(index)


    return overlap_lon,overlap_lat,overlap_index

def get_phot(name,folder):
    
    print(name, folder)
    
    #left=np.load(folder[0]+'/'+name[0]+'_full_table.npy',allow_pickle=True)
    #center=np.load(folder[1]+'/'+name[1]+'_full_table.npy',allow_pickle=True)
    #right=np.load(folder[2]+'/'+name[2]+'_full_table.npy',allow_pickle=True)
    
    left=read_info(folder[0]+names[0]+'_full_table_cut.vot')
    center=read_info(folder[1]+names[1]+'_full_table_cut.vot')
    right=read_info(folder[2]+names[2]+'_full_table_cut.vot')
    
    #read_info(folder[1]+'/'+names[1]+'_Mosaic_Mom0_comp.vot')
    phot_table=[left,center,right]
    
    return phot_table

#This unify coordiantes is not the same as the one in meerMod, need to unify, lol
def unify_coords(table,w):
    #This is it get the world coordinate system and also translate the table values to pixel values
    lon=table['lon'].data
    lat=table['lat'].data
    t=0
    test_arr=[]
    for x in lon:
        test=np.array([lon[t], lat[t]], np.float_)
        test_arr.append(test)               
        t=t+1
    positions=w.wcs_world2pix(test_arr, 2)
    
    return positions

def coords_table(cube,cubeNames,table):
    positions=[]
    all_pos=[]
    for num, name in enumerate(cubeNames):
        hdul = fits.open(cube[num]+cubeNames[num]+"_Mosaic_chan01.fits")
        w = WCS(hdul[0].header,naxis=2)
        positions[num:]= [unify_coords(table[num],w)]
    return positions

def make_table(shape):
    dtype = [('id', 'int32'),('field','object'),\
             ('chan01', 'float64'), ('chan01err', 'float64'),\
             ('chan02', 'float64'), ('chan02err', 'float64'),\
             ('chan03', 'float64'), ('chan03err', 'float64'),\
             ('chan04', 'float64'), ('chan04err', 'float64'),\
             ('chan05', 'float64'), ('chan05err', 'float64'),\
             ('chan06', 'float64'), ('chan06err', 'float64'),\
             ('chan07', 'float64'), ('chan07err', 'float64'),\
             ('chan08', 'float64'), ('chan08err', 'float64'),\
             ('chan09', 'float64'), ('chan09err', 'float64'),\
             ('chan10', 'float64'), ('chan10err', 'float64'),\
             ('chan11', 'float64'), ('chan11err', 'float64'),\
             ('chan12', 'float64'), ('chan12err', 'float64'),\
             ('chan13', 'float64'), ('chan13err', 'float64'),\
             ('chan14', 'float64'), ('chan14err', 'float64'),\
             ('si_m','float64'),('si_point_num','int32'),\
             ('xi','float64'),('pvalue','float64'),\
             ('overlap','float64'),('overlap_field','object'),\
             ('edge','bool'),('overlap_mask','bool')]
    full_table = Table(data=np.zeros(shape, dtype=dtype))
    return full_table

location='/beegfs/car/bsmart/MeerKAT/Mosaic_Planes/'
#location='/d/MeerKAT/Test/'

parser = argparse.ArgumentParser(description='Must have folder location')
parser.add_argument("--file_one")
parser.add_argument("--file_two")
parser.add_argument("--file_three")

args = parser.parse_args()

if args.file_one  == None :
    print("Must have folder locations. Please include --file_one='filepath',--file_two='filepath',--file_three='filepath'")
    exit()
folder_one= args.file_one
folder_two= args.file_two
folder_three= args.file_three

min_res=0.00222222/4.0

#folder_one= '/d/MeerKAT/Test/G345.5+000I'
#folder_two= '/d/MeerKAT/Test/G357.5+000I'
#folder_three= '/d/MeerKAT/Test/G002.5+0.0IFx'

folder=[]
folder.append(folder_one)
folder.append(folder_two)
folder.append(folder_three)
names=[]
images=[]
for k in folder:
    name=get_name(k)
    names.append(get_name(k))

vot_folder='/beegfs/car/bsmart/MeerKAT/Mom0_comp_catalogs'    
    
# Load in all the relevant files here
vot_list=load_neighbors(names,vot_folder)
phot_list=get_phot(names,folder)
positions=coords_table(folder,names,vot_list)
for i ,name in enumerate(names):
    images.append(get_image(folder[i]+name+'_Mosaic_chan01.fits'))
    
lon_range=np.empty([3, 2])
lon_range[:]=np.nan

#Get all the min and max of the longitudes for each cube here
for i in range(3):
    min_lon,max_lon=minmax_coord(images[i][1])
    lon_range[i,0]=min_lon
    lon_range[i,1]=max_lon

#Check if a point is too close to the edge and mark here

for i in range(3):
    for index, j in enumerate(vot_list[i]['lon']):
        if j <= (lon_range[i,0]+.01):
            phot_list[i]['edge'][index]=True
        elif j >= (lon_range[i,1]-.01):
            phot_list[i]['edge'][index]=True

#This sorts all of the overlapping points. I think?? I combine both neighbors into just the
#overlap neighbor?

overlap_lon_neighbor=[]
overlap_lat_neighbor=[]
overlap_index_neighbor=[]
overlap_lon_center=[]
overlap_lat_center=[]
overlap_index_center=[]

overlap_lon_neighbor,overlap_lat_neighbor,overlap_index_neighbor=overlap_check(vot_list[1],vot_list[0],overlap_lon_neighbor,overlap_lat_neighbor,overlap_index_neighbor,lon_range[1],lon_range[0])
overlap_lon_neighbor,overlap_lat_neighbor,overlap_index_neighbor=overlap_check(vot_list[1],vot_list[2],overlap_lon_neighbor,overlap_lat_neighbor,overlap_index_neighbor,lon_range[1],lon_range[2])

overlap_lon_center,overlap_lat_center,overlap_index_center=overlap_check(vot_list[0],vot_list[1],overlap_lon_center,overlap_lat_center,overlap_index_center,lon_range[0],lon_range[1])
overlap_lon_center,overlap_lat_center,overlap_index_center=overlap_check(vot_list[2],vot_list[1],overlap_lon_center,overlap_lat_center,overlap_index_center,lon_range[2],lon_range[1])

neighbor_match=[]
center_match=[]
neighbor_nomatch=[]

# I am matching the overlapping points here. In here, when I select the one matching point, the corresponding
#value in phot list must be switched to overlapping point, as well as the overlapping field + ID value

for x in range(2):
    matched_index_neighbor=[]
    nomatch_center=[]
    nomatch_neighbor=[]
    matched_index_center=[]
    matched_index_neighbor=[]
    distance_arr=[]
    for idx_first, lon in enumerate(overlap_lon_neighbor[x]):
        close_points_lon=[]
        close_points_lat=[]
        index_close=[]
        val_check=-1
        lat=overlap_lat_neighbor[x][idx_first]
        for idx_second, m in enumerate(overlap_lon_center[x]):
            if lon-min_res <= m <= lon+min_res:
                close_points_lon.append(m)
                close_points_lat.append(overlap_lat_center[x][idx_second])
                index_close.append(idx_second)
                val_check=0
        if close_points_lon != [] and val_check != -1:
            #Pretty sure the match happens here
            minimum=min(np.sqrt(np.square(close_points_lon-lon)+np.square(close_points_lat-lat)))   
            close_index=np.where(np.sqrt(np.square(close_points_lon-lon)+np.square(close_points_lat-lat)) == minimum)[0]
            print('Close index')
            print(index_close[close_index[0]])
            distance_arr.append(minimum)
            matched_index_center.append(index_close[close_index[0]])
            matched_index_neighbor.append(idx_first)
            
        else:
            nomatch_neighbor.append(idx_first)

    neighbor_match.append(matched_index_neighbor)
    neighbor_nomatch.append(nomatch_neighbor)
    center_match.append(matched_index_center)
    
for i in range(2):
    for j,name in enumerate(center_match[i]):           
            if i ==0:
                phot_list[0]['overlap'][overlap_index_neighbor[0][0][neighbor_match[i][j]]]=phot_list[1]['id'][overlap_index_center[i][0][center_match[i][j]]]
                phot_list[0]['overlap_field'][overlap_index_neighbor[0][0][neighbor_match[i][j]]]=phot_list[1]['field'][0]
                phot_list[1]['overlap'][overlap_index_center[0][0][center_match[i][j]]]=phot_list[0]['id'][overlap_index_neighbor[i][0][neighbor_match[i][j]]]
                phot_list[1]['overlap_field'][overlap_index_center[0][0][center_match[i][j]]]=phot_list[0]['field'][0]
                phot_list[1]['overlap_mask'][overlap_index_center[0][0][center_match[i][j]]]=True
            else:
                phot_list[2]['overlap'][overlap_index_neighbor[i][0][neighbor_match[i][j]]]=phot_list[1]['id'][overlap_index_center[i][0][center_match[i][j]]]
                phot_list[2]['overlap_field'][overlap_index_neighbor[i][0][neighbor_match[i][j]]]=phot_list[1]['field'][0]
                phot_list[1]['overlap'][overlap_index_center[1][0][center_match[i][j]]]=phot_list[2]['id'][overlap_index_neighbor[i][0][neighbor_match[i][j]]]
                phot_list[1]['overlap_field'][overlap_index_center[1][0][center_match[i][j]]]=phot_list[2]['field'][0]
                phot_list[2]['overlap_mask'][overlap_index_neighbor[i][0][neighbor_match[i][j]]]=True
valuesArr=[]
for channel in range(14):  
    val_list=[]
    for x in range(2):
        x_line = np.linspace(0, 2, 100)
        print(f'Values for {channel}')
        values=[]
        values2=[]
        for n in range(len(center_match[x])):
            values.append(phot_list[1]['chan'+'{:02d}'.format(channel+1)][overlap_index_center[x][0][center_match[x][n]]])
            values2.append(phot_list[0+x*2]['chan'+'{:02d}'.format(channel+1)][overlap_index_neighbor[x][0][neighbor_match[x][n]]])
        #Skips the empty planes
        if np.isnan(values).all() == True and np.isnan(values2).all() == True:
            print('No values')
        else:    
            #This checks both arrays at the same time.
            #This one is the left one
            #They contain the good matches, all the values, and a seperate list of matches  that are bad
            if x == 0:            
                val_list[0:]=[values,]
                val_list[1:]=[values2,]
                matchedArr=fit_deviation(values,values2)
                val_list[2:]=[matchedArr,]

                
                outliers=np.where(abs(matchedArr) >= 0.15)
                val_list[3:]=[outliers,]
            #This is the right image
            else:
                print(channel)
                val_list[4:]=[values,]
                val_list[5:]=[values2,]
                matchedArr=fit_deviation(values,values2)
                val_list[6:]=[matchedArr,]

                outliers=np.where(abs(matchedArr) >= 0.15)
                val_list[7:]=[outliers,]
        plt.suptitle('Main title') # or plt.suptitle('Main title')
    #This is a sanity check, not needed
    #if len(val_list) < 5:
    #    print('No values')
    #elif not val_list or np.isnan(val_list[1]).all() or (np.isnan(val_list[4]).all() and np.isnan(val_list[5]).all() ):
    #    print('No values')
    #else:  
    #    plt.suptitle(f'Channel {channel} overlapping points') # or plt.suptitle('Main title')
    #    f, axarr = plt.subplots(1,4,sharey=False,gridspec_kw = {'wspace':0, 'hspace':0})
    #    axarr[0].plot(x_line,x_line, 'r--')   
    #    axarr[0].scatter(val_list[0],val_list[1])
    #    if np.isnan(val_list[2]).all() != True:
    #        axarr[1].hist(abs(val_list[2]), 10, histtype='bar', rwidth=0.8)
    #    axarr[2].plot(x_line,x_line, 'r--')   
    #    axarr[2].scatter(val_list[4],val_list[5])
    #    if np.isnan(val_list[6]).all() != True:
    #        axarr[3].hist(abs(val_list[6]), 10, histtype='bar', rwidth=0.8)
    #valuesArr[channel:]=[val_list]
    
for i in range(3):
    shape=len(phot_list[i]['id'])
    full_table=make_table(shape)
    for j in range(shape):
        full_table[j]=phot_list[i][j]
    full_table.write(f'{location}/{names[i]}/{names[i]}_full_table_cut.vot', format='votable',overwrite=True) 