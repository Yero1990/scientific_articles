import LT.box as B
from LT.datafile import dfile
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import numpy.ma as ma
import sys                                     
import os                                                                                                       
from sys import argv  
import matplotlib
from matplotlib import rc
from matplotlib import *
from mpl_toolkits.axes_grid.inset_locator import (inset_axes, InsetPosition, mark_inset)


#Use latex commands (e.g. \textit ot \textbf)
rc('text', usetex=True)
matplotlib.rcParams['text.latex.preamble']=[r"\usepackage{amsmath}"]

#Set default font to times new roman
font = {'family' : 'Times New Roman',
        'weight' : 'bold',  #'normal', 'bold'
        'size'   : 12
}

plt.rc('font', **font)

#Set font
csfont = {'fontname':'Times New Roman'}

def convert2NaN(arr=np.array([]), value=0):
    #method to convert a specified value in a array to nan (not a number)
    
    for i in enumerate(arr):
        if arr[i[0]]==value:
            arr[i[0]] = np.nan
    return arr


#Conversion factor:  1 fm = 1/ (197 MeV),   
#The reduced cross section is in MeV^-3 units
MeV2fm = 197.3**3    #convert MeV^-3 to fm^3

#User Input (Dir. Name to store output)
sys_ext = sys.argv[1]     #Em_final40MeV, all_thnq_Q2_3to4GeV
    
dir_name = sys_ext+"_plots"
dir_name_misc = dir_name + "/misc_plots"        #directory to store miscellaneous plots (trigger rates, live time, etc. . .) #obtained from the report files
#print(dir_name)
#check if directory exists, else creates it.
#if not os.path.exists(dir_name):
#    os.makedirs(dir_name)
#if not os.path.exists(dir_name_misc):
#    os.makedirs(dir_name_misc)
     
def plot_report():

    #-------Plot the report file quantities: trigger rates, efficiencies (detector, live time, etc.), 


    def get_fname(pm_set, data_set):
        fname='../../root_files/pm%i_fsiXsec_set%i_%s/report_deep_pm%i_set%i.dat'%(pm_set, data_set, sys_ext, pm_set, data_set)
        return fname

    def get_var(pm_set=0, data_set=0, var=''):
        fvar = np.array(dfile(get_fname(pm_set,data_set))[var])
        return fvar
         
    def get_heep_var(var=''):
        fname='../../root_files/pre_HEEP_ELASTICS/report_heep.dat'
        fvar = np.array(dfile(fname)[var])
        return fvar

    
    #---------------Plot Accepted COin. Triggers Counts per charge---------------
    CPQ80_set1 = get_var(80,1,'ptrig6_accp')/get_var(80,1,'charge') ; CPQ80_set1_err = get_var(80,1,'ptrig6_accp')/get_var(80,1,'charge')**2 * (0.02*get_var(80,1,'charge'))
    CPQ580_set1 = get_var(580,1,'ptrig6_accp')/get_var(580,1,'charge') ; CPQ580_set1_err = get_var(580,1,'ptrig6_accp')/get_var(580,1,'charge')**2 * (0.02*get_var(580,1,'charge'))
    CPQ580_set2 = get_var(580,2,'ptrig6_accp')/get_var(580,2,'charge') ; CPQ580_set2_err = get_var(580,2,'ptrig6_accp')/get_var(580,2,'charge')**2 * (0.02*get_var(580,2,'charge'))
    CPQ750_set1 = get_var(750,1,'ptrig6_accp')/get_var(750,1,'charge') ; CPQ750_set1_err = get_var(750,1,'ptrig6_accp')/get_var(750,1,'charge')**2 * (0.02*get_var(750,1,'charge'))
    CPQ750_set2 = get_var(750,2,'ptrig6_accp')/get_var(750,2,'charge') ; CPQ750_set2_err = get_var(750,2,'ptrig6_accp')/get_var(750,2,'charge')**2 * (0.02*get_var(750,2,'charge'))
    CPQ750_set3 = get_var(750,3,'ptrig6_accp')/get_var(750,3,'charge') ; CPQ750_set3_err = get_var(750,3,'ptrig6_accp')/get_var(750,3,'charge')**2 * (0.02*get_var(750,3,'charge'))

    B.plot_exp(get_var(80,1,'Run'),   CPQ80_set1*0.06,   CPQ80_set1_err*0.06,  marker='^', color='k', label='80 (set1), scaled x $1/0.06$' )
    B.plot_exp(get_var(580,1,'Run'),  CPQ580_set1,  CPQ580_set1_err, marker='^', color='b', label='580 (set1)' )
    B.plot_exp(get_var(580,2,'Run'),  CPQ580_set2,  CPQ580_set2_err, marker='^', color='g', label='580 (set2)' )
    B.plot_exp(get_var(750,1,'Run'),  CPQ750_set1,  CPQ750_set1_err, marker='^', color='r', label='750 (set1)' )
    B.plot_exp(get_var(750,2,'Run'),  CPQ750_set2,  CPQ750_set2_err, marker='^', color='m', label='750 (set2)' )
    B.plot_exp(get_var(750,3,'Run'),  CPQ750_set3,  CPQ750_set3_err, marker='^', color='c', label='750 (set3)' )

    B.pl.xlabel('Run Number')
    B.pl.ylabel('Accepted Coin. Triggers / mC')
    B.pl.title('Accepted Coincidence Triggers  vs. Run Number')
    B.pl.grid(True)
    B.pl.legend(loc='upper right')
    B.pl.show()
    #B.pl.savefig(dir_name_misc+'/counts_per_charge.pdf')
    #-------------------------------------------------------
    
    #---------------Plot Run vs Total Live Time---------------
    LT80 = np.array(get_var(80,1,'tLT'))
    LT580_s1 = np.array(get_var(580,1,'tLT'))
    LT580_s2 = np.array(get_var(580,2,'tLT'))
    LT750_s1 = np.array(get_var(750,1,'tLT'))
    LT750_s2 = np.array(get_var(750,2,'tLT'))
    LT750_s3 = np.array(get_var(750,3,'tLT'))
    
    LT_final = np.concatenate((LT80, LT580_s1, LT580_s2, LT750_s1, LT750_s2, LT750_s3), axis=0)
    LT_avg = np.average(LT_final)

    B.pl.hlines(LT_avg, 3288, 3410, linestyles='--', zorder=2)

    B.plot_exp(get_var(80,1,'Run'),  get_var(80,1,'tLT'), get_var(80,1,'tLT')*0.03,  marker='s', color='k', label='80 (set1)', zorder=1)
    B.plot_exp(get_var(580,1,'Run'),  get_var(580,1,'tLT'), get_var(580,1,'tLT')*0.03,  marker='s', color='b', label='580 (set1)', zorder=1)
    B.plot_exp(get_var(580,2,'Run'),  get_var(580,2,'tLT'), get_var(580,2,'tLT')*0.03,  marker='s', color='g', label='580 (set2)', zorder=1 )
  
    B.plot_exp(get_var(750,1,'Run'),  get_var(750,1,'tLT'), get_var(750,1,'tLT')*0.03,  marker='s', color='r', label='750 (set1)', zorder=1 )
    B.plot_exp(get_var(750,2,'Run'),  get_var(750,2,'tLT'), get_var(750,2,'tLT')*0.03,  marker='s', color='m', label='750 (set2)', zorder=1)
    B.plot_exp(get_var(750,3,'Run'),  get_var(750,3,'tLT'), get_var(750,3,'tLT')*0.03,  marker='s', color='c', label='750 (set3)', zorder=1)
    
    B.pl.xlim(3288, 3410)
    B.pl.ylim(0.85, 1.1)
    B.pl.xlabel('Run Number')
    B.pl.ylabel('Total Live Time')
    B.pl.text(3290, 1.02, 'Average Live Time: %.3f'%(LT_avg))
    B.pl.grid(True)

    B.pl.title('Total EDTM Live Time vs. Run Number')

    
    B.pl.legend(loc='upper right')
    B.pl.show()
    #B.pl.savefig(dir_name_misc+'/total_livetime.pdf')

    #-------------------------------------------------------
    
    
    #---------------Plot Run vs Tracking Efficiencies---------------
    htrk80 = np.array(get_var(80,1,'hTrkEff'));         etrk80 = np.array(get_var(80,1,'eTrkEff'))
    htrk580_s1 = np.array(get_var(580,1,'hTrkEff'));    etrk580_s1 = np.array(get_var(580,1,'eTrkEff'))
    htrk580_s2 = np.array(get_var(580,2,'hTrkEff'));    etrk580_s2 = np.array(get_var(580,2,'eTrkEff'))
    htrk750_s1 = np.array(get_var(750,1,'hTrkEff'));    etrk750_s1 = np.array(get_var(750,1,'eTrkEff'))
    htrk750_s2 = np.array(get_var(750,2,'hTrkEff'));    etrk750_s2 = np.array(get_var(750,2,'eTrkEff'))
    htrk750_s3 = np.array(get_var(750,3,'hTrkEff'));    etrk750_s3 = np.array(get_var(750,3,'eTrkEff'))
    
    htrk_final = np.concatenate((htrk80, htrk580_s1, htrk580_s2, htrk750_s1, htrk750_s2, htrk750_s3), axis=0)
    etrk_final = np.concatenate((etrk80, etrk580_s1, etrk580_s2, etrk750_s1, etrk750_s2, etrk750_s3), axis=0)

    htrk_avg = np.average(htrk_final)
    etrk_avg = np.average(etrk_final)

    B.pl.hlines(htrk_avg, 3288, 3410, linestyles='--', zorder=2)

    B.plot_exp(get_var(80,1,'Run'),  get_var(80,1,'hTrkEff'), get_var(80,1,'hTrkEff_err'),  marker='s', color='k', label='80 (set1)' , zorder=1)
    B.plot_exp(get_var(580,1,'Run'),  get_var(580,1,'hTrkEff'), get_var(580,1,'hTrkEff_err'),  marker='s', color='b', label='580 (set1)' , zorder=1)
    B.plot_exp(get_var(580,2,'Run'),  get_var(580,2,'hTrkEff'), get_var(580,2,'hTrkEff_err'),  marker='s', color='g', label='580 (set2)' , zorder=1)
    B.plot_exp(get_var(750,1,'Run'),  get_var(750,1,'hTrkEff'), get_var(750,1,'hTrkEff_err'),  marker='s', color='r', label='750 (set1)' , zorder=1)
    B.plot_exp(get_var(750,2,'Run'),  get_var(750,2,'hTrkEff'), get_var(750,2,'hTrkEff_err'),  marker='s', color='m', label='750 (set2)' , zorder=1)
    B.plot_exp(get_var(750,3,'Run'),  get_var(750,3,'hTrkEff'), get_var(750,3,'hTrkEff_err'),  marker='s', color='c', label='750 (set3)' , zorder=1)

    B.pl.hlines(etrk_avg, 3288, 3410, linestyles='--', zorder=2)

    B.plot_exp(get_var(80,1,'Run'),  get_var(80,1,'eTrkEff'), get_var(80,1,'eTrkEff_err'),  marker='s', mec='k', mfc='white', ecolor='k', label='' , zorder=1)
    B.plot_exp(get_var(580,1,'Run'),  get_var(580,1,'eTrkEff'), get_var(580,1,'eTrkEff_err'),  marker='s', mec='b', mfc='white', ecolor='b', label='' , zorder=1)
    B.plot_exp(get_var(580,2,'Run'),  get_var(580,2,'eTrkEff'), get_var(580,2,'eTrkEff_err'),  marker='s', mec='g', mfc='white', ecolor='g', label='' , zorder=1)
    B.plot_exp(get_var(750,1,'Run'),  get_var(750,1,'eTrkEff'), get_var(750,1,'eTrkEff_err'),  marker='s', mec='r', mfc='white', ecolor='r', label='' , zorder=1)
    B.plot_exp(get_var(750,2,'Run'),  get_var(750,2,'eTrkEff'), get_var(750,2,'eTrkEff_err'),  marker='s', mec='m', mfc='white', ecolor='m', label='' , zorder=1)
    B.plot_exp(get_var(750,3,'Run'),  get_var(750,3,'eTrkEff'), get_var(750,3,'eTrkEff_err'),  marker='s', mec='c', mfc='white', ecolor='c', label='' , zorder=1)
    
    B.pl.xlabel('Run Number')
    B.pl.ylabel('Tracking Efficiency')
    B.pl.text(3310, 1.02, 'HMS TrkEff Average: %.3f'%(htrk_avg))
    B.pl.text(3310, 0.93, 'SHMS TrkEff Average: %.3f'%(etrk_avg))

    B.pl.title('Tracking Efficiency vs. Run Number')
    B.pl.ylim(0.92, 1.08)
    B.pl.xlim(3285, 3400)
    B.pl.grid(True)

    B.pl.legend(ncol=2, loc='upper right')
    B.pl.show()
    #B.pl.savefig(dir_name_misc+'/tracking_eff.pdf')

    
    #---------------Plot Run vs Target Boiling Factor---------------
    #tgt_Boil = 1 - m*I  ; apply errror propagation
    m =  0.00080029      #LD2 slope
    sig_m = 0.00007037   
    dI_I = 2.0/100.      #relative error in current (assume 2%)
    sig_I_80 = dI_I * get_var(80,1,'avg_current') 
    sig_I_580set1 = dI_I * get_var(580,1,'avg_current') ;  sig_I_580set2 = dI_I * get_var(580,2,'avg_current')
    sig_I_750set1 = dI_I * get_var(750,1,'avg_current') ;  sig_I_750set2 = dI_I * get_var(750,2,'avg_current') ;  sig_I_750set3 = dI_I * get_var(750,3,'avg_current')

    tb_80_err = np.sqrt(  get_var(80,1,'avg_current')**2 * sig_m**2 + m**2 * sig_I_80**2  ) 
    tb_580set1_err = np.sqrt(  get_var(580,1,'avg_current')**2 * sig_m**2 + m**2 * sig_I_580set1**2  ) 
    tb_580set2_err = np.sqrt(  get_var(580,2,'avg_current')**2 * sig_m**2 + m**2 * sig_I_580set2**2  ) 
    tb_750set1_err = np.sqrt(  get_var(750,1,'avg_current')**2 * sig_m**2 + m**2 * sig_I_750set1**2  ) 
    tb_750set2_err = np.sqrt(  get_var(750,2,'avg_current')**2 * sig_m**2 + m**2 * sig_I_750set2**2  ) 
    tb_750set3_err = np.sqrt(  get_var(750,3,'avg_current')**2 * sig_m**2 + m**2 * sig_I_750set3**2  ) 

    tb_80s1 = get_var(80,1,'tgtBoil_factor')
    tb_580s1 = get_var(580,1,'tgtBoil_factor')
    tb_580s2 = get_var(580,2,'tgtBoil_factor')
    tb_750s1 = get_var(750,1,'tgtBoil_factor')
    tb_750s2 = get_var(750,2,'tgtBoil_factor')
    tb_750s3 = get_var(750,3,'tgtBoil_factor')
    tb_final = np.concatenate((tb_80s1, tb_580s1, tb_580s2, tb_750s1, tb_750s2, tb_750s3), axis=0)
    tb_avg = np.average(tb_final)
    B.pl.hlines(tb_avg, 3288, 3410, linestyles='--', zorder=2)

    B.plot_exp(get_var(80,1,'Run'),  get_var(80,1,'tgtBoil_factor'), tb_80_err,  marker='s', ecolor = 'k', mec='k', mfc='white', label='80 (set1)', zorder=1 )
    B.plot_exp(get_var(580,1,'Run'),  get_var(580,1,'tgtBoil_factor'), tb_580set1_err,  marker='s',  ecolor = 'b', mec='b', mfc='white',label='580 (set1)' , zorder=1)
    B.plot_exp(get_var(580,2,'Run'),  get_var(580,2,'tgtBoil_factor'), tb_580set2_err,  marker='s',  ecolor = 'g', mec='g', mfc='white',label='580 (set2)' , zorder=1)
  
    B.plot_exp(get_var(750,1,'Run'),  get_var(750,1,'tgtBoil_factor'), tb_750set1_err,  marker='s',  ecolor = 'r', mec='r', mfc='white',label='750 (set1)' , zorder=1)
    B.plot_exp(get_var(750,2,'Run'),  get_var(750,2,'tgtBoil_factor'), tb_750set2_err,  marker='s',  ecolor = 'm', mec='m', mfc='white',label='750 (set2)' , zorder=1)
    B.plot_exp(get_var(750,3,'Run'),  get_var(750,3,'tgtBoil_factor'), tb_750set3_err,  marker='s',  ecolor = 'c', mec='c', mfc='white',label='750 (set3)' , zorder=1)

    B.pl.xlabel('Run Number')
    B.pl.ylabel('Target Boiling Factor')
    B.pl.text(3290, 1.0, 'Average Boiling Factor: %.3f'%(tb_avg))

    B.pl.title(r'LD$_{2}$ Boiling Factor vs. Run Number')
    B.pl.ylim(0.9, 1.05)
    B.pl.xlim(3285, 3400)
    B.pl.grid(True)

    B.pl.legend(loc='upper right')
    B.pl.show()
    #B.pl.savefig(dir_name_misc+'/target_boil.pdf')

    #---------------------------------------------------------------
    
    
    #---------------Plot Run vs Average Beam Current---------------
    B.plot_exp(get_var(80,1,'Run'),  get_var(80,1,'avg_current'), get_var(80,1,'avg_current')*0.02,  marker='s', color='k', label='80 (set1)' )
    B.plot_exp(get_var(580,1,'Run'),  get_var(580,1,'avg_current'), get_var(580,1,'avg_current')*0.02,  marker='s', color='b', label='580 (set1)' )
    B.plot_exp(get_var(580,2,'Run'),  get_var(580,2,'avg_current'), get_var(580,2,'avg_current')*0.02,  marker='s', color='g', label='580 (set2)' )
  
    B.plot_exp(get_var(750,1,'Run'),  get_var(750,1,'avg_current'), get_var(750,1,'avg_current')*0.02,  marker='s', color='r', label='750 (set1)' )
    B.plot_exp(get_var(750,2,'Run'),  get_var(750,2,'avg_current'), get_var(750,2,'avg_current')*0.02,  marker='s', color='m', label='750 (set2)' )
    B.plot_exp(get_var(750,3,'Run'),  get_var(750,3,'avg_current'), get_var(750,3,'avg_current')*0.02,  marker='s', color='c', label='750 (set3)' )

    B.pl.xlabel('Run Number')
    B.pl.ylabel(r'Average Beam Current [$\mu$A]')
    B.pl.title('Average Beam Current vs. Run Number')
    B.pl.ylim(40, 75)
    B.pl.xlim(3285, 3400)
    B.pl.grid(True)

    B.pl.legend(loc='upper right')
    B.pl.show()
    #B.pl.savefig(dir_name_misc+'/beam_current.pdf')

    #-------------------------------------------------------
    

    
    #---------------Plot Run vs Trigger Rates---------------   
    B.pl.subplot(311)
    B.plot_exp(get_var(80,1,'Run'),  get_var(80,1,'ptrig1_rate'),   marker='s', color='k', label='80 (set1)' )
    B.plot_exp(get_var(580,1,'Run'),  get_var(580,1,'ptrig1_rate'),   marker='s', color='b', label='580 (set1)' )
    B.plot_exp(get_var(580,2,'Run'),  get_var(580,2,'ptrig1_rate'),  marker='s', color='g', label='580 (set2)' )
    B.plot_exp(get_var(750,1,'Run'),  get_var(750,1,'ptrig1_rate'),   marker='s', color='r', label='750 (set1)' )
    B.plot_exp(get_var(750,2,'Run'),  get_var(750,2,'ptrig1_rate'),  marker='s', color='m', label='750 (set2)' )
    B.plot_exp(get_var(750,3,'Run'),  get_var(750,3,'ptrig1_rate'),   marker='s', color='c', label='750 (set3)' )
    B.pl.title('Trigger Rates vs. Run Number')
    B.pl.ylabel(r'SHMS Rate [kHz]')
    B.pl.xlim(3285, 3410)
    B.pl.grid(True)

    B.pl.legend(loc='upper right')

    #---------------------------
    B.pl.subplot(312)
    B.plot_exp(get_var(80,1,'Run'),  get_var(80,1,'ptrig4_rate')*0.2,   marker='s', color='k')
    B.plot_exp(get_var(580,1,'Run'),  get_var(580,1,'ptrig4_rate'),   marker='s', color='b')
    B.plot_exp(get_var(580,2,'Run'),  get_var(580,2,'ptrig4_rate'),  marker='s', color='g')
    B.plot_exp(get_var(750,1,'Run'),  get_var(750,1,'ptrig4_rate'),   marker='s', color='r')
    B.plot_exp(get_var(750,2,'Run'),  get_var(750,2,'ptrig4_rate'),  marker='s', color='m')
    B.plot_exp(get_var(750,3,'Run'),  get_var(750,3,'ptrig4_rate'),   marker='s', color='c')
    B.pl.ylabel(r'HMS Rate [kHz]')
    B.pl.text(3390, 0.15, '$P_{m}=80$ MeV/c \n (scaled x $1/0.2$)')
    B.pl.title('')
    B.pl.xlim(3285, 3410)
    B.pl.grid(True)

    #---------------------------
    B.pl.subplot(313)
    B.plot_exp(get_var(80,1,'Run'),  get_var(80,1,'ptrig6_rate')*1000*0.02,   marker='s', color='k')
    B.plot_exp(get_var(580,1,'Run'),  get_var(580,1,'ptrig6_rate')*1000,   marker='s', color='b')
    B.plot_exp(get_var(580,2,'Run'),  get_var(580,2,'ptrig6_rate')*1000,  marker='s', color='g')
    B.plot_exp(get_var(750,1,'Run'),  get_var(750,1,'ptrig6_rate')*1000,   marker='s', color='r')
    B.plot_exp(get_var(750,2,'Run'),  get_var(750,2,'ptrig6_rate')*1000,  marker='s', color='m')
    B.plot_exp(get_var(750,3,'Run'),  get_var(750,3,'ptrig6_rate')*1000,   marker='s', color='c')
    B.pl.ylabel(r'Coin. Rate [Hz]')
    B.pl.text(3390, 2.6, '$P_{m}=80$ MeV/c \n (scaled x $1/0.02$)')
    B.pl.title('')
    B.pl.grid(True)

    B.pl.subplots_adjust(hspace=.001)
    B.pl.xlabel('Run Number')
    #B.pl.ylabel(r'Trigger Rate [kHz]')
    B.pl.xlim(3285, 3410)
    B.pl.show()
    #B.pl.savefig(dir_name_misc+'/trigger_rates.pdf')

    #-------------------------------------------------------

    
    
    #---------------Plot Run vs BPM position---------------
    xbpm_80s1 = get_var(80,1,'xBPM')   ;  ybpm_80s1 = get_var(80,1,'yBPM')
    xbpm_580s1 = get_var(580,1,'xBPM') ;  ybpm_580s1 = get_var(580,1,'yBPM')
    xbpm_580s2 = get_var(580,2,'xBPM') ;  ybpm_580s2 = get_var(580,2,'yBPM')
    xbpm_750s1 = get_var(750,1,'xBPM') ;  ybpm_750s1 = get_var(750,1,'yBPM')
    xbpm_750s2 = get_var(750,2,'xBPM') ;  ybpm_750s2 = get_var(750,2,'yBPM')
    xbpm_750s3 = get_var(750,3,'xBPM') ;  ybpm_750s3 = get_var(750,3,'yBPM')

    xbpm_final = np.concatenate((xbpm_80s1,xbpm_580s1,xbpm_580s2,xbpm_750s1,xbpm_750s2,xbpm_750s3), axis=0)
    ybpm_final = np.concatenate((ybpm_80s1,ybpm_580s1,ybpm_580s2,ybpm_750s1,ybpm_750s2,ybpm_750s3), axis=0)

    xbpm_avg = np.average(xbpm_final)
    ybpm_avg = np.average(ybpm_final)

    B.pl.hlines(xbpm_avg, 3288, 3410, linestyles='--', zorder=2)

    #Assume relative uncertainty of 0.1 mm (0.01 cm) (from D. Gaskell) for now
    bpm_err = 0.01 #in cm,  df/f
    B.plot_exp(get_heep_var('Run'),  get_heep_var('xBPM'), get_heep_var('xBPM')*bpm_err, marker='D', color='gray', label='H(e,e\'p)' , zorder=1)

    B.plot_exp(get_var(80,1,'Run'),  get_var(80,1,'xBPM'),  get_var(80,1,'xBPM')*bpm_err, marker='s', color='k', label='80 (set1)' )
    B.plot_exp(get_var(580,1,'Run'),  get_var(580,1,'xBPM'),get_var(580,1,'xBPM')*bpm_err,  marker='s', color='b', label='580 (set1)' , zorder=1)
    B.plot_exp(get_var(580,2,'Run'),  get_var(580,2,'xBPM'),get_var(580,2,'xBPM')*bpm_err,  marker='s', color='g', label='580 (set2)' , zorder=1)
  
    B.plot_exp(get_var(750,1,'Run'),  get_var(750,1,'xBPM'), get_var(750,1,'xBPM')*bpm_err, marker='s', color='r', label='750 (set1)' , zorder=1)
    B.plot_exp(get_var(750,2,'Run'),  get_var(750,2,'xBPM'), get_var(750,2,'xBPM')*bpm_err, marker='s', color='m', label='750 (set2)' , zorder=1)
    B.plot_exp(get_var(750,3,'Run'),  get_var(750,3,'xBPM'), get_var(750,3,'xBPM')*bpm_err, marker='s', color='c', label='750 (set3)' , zorder=1)
    #-------------
    B.pl.hlines(ybpm_avg, 3288, 3410, linestyles='--', label='', zorder=2)

    B.plot_exp(get_heep_var('Run'),  get_heep_var('yBPM'), get_heep_var('yBPM')*bpm_err, marker='D', color='gray', mfc='white', zorder=1)

    B.plot_exp(get_var(80,1,'Run'),  get_var(80,1,'yBPM'),  get_var(80,1,'yBPM')*bpm_err, marker='s', color='k', mfc='white')
    B.plot_exp(get_var(580,1,'Run'),  get_var(580,1,'yBPM'),get_var(580,1,'yBPM')*bpm_err,  marker='s', color='b',  mfc='white', zorder=1)
    B.plot_exp(get_var(580,2,'Run'),  get_var(580,2,'yBPM'),get_var(580,2,'yBPM')*bpm_err,  marker='s', color='g', mfc='white', zorder=1)
  
    B.plot_exp(get_var(750,1,'Run'),  get_var(750,1,'yBPM'),get_var(750,1,'yBPM')*bpm_err,  marker='s', color='r',  mfc='white', zorder=1)
    B.plot_exp(get_var(750,2,'Run'),  get_var(750,2,'yBPM'),get_var(750,2,'yBPM')*bpm_err,  marker='s', color='m',  mfc='white', zorder=1)
    B.plot_exp(get_var(750,3,'Run'),  get_var(750,3,'yBPM'),get_var(750,3,'yBPM')*bpm_err,  marker='s', color='c',  mfc='white', zorder=1)


    B.pl.xlabel('Run Number')
    B.pl.ylabel(r'BPM Position [cm]')
    B.pl.title('Beam Position Monitor vs. Run Number')
    B.pl.text(3290, 0.0325, r'X BPM Average: %.3f cm'%(xbpm_avg))
    B.pl.text(3290, 0.022, r'Y BPM Average: %.3f cm'%(ybpm_avg))
    B.pl.xlim(3285, 3410)
    B.pl.ylim(0.0125, 0.0375)
    B.pl.grid(True)

    B.pl.legend()
    B.pl.show()
    #B.pl.savefig(dir_name_misc+'/beam_position.pdf')
    
    #------------------------------------------------------------

def main():
    print('Entering Main . . .')

    plot_report()

if __name__=="__main__":
    main()


