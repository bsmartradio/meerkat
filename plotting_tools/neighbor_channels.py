import matplotlib.pyplot as plt
import common.data_helper as helper

def plot_channels(cubes, overlap_index_center, overlap_index_neighbor, valuesArr):
    plt.rcParams["axes.grid"] = False
    plt.rcParams['xtick.labelsize'] = 8
    plt.rcParams['ytick.labelsize'] = 8
    for channel in range(14):
        f, axarr = plt.subplots(1, 3, sharey=True, gridspec_kw={'wspace': 0, 'hspace': 0})
        for im in range(3, 0, -1):
            if valuesArr[channel]:
                axarr[3 - im].imshow(cubes[im-1].channels[channel.data], cmap='gray', vmin=-.004, vmax=.004)
                if im == 1:
                    # print('')
                    axarr[3 - im].scatter(positions[0][overlap_index_neighbor[0][0][valuesArr[channel][3]], 0],
                                          positions[0][overlap_index_neighbor[0][0][valuesArr[channel][3]], 1], s=1)
                if im == 2:
                    axarr[3 - im].scatter(positions[1][overlap_index_center[1][0][valuesArr[channel][7]], 0],
                                          positions[1][overlap_index_center[1][0][valuesArr[channel][7]], 1], s=1)
                    axarr[3 - im].scatter(positions[1][overlap_index_center[0][0][valuesArr[channel][3]], 0],
                                          positions[1][overlap_index_center[0][0][valuesArr[channel][3]], 1], s=1)
                if im == 3:
                    axarr[3 - im].scatter(positions[2][overlap_index_neighbor[1][0][valuesArr[channel][7]], 0],
                                          positions[2][overlap_index_neighbor[1][0][valuesArr[channel][7]], 1], s=1)
        f.subplots_adjust(hspace=0)
        for ay in axarr:
            ay.label_outer()
        plt.savefig('/Volumes/200GB/MeerKAT/' + cubes[0].folder_name+ '/' + cubes.folder_name + "chan" + "{:02d}".format(
            channel + 1) + "_outliers.png", dpi=600)
        plt.show()
        plt.close(f)

def all_sources(cubes, show=False, save = True):
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
            plt.savefig(cubes[0].location + '/' + cubes.folder_name + "chan" + "{:02d}".format(channel + 1)
                        + "_all_sources.png", dpi=600)
        if show:
            plt.show()
            plt.close(f)
