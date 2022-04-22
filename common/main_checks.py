import logging


def check_folder_loc(args):
    if args.folder_loc is None:
        logging.warning('Must have folder location.\nPlease include --folder_loc="filepath/foldername" argument.\n'
                        'Example: --folder_loc="Example/test_data/Mosaic_Planes/G282.5-0.5IFx/"')
        exit()


def check_main_folder(args):
    if args.main_folder is None:
        logging.warning("Must have main folder location containing all processed cube folders. Please include"
                        " --main_folder='filepath'")
        logging.warning("Example: --main_folder='Example/test_data/Mosaic_Planes/'")
        exit()


def check_multi_folders(args):
    if args.folder_one is None or args.folder_two is None or args.folder_three is None:
        logging.warning("Must have three folder locations.\nPlease include --folder_one='filepath', "
                        "--folder_two='filepath', and --folder_three='filepath' \n"
                        "Example:\n--folder_one='/Example/test_data/Mosaic_Planes/G279.5-0.5IFx/'\n"
                        "--folder_two='/Example/test_data/Mosaic_Planes/G282.5-0.5IFx/'\n"
                        "--folder_three='/Example/test_data/Mosaic_Planes/G285.5-0.5IFx/'")
        exit()