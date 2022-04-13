import common.data_checks as checks
import os
import common.data_helper as helper

# Read in file name argument.
parser = argparse.ArgumentParser(description='Must give folder name')
parser.add_argument("--folder_location")

args = parser.parse_args()

if args.input_folder == None:
    print("Must have folder location'")
    exit()
files = args.input_folder

location = files.strip()
print(location)
print("Checking if all files are named correctly")
checks.file_check(location)
name = helper.get_name(location)
print(location)
fileslist = os.listdir(location.strip())
c_list, b_list = channel_list(fileslist)

# Writes a list of all of the channel files which can be used in other programs
if os.path.isfile(location + name + '_missing_backgrounds_list.txt'):
    c_list = []
    print('Reading existing channel file.')
    with open(location + name + '_channels_list.txt', 'r') as filehandle:
        c_list = filehandle.read().splitlines()
else:
    print('Writing new channels file.')
    with open(location + name + '_channels_list.txt', 'w') as filehandle:
        filehandle.writelines("%s\n" % place for place in c_list)
# Writes a list of all of the backgrounds created files which can be used in other programs
print(c_list)
print(len(c_list))
print(len(b_list))

# checks if bane has already been run on the subfolder
if len(c_list) == len(b_list):
    print('Bane has already been run on all channels for' + location)
# If bane has been run on some but not all, warns you.
elif len(b_list) > 0:
    print('Bane has already been run on some channels. Re-running Bane')
    for i in c_list:
        run_bane(location, i)
# Runs bane if there is no existing background files
else:
    for i in c_list:
        run_bane(location, i)
        print("Running Bane on all channels.")

dirs = os.listdir(location)
with open(location + name + '_background_list.txt', 'w') as filehandle:
    for i in dirs:
        if 'bkg.fits' in i:
            filehandle.writelines(i + '\n')
            print(i + ' written to background list.')

print('Checking that all channels have a background')

if os.path.isfile(location + name + '_missing_background_list.txt'):
    print(
        'Channels missing background files have already been moved into ' + location + name + '_missing_background_list.txt')

else:
    s = b_list
    full_list = listToString(s)
    missing = []
    print(i)
    print(c_list)
    for i in b_list:
        channel = str(re.findall(r'\_c.*?\.', i))
        channel = channel[3:-3]
        if channel in full_list:
            print('Channel ' + channel + ' has background')

        else:
            print('Channel ' + channel + ' does not have background. Channel removed from list')
            with open(location + name + '_channels_list.txt', 'r') as f:
                lines = f.readlines()
            with open(location + name + '_channels_list.txt', 'w') as f:
                for line in lines:
                    if line.strip("\n") != i:
                        f.write(line)
            with open(location + name + '_missing_background_list.txt', 'w') as f:
                missing.append(i)

    if len(missing) > 0:
        print('There are ' + str(len(missing)) + ' missing background files')
        with open(location + name + '_missing_background_list.txt', 'w') as f:
            for k in missing:
                f.write(k)