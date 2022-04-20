from matplotlib import pyplot as plt


def plot(cubes, show=False, save = True):
    plt.rcParams["axes.grid"] = False
    plt.rcParams['xtick.labelsize'] = 8
    plt.rcParams['ytick.labelsize'] = 8
    for channel in range(14):
        f, axarr = plt.subplots(1, 3, sharey=True, gridspec_kw={'wspace': 0, 'hspace': 0})
        for im in range(3, 0, -1):
            axarr[3 - im].imshow(cubes[im - 1].channels[channel].data, cmap='gray', vmin=-.004, vmax=.004)
            axarr[3 - im].scatter(cubes[im-1].positions[:, 0], cubes[im-1].positions[:, 1], s=1)
        f.subplots_adjust(hspace=0)
        for ay in axarr:
            ay.label_outer()
        if save:
            plt.savefig(cubes[0].path + '/' + cubes.folder_name + "chan" + "{:02d}".format(channel + 1)
                        + "_all_sources.png", dpi=600)
        if show:
            plt.show()
            plt.close(f)