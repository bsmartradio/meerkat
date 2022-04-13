import matplotlib.pyplot as plt
import common.data_helper as helper

def plot_channels(cubes, cubeNames, overlap_index_center, overlap_index_neighbor, positions, valuesArr):
    plt.rcParams["axes.grid"] = False
    plt.rcParams['xtick.labelsize'] = 8
    plt.rcParams['ytick.labelsize'] = 8
    for channel in range(14):
        f, axarr = plt.subplots(1, 3, sharey=True, gridspec_kw={'wspace': 0, 'hspace': 0})
        for im in range(3, 0, -1):
            image_data = helper.get_image(
                cubes[im - 1] + '/' + cubeNames[im - 1] + "_Mosaic_chan" + "{:02d}".format(channel + 1) + ".fits")
            print(image_data[0][0].any())
            if valuesArr[channel]:
                axarr[3 - im].imshow(image_data[0], cmap='gray', vmin=-.004, vmax=.004)
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
        plt.savefig('/Volumes/200GB/MeerKAT/' + cubeNames[1] + '/' + cubeNames[1] + "chan" + "{:02d}".format(
            channel + 1) + "_outliers.png", dpi=600)
        plt.show()
        plt.close(f)
