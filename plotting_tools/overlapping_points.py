import matplotlib.pyplot as plt
import numpy as np

def plot(cubes, n_sources):
    plt.rcParams["axes.grid"] = False
    plt.rcParams['xtick.labelsize'] = 8
    plt.rcParams['ytick.labelsize'] = 8
    for channel in range(14):
        f, axarr = plt.subplots(1, 3, sharey=True, gridspec_kw={'wspace': 0, 'hspace': 0})
        for im in range(3, 0, -1):
            axarr[3 - im].imshow(cubes[im-1].channels[channel].data, cmap='gray', vmin=-.004, vmax=.004)
            if im == 1:
                matched=np.array(n_sources.left.overlap_index[0][0])
                axarr[3 - im].scatter(cubes[im-1].positions[matched][:, 0],
                                      cubes[im-1].positions[matched][:, 1], s=1)
            if im == 2:
                matched = np.array(n_sources.center_right.overlap_index[0][0])
                axarr[1].scatter(cubes[1].positions[matched][:, 0],
                                      cubes[1].positions[matched][:, 1], s=1)
                matched = np.array(n_sources.center_left.overlap_index[0][0])
                axarr[1].scatter(cubes[1].positions[matched][:, 0],
                                      cubes[1].positions[matched][:, 1], s=1)
            if im == 3:
                matched=np.array(n_sources.right.overlap_index[0][0])
                axarr[0].scatter(cubes[im-3].positions[matched][:, 0],
                                      cubes[im-3].positions[matched][:, 1], s=1)
        f.subplots_adjust(hspace=0)
        for ay in axarr:
            ay.label_outer()
        plt.savefig('/Volumes/200GB/MeerKAT/' + cubes[0].folder_name+ '/' + cubes.folder_name + "chan" + "{:02d}".format(
            channel + 1) + "_outliers.png", dpi=600)
        plt.show()
        plt.close(f)

