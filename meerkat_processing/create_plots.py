from plotting_tools import all_sources
from plotting_tools import overlapping_points
from plotting_tools import bright_sources
import common.phot_helper as phot_helper
import models.image as image


def begin_plotting(folder_one, folder_two, folder_three, all=False, bright=False):

    folder = [folder_one, folder_two, folder_three]

    data_cubes = [image.Image(folder_one), image.Image(folder_two), image.Image(folder_three)]

    phot_tables = []

    for i in range(3):
        phot_tables.append(
            phot_helper.load_phot_table(folder[i] + '/' + data_cubes[i].folder_name + '_full_table_cut.npy'))

    if all:
        all_sources.plot(data_cubes, show=True)

    if bright:
        bright_sources.plot(data_cubes, phot_tables, show=True)

