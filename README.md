# MeerKAT Point Source Catalog SED Processing and Plotting Tools

Supporting programs for the creation of an SED catalog for a MeerKAT data cubes.
These programs were developed in [Pycharm community edition.](https://www.jetbrains.com/pycharm/download/#section=mac)

###Programs required:
- phython 3.7
- [Aegean Processing Package](https://github.com/PaulHancock/Aegean)
- astropy
- photutils

If you have access to the Cambridge HPC, it is recommended you use the meerkat singularity container available there. 
The container has a version of python 3.7 and a version of the aegean processing tools which
are guaranteed to run with all the programs in this package. The meerkat singularity container will be publicly available
in the future and include everything within this package.

### Setup

The current structure of these programs expects the relevant aegean point sources
and meerkat data cubes to be in the following locations:

    filepath/Mosaic_Planes
    filepath/Mom0_comp_catalogs

Make sure you have both Mosaic_Planes and the Mom0_comp_catalogs in the same location.

###How to use

To run any of the meerkat processing routines, you need to run main and pass it the desired process.
You then must also supply any supporting arguments. 

The possible arguments you may supply are the following.

__For bane, photometry, and combine:__

    --process = 'bane' 
    --folder_loc = 'filepath/Mosaic_Planes/G282.5-Fx/'

__For assign_id and full_catalog:__

    --process = 'assign_id'
    --main_folder = 'filepath/Mosaic_Planes/'

For neighbors and plotting:

    --process = 'neighbors'
    --folder_one = 'filepath/Mosaic_Planes/G279.5-Fx/'
    --folder_two = 'filepath/Mosaic_Planes/G282.5-Fx/'
    --folder_three = 'filepath/Mosaic_Planes/G285.5-Fx/'

For example, to run photometry you would pass the following arguments in:

    python3 main.py --process='photometry' --folder_loc='Path'

###Processes in this package

- __bane_processing__ - This is required if none of the individual mosaic_planes have backgrounds and just the channels and 
Aegean vot files have been downloaded. This will run bane on all the individual channels, creating background and rms files.


- __photometry.py__ - Uses aperture photometry and the point source catalog to create aperture photometry catalogs for each 
channel in a MeerKAT cube. If the aegean vot tables or individual backgrounds are missing, the program
will not run and raise an error pertaining to the missing data.

- __combine_photometry.py__ - Takes the separate channel photometry catalogs and combines them into a single catalog for an 
individual cube. Note that the output is saved both as a vot file and as a .npy file. 
An rms and error cut are run on the files, changing any values which are either below 5 times
below the rms or 3 times below the error. The non-cut catalog is saved as '_full_catalog' and the
rms and error cut are saved as '_full_catalog_cut.' The spectral index fitting is then run
on the cut table, with any source with less than 5 values ignored and not fit.
At this point the catalogs are not
complete, with no catalog ID or processing investigating neighboring cubes. The following files
expect the cut tables.


- __assign_id.py__: This program takes in combined photometry files and looks at all processed files. Starting
at the lowest longitude, it assigns and ID to each source in the catalog. It does the same for the Aegean vot
files, allowing for both catalogs to have the same catalog ID's for cross-referencing.
It does not make cuts or leave
out ID assignment for points that are bellow the 3 or 5 sigma level so all identified sources in the combined
map will have an ID even if they are not assigned a spectral index in the final catalog. If the full
catalog is not processed or cubes are missing, the program will not skip cubes, it will continue assigning
ID's. This allows for sub-catalogs with their own unique ID's to be made.


- __process_neighbors.py__: This program takes 3 adjacent cubes and compares any points that are overlapping between
the central image and the images on its left and right. It then marks any points that are in the overlap region,
and finds sources which are present in both catalogs. 


- __full_catalog.py__: Combines all the full catalogs in each cube folder into a master list. Does the same
for the Aegean vot files.
This program should only be run when all the specific flags, spectral indexes, and any other
changes to the catalogs have been made.


- __create_plots.py__: Allows for plotting individual cubes and channels in the catalog. 
Expects 3 adjacent cubes at this time, as well as the catalogs for individual cubes and not the full catalog.
Currently plotting is set up for bright sources, sources present in adjacent images, and plotting all sources.
Due to the high number of sources, it is better to plot only the sources present in both images or the sources
present only in one for visibility.


###Recommended processing order:

If starting with just the aegean vot files and mosaic plane fles, the following order is recommended:

- bane
- photometry
- combine
- assign_id
- neighbors
- full_catalog
- plotting

###Notes:

Most of these programs are expected to be run on an HPC due to the time it takes to process 
and the multiprocessing requirements. Specifically, photometry and bane are time intensive.
jobSubmitters currently contains examples of submitting specific meerkat processing 
jobs by running through all the desired folders. The specific slurm configuration files are not currently
in this package.

Currently, all output files are written into their respective Mosaic_Plane cube folders.
