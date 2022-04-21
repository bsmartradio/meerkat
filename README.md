# MeerKAT Point Source Catalog SED Processing and Plotting Tools

Supporting programs for the creation of an SED catalog for a MeerKAT data cubes.

Recommended processing order:

bane_processing - This is required if none of the individual mosaic_planes have backgrounds and just the channels and 
Aegean vot files have been downloaded. This will run bane on all the individual channels, creating background and rms files.

photometry.py - Uses aperture photometry and the point source catalog to create aperture photometry catalogs for each 
channel in a MeerKAT cube. If the aegean vot tables or individual backgrounds are missing, the program
will not run and raise an error pertaining to the missing data.

combine_photometry.py - Takes the separate channel photometry catalogs and combines them into a single catalog for an 
individual cube. Note that the output is saved both as a vot file and as a .npy file. 
An rms and error cut are run on the files, changing any values which are either below 5 times
below the rms or 3 times below the error. The non-cut catalog is saved as '_full_catalog' and the
rms and error cut are saved as '_full_catalog_cut.' The spectral index fitting is then run
on the cut table, with any source with less than 5 values ignored and not fit.

At this point the catalogs are not
complete, with no catalog ID or processing investigating neighboring cubes. The following files
expect the cut tables, however a flag can be set to look at the non-cut ones as well.

assign_id.py: This program takes in combined photometry files and looks at all processed files. Starting
at the lowest longitude, it assigns and ID to each source in the catalog. It does the same for the Aegean vot
files, allowing for both catalogs to have the same catalog ID's for cross-referencing.
It does not make cuts or leave
out ID assignment for points that are bellow the 3 or 5 sigma level so all identified sources in the combined
map will have an ID even if they are not assigned a spectral index in the final catalog. If the full
catalog is not processed or cubes are missing, the program will not skip cubes, it will continue assigning
ID's. This allows for sub-catalogs with their own unique ID's to be made.

process_neighbors.py: This program takes 3 adjacent cubes and compares any points that are overlapping between
the central image and the images on its left and right. It then marks any points that are in the overlap region,
and finds sources which are present in both catalogs. If a plot flag is set, it is possible
to plot all overlapping sources or all sources present in both images. 

Note: Due to the high number of sources, it is better to plot only the sources present in both images or the sources
present only in one for visibility.

full_catalog.py: Combines all the full catalogs in each cube folder into a master list. Does the same
for the Aegean vot files.
This program should only be run when all the specific flags, spectral indexes, and any other
changes to the catalogs have been made.

Notes:
jobSubmitters are currently examples of submitting specific meerkat processing job to the Cambridge HPC using slurm. 
