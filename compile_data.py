#!/usr/bin/env python3# -*- coding: utf-8 -*-"""Created on Tue Mar  2 13:57:21 2021@author: gracedayCode to gather information from .dat files relating to coordinationenvironments in amorphous C structures at different densities.OUTLINE:    - Got 21 x 10 .dat files containing data in form:        coord_no atoms        ***      ***    - Got 21 x 10 x 3 .dat files containing density, vol per atom, energy per atom      of the given structure"""import argparseimport numpy as npparser = argparse.ArgumentParser(    description="Generate LAMMPS input files for performing dynamics "                "at 10000K at different densities."    )parser.add_argument(    "--pot",    type=str,    default="tersoff",    help="tersoff or lcbop."    )args = parser.parse_args()def read_simple_data():    densities = []    vols_per_atom = []    for factor in scalefactors:        with open(f"./deform_{factor:.2f}_{pot}/"                  f"deform_{factor:.2f}_{pot}_density.dat", "r") as density:            densities.append(float(density.read().strip()))        with open(f"./deform_{factor:.2f}_{pot}/"                  f"cool_{factor:.2f}_{pot}_60000/"                  f"cool_{factor:.2f}_{pot}_60000_volume.dat", "r"                  ) as vol_per_atom:            vols_per_atom.append(float(vol_per_atom.read().strip()))    return densities, vols_per_atomdef read_energy():    energies = []    mean_energies = []    std_energies = []    for factor in scalefactors:        for step in steps:               with open(f"./deform_{factor:.2f}_{pot}/"                      f"cool_{factor:.2f}_{pot}_{step}/"                      f"cool_{factor:.2f}_{pot}_{step}_energy.dat", "r"                      ) as energy:                energies.append(float(energy.read().strip()))        mean_energies.append(np.mean(energies))        std_energies.append(np.std(energies))    return mean_energies, std_energiesdef read_histograms():    coord_no_means = []    coord_no_stdevs = []    coord_no_averages = []    coord_no_averages_stdev = []    for factor in scalefactors:        distribution = []        for step in steps:               with open(f"./deform_{factor:.2f}_{pot}/"                      f"cool_{factor:.2f}_{pot}_{step}/"                      f"cool_{factor:.2f}_{pot}_{step}_coord_distr.dat", "r"                      ) as histogram:                data = []                lines = histogram.readlines()                for i in range(1, 8, 1):                    data.append(int((lines[i].split())[1]))            distribution.append(data)  # this is 10 sets of 7 data points        transposed_distribution = [            [row[i] for row in distribution] for i in range(7)            ]        coord_no_means.append(            [np.mean(row) for row in transposed_distribution]            )        coord_no_stdevs.append(            [np.std(row) for row in transposed_distribution]            )        coord_no_averages.append(np.mean(            [np.average(range(7), weights=row) for row in distribution])            )        coord_no_averages_stdev.append(            np.std([np.average(range(7), weights=row) for row in distribution])            )    return coord_no_means, coord_no_stdevs, coord_no_averages, coord_no_averages_stdevdef main():    densities, vols_per_atom = read_simple_data()    mean_energies, std_energies = read_energy()    coord_no_means, coord_no_stdevs, coord_no_averages, coord_no_averages_stdev = read_histograms()    with open(f"results_table_{pot}.dat", "w") as results:        results.write("scalefactor density vol_per_atom "                      "mean_energy std_energy "                      "mean0 mean1 mean2 mean3 mean4 mean5 mean6 "                      "std0 std1 std2 std3 std4 std5 std6 "                      "overall_mean overall_std \n")        for i in range(len(scalefactors)):            results.write("{:.4f} {:.4f} {:.4f} ".format(scalefactors[i],                                                         densities[i],                                                         vols_per_atom[i]))            results.write("{:.4f} {:.4f} ".format(mean_energies[i],                                                  std_energies[i]))            results.write("{:.4f} {:.4f} {:.4f} {:.4f} {:.4f} {:.4f} {:.4f} ".format(*coord_no_means[i]))            results.write("{:.4f} {:.4f} {:.4f} {:.4f} {:.4f} {:.4f} {:.4f} ".format(*coord_no_stdevs[i]))            results.write("{:.4f} {:.4f} \n".format(coord_no_averages[i],                                                    coord_no_averages_stdev[i]))if __name__ == "__main__":    pot = args.pot    scalefactors = [0.86,                    0.87,                    0.90,                    0.92,                    0.95,                    0.98,                    1.02,                    1.06,                    1.09,                    1.14,                    1.18,                    1.23,                    1.28,                    1.34,                    1.41,                    1.48,                    1.56,                    1.64,                    1.74,                    1.85,                    1.97]    steps = range(10000, 110000, 10000)    main()                                        