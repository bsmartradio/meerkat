import argparse
import meerkat_processing.photometry as photometry
import meerkat_processing.bane_processing as bane_processing
import meerkat_processing.assign_id as assign_id
import meerkat_processing.combine_photometry as combine_photometry
import meerkat_processing.full_catalog as full_catalog
import meerkat_processing.process_neighbors as process_neighbors
import meerkat_processing.create_plots as create_plots
import os
import logging
from app_logging import logger
from common.main_checks import check_folder_loc, check_main_folder, check_multi_folders


def start_photometry(args):
    check_folder_loc(args)

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


def start_bane(args):
    check_folder_loc(args)

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


def start_combine(args):
    check_folder_loc(args)

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


def start_assign_id(args):
    check_main_folder(args)

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


def start_full_catalog(args):
    check_main_folder(args)

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


def start_neighbors(args):
    check_multi_folders(args)

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


def start_plotting(args):
    check_multi_folders(args)

    folder_one = args.folder_one
    folder_two = args.folder_two
    folder_three = args.folder_three
    path_check_one = os.path.isdir(folder_one)
    path_check_two = os.path.isdir(folder_two)
    path_check_three = os.path.isdir(folder_three)

    if path_check_one and path_check_two and path_check_three:
        try:
            logging.info('Beginning Plotting')
            create_plots.begin_plotting(folder_one, folder_two, folder_three, all=False, bright=True)
        except Exception as e:
            logging.exception(msg='Exception in Plotting.', exc_info=e)
    else:
        logging.warning('Please check all three folder paths are valid to run Plotting.')


if __name__ == '__main__':

    logger.init(logging.DEBUG, '.', 'app_logging')

    parser = argparse.ArgumentParser(description='Please indicate which process you will be running:'
                                                 'Bane,Photometry, Combine, Full_Catalog, Neighbors, Assign_Id. Bane,'
                                                 ' Photometry and Combine require --folder_loc. Neighbors requires '
                                                 '--folder_one, --folder_two, and --folder_three. Assign_ID and '
                                                 'Full_Catalog require --main_folder.')
    parser.add_argument('--process')
    parser.add_argument('--folder_loc')
    parser.add_argument('--main_folder')
    parser.add_argument('--folder_one')
    parser.add_argument('--folder_two')
    parser.add_argument('--folder_three')

    args = parser.parse_args()

    if not args.process:
        logging.warning('Please indicate which process you will be running using --process. \n'
                        'Available processes: Bane, Photometry, Combine, Full_Catalog, Neighbors, or Assign_Id. \nBane,'
                        ' Photometry and Combine require --folder_loc. \nNeighbors requires '
                        '--folder_one, --folder_two, and --folder_three. \nAssign_ID and '
                        'Full_Catalog require --main_folder.')

    if args.process.lower() == 'photometry':
        start_photometry(args)
        exit()
    elif args.process.lower() == 'bane':
        start_bane(args)
        exit()
    elif args.process.lower() == 'combine':
        start_combine(args)
        exit()
    elif args.process.lower() == 'assign_id':
        start_assign_id(args)
        exit()
    elif args.process.lower() == 'full_catalog':
        start_full_catalog(args)
        exit()
    elif args.process.lower() == 'neighbors':

        start_neighbors(args)
        exit()
    elif args.process.lower() == 'plotting':

        start_plotting(args)
        exit()
    else:
        logging.warning('Input for --process is not recognized. Please check argument and choose from the following '
                        'list:\nbane, photometry, combine, full_catalog, assign_id, neighbors.')
