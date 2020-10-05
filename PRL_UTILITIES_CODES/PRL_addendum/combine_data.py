'''
This code:
* combines matching thnq bins from different files, i.e. pm80_set1, pm_580_set1, pm_580_set2, . . . .
* each of these has a full range of (thnq, pr) bins, howver, we want to combined all the same 
  thnq of different files onto a single file
'''

import LT.box as B
from LT.datafile import dfile
import numpy as np
import matplotlib.pyplot as plt
import numpy.ma as ma
import sys                                     
import os                                                                                                       
from sys import argv  
import matplotlib
from matplotlib import rc
from matplotlib import *

def find_common_thnq(thnq_match):

    fname = np.array(['pm80_laget_bc_corr_set1.txt', 'pm580_laget_bc_corr_set1.txt', 'pm580_laget_bc_corr_set2.txt', 'pm750_laget_bc_corr_set1.txt', 'pm750_laget_bc_corr_set2.txt', 'pm750_laget_bc_corr_set3.txt'])
    fname_out = 'theory_JML_thnq%d.txt'%(thnq_match)

    #open file to write results:
    ofile = open(fname_out, 'w')
    header = """ 
    # Jean-Marc Laget (JML) theoretical cross sections and reduced cross sections as a function of missing momentum
    #
    # theta_nq = %s (deg)
    #
    # header definitions
    #
    # pm_bin            : missig momentum bin center (GeV/c) (bin width from center is +/- 0.02 GeV)
    # pm_avg            : average missing momentum over pm_bin (GeV/c)
    # theory_pwiaXsec      : theoretical cross section using the JML Paris PWIA model ( nb / (MeV Sr^2) ) 
    # theory_fsiXsec       : theoretical cross section using the JML Paris FSI model ( nb / (MeV Sr^2) )
    # theory_red_pwiaXsec  : theoretical reduced cross section using the JML Paris PWIA model (fm^3) 
    # theory_red_fsiXsec   : theoretical reduced cross section using the JML Paris FSI model (fm^3)
    
    #! pm_bin[f,0]/ pm_avg[f,1]/ theory_pwiaXsec[f,2]/ theory_fsiXsec[f,3]/  theory_red_pwiaXsec[f,4]/ theory_red_fsiXsec[f,5]/  setting[s,6]/ 

    """
    ofile.write(header)

    # Conversion factor:  1 fm = 1/ (197 MeV),   
    # The reduced cross section is in MeV^-3 units
    MeV2fm = 197.3**3    #convert MeV^-3 to fm^3
    ub2nb = 1000.        # 1 ub == 1000 nb

    #create empty numpy arrays for storing (concatenate) arrays from each file
    pm_bin_tot = np.array([])
    pm_avg_tot = np.array([])
    JML_pwiaXsec_tot = np.array([])
    JML_fsiXsec_tot = np.array([])
    JML_red_pwiaXsec_tot = np.array([])
    JML_red_fsiXsec_tot = np.array([])
    
    #empty array to store strings
    pm_setting = []
    
    #loop over each file
    for fi in fname:
        #print(fi)

        #parse file name to extact pm_setting
        pm_str = fi.split('_')[0]
        pm_str = pm_str.strip('pm')
        set_str = fi.split('_')[-1]
        set_str = set_str.strip('.txt')
        pm_setting_str = pm_str + '_' + set_str
        #open file to read
        kin = dfile(fi) 
        #print(pm_setting)
        #open array of recoil angles: 5, 15, 25, etc. deg
        thnq = np.array(kin['xb']) 

        #read arrays and find matching thnq bins ONLY
        pm_bin = np.array( (kin['yb'])[thnq==thnq_match] )       # GeV/c
        pm_avg = np.array( (kin['pm_avg'])[thnq==thnq_match] )   # GeV/c
        JML_pwiaXsec = np.array( (kin['pwiaXsec_theory'])[thnq==thnq_match] )     # cross section: ub / (MeV * Sr^2)
        JML_fsiXsec = np.array( (kin['fsiXsec_theory'])[thnq==thnq_match] )         # cross section: ub / (MeV * Sr^2)
        JML_red_pwiaXsec = np.array( (kin['red_pwiaXsec'])[thnq==thnq_match] )     # red. Xsec (MeV^-3)
        JML_red_fsiXsec = np.array( (kin['red_fsiXsec'])[thnq==thnq_match] )       # red. Xsec (MeV^-3)

        for i in range(len(pm_bin)):
            pm_setting.append(pm_setting_str)
            
        #conatenate arrays to total array
        pm_bin_tot = np.concatenate([pm_bin_tot, pm_bin])
        pm_avg_tot = np.concatenate([pm_avg_tot, pm_avg])
        JML_pwiaXsec_tot = np.concatenate([JML_pwiaXsec_tot, JML_pwiaXsec])
        JML_fsiXsec_tot = np.concatenate([JML_fsiXsec_tot, JML_fsiXsec])
        JML_red_pwiaXsec_tot = np.concatenate([JML_red_pwiaXsec_tot, JML_red_pwiaXsec])
        JML_red_fsiXsec_tot = np.concatenate([JML_red_fsiXsec_tot, JML_red_fsiXsec])
        
    #sort the concatenated arrays in order of pm_bins
    pm_bin_tot, pm_avg_tot, JML_pwiaXsec_tot, JML_fsiXsec_tot, JML_red_pwiaXsec_tot, JML_red_fsiXsec_tot, pm_setting = zip(*sorted(zip(pm_bin_tot, pm_avg_tot, JML_pwiaXsec_tot, JML_fsiXsec_tot, JML_red_pwiaXsec_tot, JML_red_fsiXsec_tot, pm_setting  )))
    
    for i, ival in enumerate(pm_bin_tot):
        if(JML_pwiaXsec_tot[i]==-1. or JML_fsiXsec_tot[i]==-1.):
            continue
        else:
            ofile.write("%.5f  %.5f  %.5E  %.5E  %.5E  %.5E %s\n" % (pm_bin_tot[i], pm_avg_tot[i], JML_pwiaXsec_tot[i]*ub2nb, JML_fsiXsec_tot[i]*ub2nb, JML_red_pwiaXsec_tot[i]*MeV2fm, JML_red_fsiXsec_tot[i]*MeV2fm, pm_setting[i] ))
        

def main():
   
    find_common_thnq(35)
    find_common_thnq(45)
    find_common_thnq(75)

if __name__ == "__main__":
    main()

    
        #for i, ival in enumerate(JML_pwiaXsec):
        #    if(JML_pwiaXsec[i]==-1. or JML_pwiaXsec[i]==-1.):
        #        continue
        #    else:
        #        print(i, pm_bin[i], pm_avg[i], JML_pwiaXsec[i], JML_fsiXsec[i])
