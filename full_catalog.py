#ALL of the aegean id files and concat them together, same with the photometry files.


import numpy as np
import glob
from astropy.io.votable.tree import VOTableFile, Resource, Table, Field
from astropy.table import QTable, Table, Column
from meerMod import *
from astropy.io.votable import parse_single_table

def get_vots(location):
    
    vot_list=sorted(glob.glob(location+"*_Mosaic_Mom0_comp.vot+id"))
    for i in range(len(vot_list)):
        
        #Makes the initial table and then fills it in
        if i == 0:
            table = parse_single_table(vot_list[i]) 
            shape=len(table.array)
            full_table=make_table(shape,aegean=True,table_type=table.array)
            
            for i in range(shape):
                full_table[i]=table.array[i]
        #Takes the other tables and concats them onto the end. For some reason nans all become 0s :/    
        else:
            table=parse_single_table(vot_list[i])   
            for i in range(len(table.array)):
                full_table.add_row(table.array[i])  
    return full_table

                
def get_phots(location):
    phot_list=sorted(glob.glob(location+"G*/*_full_table_cut.vot"))
    for i in range(len(phot_list)):
        
        #Makes the initial table and then fills it in
        if i == 0:
            table = parse_single_table(phot_list[i]) 
            shape=len(table.array)
            full_table=make_table(shape)
            
            for i in range(shape):
                full_table[i]=table.array[i]
        #Takes the other tables and concats them onto the end. For some reason nans all become 0s :/    
        else:
            table=parse_single_table(phot_list[i])   
            for i in range(len(table.array)):
                full_table.add_row(table.array[i])
        
    return full_table
                  
                  
def make_table(shape, aegean=False, table_type=[]):
    
    if aegean:
        dtype=np.dtype(table_type.dtype.descr)
    else:
    
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
     
    
    
    
vot_location='/beegfs/car/bsmart/MeerKAT/Mom0_comp_catalogs/'
phot_location='/beegfs/car/bsmart/MeerKAT/Mosaic_Planes/'

#full_table=get_phots(phot_location)

#for i in range(14):
#    for j in range(len(full_table)):
#        if full_table["chan"+"{:02d}".format(i+1)][j] == 0:
#            full_table["chan"+"{:02d}".format(i+1)][j]=np.nan
            
#for i in range(14):
#    for j in range(len(full_table)):
#        if full_table["si_point_num"][j] == -2147483648:
#            full_table["si_point_num"][j]=np.nan
            
#for i in range(14):
#    for j in range(len(full_table)):
#        if full_table["overlap"][j] == 1:
#            full_table["overlap"][j]=np.nan

#full_table.write(f'{phot_location}MeerKAT_full_phot_catalog.vot', format='votable',overwrite=True)

full_table_vot=get_vots(vot_location)


full_table_vot.write(f'{vot_location}MeerKAT_full_Aegean_catalog.vot', format='votable',overwrite=True)
           
