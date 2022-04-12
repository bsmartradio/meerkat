def add_arguments(folder_location = False):
    if folder_location:
        parser = argparse.ArgumentParser(description='Must have folder location')
        parser.add_argument("--folder_loc")

        args = parser.parse_args()

        if args.folder_loc is None:
            print("Must have folder location. Please include --folder_loc='filepath/filename'")
            exit()

        path = args.folder_loc
        return path