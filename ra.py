#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
range_analysis/ra.py
Analyzes the range data in a RangeNet logfile
Feb 21 2016: changed name to qualify.py, added qualify-info.csv
"""

import argparse
import sys, os
import pdb
import pickle
import pprint as pp
import numpy as np
import matplotlib.pyplot as plt
#from matplotlib.patches import patches
from matplotlib.backends.backend_pdf import PdfPages
from pprint import pprint as pp

sys.path.append('..')
import lib

parser = argparse.ArgumentParser(description='RangeNet logfile analysis')
parser.add_argument('-f','--ffn_in',help='input file')
parser.add_argument('-c','--compress',action='store_true',default=False)
myargs = parser.parse_args()

ffn_in = myargs.ffn_in
compress_flag = myargs.compress

# temporary override
ffn_in = '/Volumes/Transcend/Data/RangeNet/Lobby_DOP_Tests/Lobby_DOP4_BaldSpot_OnTheEdge_001.csv'
ffn_in = '/Volumes/Transcend/Data/RangeNet/Lobby_DOP_Tests/Lobby_DOP4_BaldSpot_OnTheEdge_001.pkl'
if not ffn_in :
    ffn_in = lib.query_file()

path,fn_in = os.path.split(ffn_in)
fn_main,fn_ext = os.path.splitext(fn_in)
fn_pkl = fn_main + '.pkl'
ffn_pkl = os.path.join(path,fn_pkl)

#pdb.set_trace()
if fn_ext == '.csv' :
    #if not os.path.isfile(ffn_pkl) or compress_flag :
    D = lib.read_log(ffn_in)
    fh_pkl = open(ffn_pkl,'wb')
    pickle.dump(D,fh_pkl)
    fh_pkl.close()
    print 'Compressed data saved to ', ffn_pkl
else :
    D = pickle.load(open(ffn_pkl,'rb'))

req_list = np.unique(D['RcmRanges']['reqID'])
rsp_list = np.unique(D['RcmRanges']['rspID'])
pii_list = np.unique(D['RcmRanges']['t_stopwatch'])

fn_pdf = fn_main + '.pdf'
ffn_pdf = os.path.join(path,fn_pdf)
pdf = PdfPages(ffn_pdf)


plt.ion()
#rsp_list = [101]
for rspID in rsp_list :

    #--- create a mask for this responder
    RA = D['RcmRanges'].ravel()
    rspID_mask = RA['rspID'] == rspID

    #--- associated Time vector
    t_vec = RA[rspID_mask]['t_host']
    t0 = RA['t_host'][0]
    t_vec = t_vec - t0

    #--- create a figure
    fig = plt.figure(figsize=(18,10))
    plt.suptitle(fn_main,fontsize=13)

    #--- isolate ranges
    r_vec = RA[rspID_mask]['rmeas']
    print
    print 'rspID ' + str(rspID)
    print 'range stats: mean=%5.3f, max=%5.3f, min=%5.3f' %(np.mean(r_vec),max(r_vec),min(r_vec))

    #---  Range Subplot
    ax1 = plt.subplot(511)
    plt.plot(t_vec,r_vec,'b.')
    plt.grid(True)
    plt.title('Responder: %d' % (rspID),fontsize=14)
    plt.ylabel('Rmeas (m)',fontsize=12)

    ax1.set_ylim([2,16])

    #--- isolate REEs
    ree_vec = RA[rspID_mask]['ree']
    print 'ree stats: mean=%5.3f, max=%5.3f, min=%5.3f' %(np.mean(ree_vec),max(ree_vec),min(ree_vec))

    #---  REE Subplot
    ax2 = plt.subplot(512)
    plt.plot(t_vec,ree_vec,'b.')
    plt.grid(True)
    plt.ylabel('REE (m)',fontsize=12)

    #--- isolate LED Flags
    ledflag_vec = RA[rspID_mask]['ledflags']
    print 'ledflag stats: mean=%5.3f, max=%5.3f, min=%5.3f' % (np.mean(ledflag_vec),max(ledflag_vec),min(ledflag_vec))

    #---  LEDFLAG Subplot
    ax3 = plt.subplot(513)
    plt.plot(t_vec,ledflag_vec,'b.')
    plt.grid(True)
    plt.ylabel('LED Flags',fontsize=12)

    #---  isolate SNR
    vpk_vec = RA[rspID_mask]['vpeak']
    noise_vec = RA[rspID_mask]['noise']
    snr_vec = 20.*np.log10(np.divide(vpk_vec,noise_vec))
    print 'snr stats: mean=%5.3f, max=%5.3f, min=%5.3f' % (np.mean(snr_vec),max(snr_vec),min(snr_vec))

    #---  SNR Subplot
    ax4 = plt.subplot(514)
    plt.plot(t_vec,snr_vec,'b.')
    plt.grid(True)
    plt.ylabel('SNR (m)',fontsize=12)

    #--- isolate delta Times
    dt_vec = np.diff(t_vec)
    print 'dt stats: mean=%5.3f, max=%5.3f, min=%5.3f' % (np.mean(dt_vec),max(dt_vec),min(dt_vec))

    #--- plot dT vs T
    ax5 = plt.subplot(515)
    plt.plot(t_vec[1:],dt_vec,'b.')
    plt.grid(True)
    plt.ylabel('dT (ms)',fontsize=12)


    #--- isolate stinkers
    ree_gt_thresh_mask = (ree_vec > 0.1)
    t_vec_ree = t_vec[ree_gt_thresh_mask]
    r_vec_ree = r_vec[ree_gt_thresh_mask]

    #---  overplot range with those with ree > thresh
    ax1.plot(t_vec_ree,r_vec_ree,'s',markeredgecolor='r',fillstyle='none')





    plt.draw()

    pdf.savefig()

pdf.close()

pdb.set_trace()
#raw_input('press any key to quit:')
