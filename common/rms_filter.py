import numpy as np

def rms_cut(data_cube, full_table):
    total_cut = np.zeros(14)
    for k in range(14):
        print(k)
        if np.isnan(data_cube.rms[k].data).any():
            print(np.isnan(data_cube.rms[k].data).any())
            mean_rms = np.nanmean(data_cube.rms[k].data)
            for j in range(len(full_table["chan" + "{:02d}".format(k + 1)])):
                val = full_table["chan" + "{:02d}".format(k + 1)][j]
                if val <= mean_rms * 5.0:
                    full_table["chan" + "{:02d}".format(k + 1)][j] = np.nan
                    total_cut[k] = total_cut[k] + 1

                elif val <= full_table["chan" + "{:02d}".format(k + 1) + "err"][j] * 3.0:
                    full_table["chan" + "{:02d}".format(k + 1)][j] = np.nan
                    total_cut[k] = total_cut[k] + 1

    return total_cut, full_table