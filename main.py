import argparse
import meerkat_processing.photometry as photometry
import meerkat_processing.bane_processing as bane_processing
import meerkat_processing.assign_id as assign_id
import meerkat_processing.combine_photometry as combine_photometry
import meerkat_processing.full_catalog as full_catalog
import meerkat_processing.process_neighbors as process_neighbors
import os
import logging
from app_logging import logger

if __name__ == '__main__':

    logger.init(logging.DEBUG, '.', 'app_logging')

    parser = argparse.ArgumentParser(description='Please indicate which process you will be running:'
                                                 'Bane,Photometry, Combine, Full_Catalog, Neighbors, Assign_Id. Bane,'
                                                 ' Photometry and Combine require --folder_loc. Neighbors requires '
                                                 '--folder_one, --folder_two, and --folder_three. Assign_ID and '
                                                 'Full_Catalog require --main_folder.')
    parser.add_argument("--process")
    parser.add_argument("--folder_loc")
    parser.add_argument("--main_folder")
    parser.add_argument("--folder_one")
    parser.add_argument("--folder_two")
    parser.add_argument("--folder_three")

    args = parser.parse_args()

    if args.process == 'photometry' or args.process == 'Photometry':

        if args.folder_loc is None:
            logging.warning("Must have folder location.\nPlease include --folder_loc='filepath/foldername' argument.\n"
                            "Example: --folder_loc='/Users/bs19aam/Documents/test_data/Mosaic_Planes/G282.5-0.5IFx/'")
            exit()

        path = args.folder_loc
        path_check = os.path.isdir(path)

        if path_check:
            try:
                logging.info('Beginning Photometry processing')
                photometry.process_photometry(path)
            except Exception as e:
                logging.exception(msg='Photometry exited without processing', exc_info=e)
        else:
            logging.warning('folder_loc does not contain a valid filepath')

    if args.process == 'bane' or args.process == 'Bane':

        if args.folder_loc is None:
            logging.warning(
                "Must have folder location. Please include --folder_loc='filepath/foldername' argument")
            logging.warning("Example: --folder_loc='/Users/bs19aam/Documents/test_data/Mosaic_Planes/G282.5-0.5IFx/'")
            exit()

        path = args.folder_loc
        path_check = os.path.isdir(path)

        if path_check:
            try:
                logging.info('Beginning Bane background processing')
                bane_processing.begin_bane(path)
            except Exception as e:
                logging.exception(msg='Bane exited without processing', exc_info=e)
        else:
            logging.warning('folder_loc does not contain a valid filepath')

    if args.process == 'combine' or args.process == 'Combine':

        if args.folder_loc is None:
            logging.warning(
                "Must have folder location. Please include --folder_loc='filepath/foldername'")
            logging.warning("Example: --folder_loc='/Users/bs19aam/Documents/test_data/Mosaic_Planes/G282.5-0.5IFx/'")
            exit()

        path = args.folder_loc
        path_check = os.path.isdir(path)

        if path_check:
            try:
                logging.info('Beginning Combine')
                combine_photometry.begin_combine(path)
            except Exception as e:
                logging.exception(msg='Combine exited without processing', exc_info=e)
        else:
            logging.warning('folder_loc does not contain a valid filepath')

    if args.process == 'assign_id' or args.process == 'Assign_id' or args.process == 'Assign_Id':

        if args.main_folder is None:
            logging.warning("Must have main folder location containing all processed cube folders. Please include"
                            " --main_folder='filepath'")
            logging.warning("Example: --main_folder='/Users/bs19aam/Documents/test_data/Mosaic_Planes/'")
            exit()

        path = args.main_folder
        path_check = os.path.isdir(path)

        if path_check:
            try:
                logging.info('Beginning Assign_ID')
                assign_id.begin_assign(path)
            except Exception as e:
                logging.exception(msg='Assign_ID exited without processing', exc_info=e)
        else:
            logging.warning('--main_folder does not contain a valid filepath')

    if args.process == 'full_catalog' or args.process == 'Full_catalog' or \
            args.process == 'Full_Catalog':

        if args.main_folder is None:
            logging.warning("Must have main folder location containing all processed cube folders. \n" 
                            "Please include --main_folder='filepath' \n" 
                            "Example: \n--main_folder='/Users/bs19aam/Documents/test_data/Mosaic_Planes/'")
            exit()

        path = args.main_folder
        path_check = os.path.isdir(path)

        if path_check:
            try:
                logging.info('Beginning Full_Catalog')
                full_catalog.begin_full_catalog(path)
            except Exception as e:
                logging.exception(msg='Full catalog exited without processing', exc_info=e)
        else:
            logging.warning('--main_folder does not contain a valid filepath')

    if args.process == 'neighbors' or args.process == 'Neighbors':

        if args.folder_one is None or args.folder_two is None or args.folder_three is None:
            logging.warning("Must have three folder locations.\nPlease include --folder_one='filepath', "
                            "--folder_two='filepath', and --folder_three='filepath' \n" 
                            "Example:\n--folder_one='/Users/bs19aam/Documents/test_data/Mosaic_Planes/G279.5-0.5IFx/'\n" 
                            "--folder_two='/Users/bs19aam/Documents/test_data/Mosaic_Planes/G282.5-0.5IFx/'\n" 
                            "--folder_three='/Users/bs19aam/Documents/test_data/Mosaic_Planes/G285.5-0.5IFx/'")
            exit()

        folder_one = args.folder_one
        folder_two = args.folder_two
        folder_three = args.folder_three
        path_check_one = os.path.isdir(folder_one)
        path_check_two = os.path.isdir(folder_two)
        path_check_three = os.path.isdir(folder_three)

        if path_check_one and path_check_two and path_check_three:
            try:
                logging.info('Beginning Neighbors')
                process_neighbors.begin_neighbors(folder_one, folder_two, folder_three)
            except Exception as e:
                logging.exception(msg='Exception in Nieghbors.', exc_info=e)
        else:
            logging.warning('Please check all three folder paths are valid to run Neighbors.')

    if not args.process:

        logging.warning('Please indicate which process you will be running using --process. \n'
                        'Avaliable processes: Bane, Photometry, Combine, Full_Catalog, Neighbors, or Assign_Id. \nBane,'
                        ' Photometry and Combine require --folder_loc. \nNeighbors requires '
                        '--folder_one, --folder_two, and --folder_three. \nAssign_ID and '
                        'Full_Catalog require --main_folder.')
