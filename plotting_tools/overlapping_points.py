import matplotlib.pyplot as plt
import numpy as np


def plot(cubes, photometry_tables, show=True, save = False):
    plt.rcParams["axes.grid"] = False
    plt.rcParams['xtick.labelsize'] = 8
    plt.rcParams['ytick.labelsize'] = 8

    #Will create an image or plot each channel and the overlapping points
    for channel in range(14):
        f, axarr = plt.subplots(1, 3, sharey=True, gridspec_kw={'wspace': 0, 'hspace': 0})

        for im in range(3, 0, -1):
            overlapping_points = np.where(photometry_tables[im - 1]['overlap'] >= 0)
            axarr[3 - im].imshow(cubes[im - 1].channels[channel].data, cmap='gray', vmin=-.004, vmax=.004)
            axarr[3 - im].scatter(cubes[im - 1].positions[overlapping_points, 0],
                                  cubes[im - 1].positions[overlapping_points, 1], s=1)
        f.subplots_adjust(hspace=0)

        for ay in axarr:
            ay.label_outer()

        if save:
            plt.savefig(
                '/Volumes/200GB/MeerKAT/' + cubes[0].folder_name + '/' + cubes.folder_name + "chan" + "{:02d}".format(
                    channel + 1) + "_overlapping_points.png", dpi=600)

        if show:
            plt.show()
            plt.close(f)
