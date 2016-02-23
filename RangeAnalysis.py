#!/usr/local/bin/python
import os
import cPickle as pickle
import pdb
import numpy as np

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
# import sys
#
# sys.path.append('/Volumes/Transcend/Projects')
# from Tools.tictoc import tic, toc
# from numpy import inf,nan
# if os.name == 'posix' :
#     import matplotlib
#     matplotlib.use('TkAgg')
# import Tkinter#, tkFileDialog
#import time
#from collections import namedtuple
#from pprint import pprint

path_in = '/Volumes/Transcend/Data/NavNet'
fn_in = 'Lobby_RR_Flip_001'

path_in = '/Volumes/Transcend/Data/NavNet/Lobby_DOP_Tests/'
fn_in = 'Lobby_DOP4_BaldSpot_OnTheEdge_001.csv'


ffn_in = os.path.join( path_in, fn_in+'.csv' )
#ffn_in = []

PICKLE_THE_LOGFILE = True
if PICKLE_THE_LOGFILE :
    import ReadLog
    ffn_pkl = ReadLog.main(ffn_in)
else :
    ffn_pkl = os.path.join( path_in, fn_in+'.pkl' )

rangeDict = pickle.load(open(ffn_pkl,'rb'))

def plot_stuff1(rangeDict) :
    #AnalyzeRanges()
    linkList = rangeDict.keys()
    for iLink in range(len(linkList)) :
        LUT = linkList[iLink]
        rangeArray = rangeDict[LUT]
        tvec = rangeArray['tstamp'] - rangeArray['tstamp'][0]
        rvec = rangeArray['rmeas']
        reevec = rangeArray['ree']
        flagvec = [int(value[0],0) for value in rangeArray['ledflags']]
        satvec = [1 & value for value in flagvec]
        losvec = [(8 & value) >> 3 for value in flagvec]
        unknown = [(40 & value) >> 5 for value in flagvec]

#        pdb.set_trace()

        nRanges = len(rvec)
        t_duration = tvec[-1]-tvec[0]
        dt_mean = t_duration/nRanges
        r_mean = np.mean(rvec)
        r_std = np.std(rvec)
        r_max = np.max(rvec)
        r_min = np.min(rvec)
        i_min = np.argmin(rvec)
        print LUT
        print '  Total number of ranges: %d' % nRanges
        print '  Mean time between ranges: %5.3f s' % dt_mean
        print '  Mean distance: %5.3f std: %5.3f max: %5.3f, min: %5.3f' % (r_mean,r_std,r_max,r_min)
        print '  Minimum distance at index %d' % i_min

        plt.ion()
        figh = plt.figure(iLink)
        # plt.get_current_fig_manager().window.wm_geometry("+600+400")
        # pdb.set_trace()

        ax0 = figh.add_subplot(311)
        ax0.plot(tvec,rvec,'b.-')#,markersize=1,markerfacecolor='r')
        ax0.set_title(linkList[iLink])
        ax0.grid('on')
        plt.ylabel('Range (m)')
        plt.suptitle(fn_in)

        ax1 = figh.add_subplot(312)
        ax1.plot(tvec,reevec,'g.-')#,markersize=1,markerfacecolor='g')
        ax1.grid('on')
        plt.ylabel('Range Error Est (m)')

        ax2 = figh.add_subplot(313)
        ax2.plot(tvec,satvec,'o-',color='b',markerfacecolor='none')
        ax2.plot(tvec,losvec,'.-',color='g')
        ax2.set_ylim((-0.5,1.5))
        ax2.grid('on')
        plt.ylabel('LED Flags')
        ax2.legend(['SAT','LOS'])

    plt.draw()

def plot_2x3(rangeDict,fn) :

    plt.ion()
    fig = plt.figure(figsize=(18,10))

    linkList = rangeDict.keys()

    # Plot a Link Under Test
    iLUT = 0
    LUT = linkList[iLUT]
    rangeArray = rangeDict[LUT]
    tvec = rangeArray['tstamp'] - rangeArray['tstamp'][0]
    rvec = rangeArray['rmeas']
    reevec = rangeArray['ree']
    flagvec = [int(value[0],0) for value in rangeArray['ledflags']]
    satvec = [1 & value for value in flagvec]
    losvec = [(8 & value) >> 3 for value in flagvec]
    unknown = [(40 & value) >> 5 for value in flagvec]

    gs = range(6)

    gs[iLUT] = GridSpec(3,1)
    gs[0].update(left=.04,right=.35,bottom=0.55,top=0.92,wspace=0.05,hspace=0.05)

    ax0 = plt.subplot(gs[iLUT][0])
    ax0.set_title(linkList[iLUT])
    ax0.plot(tvec,rvec,'b.-')#,markersize=1,markerfacecolor='r')
    ax0.grid('on')
    ax0.set_xticks([]);
    plt.xlim([min(tvec),max(tvec)])

    ax1 = plt.subplot(gs[iLUT][1])
    ax1.plot(tvec,reevec,'g.-')#,markersize=1,markerfacecolor='g')
    ax1.grid('on')
    ax1.set_xticks([]);
    plt.xlim([min(tvec),max(tvec)])

    ax2 = plt.subplot(gs[iLUT][2])
    ax2.plot(tvec,satvec,'o-',color='c',markeredgecolor='c',markerfacecolor='none')
    losvec = np.array(losvec)+0.1
    ax2.plot(tvec,losvec,'.-',color='m')
    #    ax2.set_ylim((-0.5,1.5))
    ax2.grid('on')
    ax2.set_yticks([])
    plt.xlim([min(tvec),max(tvec)])
    ax2.legend(['SAT','LOS'],loc=5,prop={'size':8})

    #    plt.draw()

    ############# Plot another Link Under Test
    iLUT = 1
    LUT = linkList[iLUT]
    rangeArray = rangeDict[LUT]
    tvec = rangeArray['tstamp'] - rangeArray['tstamp'][0]
    rvec = rangeArray['rmeas']
    reevec = rangeArray['ree']
    flagvec = [int(value[0],0) for value in rangeArray['ledflags']]
    satvec = [1 & value for value in flagvec]
    losvec = [(8 & value) >> 3 for value in flagvec]
    unknown = [(40 & value) >> 5 for value in flagvec]

    gs[iLUT] = GridSpec(3,1)
    gs[1].update(left=.36,right=.67,bottom=0.55,top=0.92,wspace=0.05,hspace=0.05)

    ax0 = plt.subplot(gs[iLUT][0])
    ax0.set_title(linkList[iLUT])
    ax0.plot(tvec,rvec,'b.-')#,markersize=1,markerfacecolor='r')
    ax0.grid('on')
    ax0.set_xticks([]);
    plt.xlim([min(tvec),max(tvec)])
    #    ax0.set_yticks([])
    #    plt.ylabel('range (m)')

    ax1 = plt.subplot(gs[iLUT][1])
    ax1.plot(tvec,reevec,'g.-')#,markersize=1,markerfacecolor='g')
    ax1.grid('on')
    ax1.set_xticks([]);
    plt.xlim([min(tvec),max(tvec)])
    #     plt.ylabel('ree (m)')
    plt.suptitle(fn)

    ax2 = plt.subplot(gs[iLUT][2])
    ax2.plot(tvec,satvec,'o-',color='c',markeredgecolor='c',markerfacecolor='none')
    losvec = np.array(losvec)+0.1
    ax2.plot(tvec,losvec,'.-',color='m')
    ax2.grid('on')
    ax2.set_yticks([])
    plt.xlim([min(tvec),max(tvec)])
    ax2.legend(['SAT','LOS'],loc=5,prop={'size':8})


    ############# Plot another Link Under Test
    iLUT = 2
    LUT = linkList[iLUT]
    rangeArray = rangeDict[LUT]
    tvec = rangeArray['tstamp'] - rangeArray['tstamp'][0]
    rvec = rangeArray['rmeas']
    reevec = rangeArray['ree']
    flagvec = [int(value[0],0) for value in rangeArray['ledflags']]
    satvec = [1 & value for value in flagvec]
    losvec = [(8 & value) >> 3 for value in flagvec]
    unknown = [(40 & value) >> 5 for value in flagvec]

    gs[iLUT] = GridSpec(3,1)
    gs[2].update(left=.68,right=.99,bottom=0.55,top=0.92,wspace=0.05,hspace=0.05)

    ax0 = plt.subplot(gs[iLUT][0])
    ax0.set_title(linkList[iLUT])
    ax0.plot(tvec,rvec,'b.-')#,markersize=1,markerfacecolor='r')
    ax0.grid('on')
    ax0.set_xticks([]);
    plt.xlim([min(tvec),max(tvec)])
    #    ax0.set_yticks([])
    #    plt.ylabel('range (m)')
    #plt.suptitle(fn_in)

    ax1 = plt.subplot(gs[iLUT][1])
    ax1.plot(tvec,reevec,'g.-')#,markersize=1,markerfacecolor='g')
    ax1.grid('on')
    ax1.set_xticks([]);
    plt.xlim([min(tvec),max(tvec)])
    #    plt.ylabel('ree (m)')

    ax2 = plt.subplot(gs[iLUT][2])
    ax2.plot(tvec,satvec,'o-',color='c',markeredgecolor='c',markerfacecolor='none')
    losvec = np.array(losvec)+0.1
    ax2.plot(tvec,losvec,'.-',color='m')
    #    ax2.set_ylim((-0.5,1.5))
    ax2.grid('on')
    ax2.set_yticks([])
    plt.xlim([min(tvec),max(tvec)])
    ax2.legend(['SAT','LOS'],loc=5,prop={'size':8})

    ############# Plot another Link Under Test
    iLUT = 3
    LUT = linkList[iLUT]
    rangeArray = rangeDict[LUT]
    tvec = rangeArray['tstamp'] - rangeArray['tstamp'][0]
    rvec = rangeArray['rmeas']
    reevec = rangeArray['ree']
    flagvec = [int(value[0],0) for value in rangeArray['ledflags']]
    satvec = [1 & value for value in flagvec]
    losvec = [(8 & value) >> 3 for value in flagvec]
    unknown = [(40 & value) >> 5 for value in flagvec]

    gs[iLUT] = GridSpec(3,1)
    gs[3].update(left=.04,right=0.35,bottom=0.07,top=0.47,wspace=0.05,hspace=0.05)

    ax0 = plt.subplot(gs[iLUT][0])
    ax0.set_title(linkList[iLUT])
    ax0.plot(tvec,rvec,'b.-')#,markersize=1,markerfacecolor='r')
    ax0.grid('on')
    ax0.set_xticks([]);
    plt.xlim([min(tvec),max(tvec)])
    #    ax0.set_yticks([])
    #    plt.ylabel('range (m)')
        #plt.suptitle(fn_in)

    ax1 = plt.subplot(gs[iLUT][1])
    ax1.plot(tvec,reevec,'g.-')#,markersize=1,markerfacecolor='g')
    ax1.grid('on')
    ax1.set_xticks([]);
    plt.xlim([min(tvec),max(tvec)])
    #    plt.ylabel('ree (m)')

    ax2 = plt.subplot(gs[iLUT][2])
    ax2.plot(tvec,satvec,'o-',color='c',markeredgecolor='c',markerfacecolor='none')
    losvec = np.array(losvec)+0.1
    ax2.plot(tvec,losvec,'.-',color='m')
    #    ax2.set_ylim((-0.5,1.5))
    ax2.grid('on')
    ax2.set_yticks([])
    plt.xlim([min(tvec),max(tvec)])
    ax2.legend(['SAT','LOS'],loc=5,prop={'size':8})

    ############# Plot another Link Under Test
    iLUT = 4
    LUT = linkList[iLUT]
    rangeArray = rangeDict[LUT]
    tvec = rangeArray['tstamp'] - rangeArray['tstamp'][0]
    rvec = rangeArray['rmeas']
    reevec = rangeArray['ree']
    flagvec = [int(value[0],0) for value in rangeArray['ledflags']]
    satvec = [1 & value for value in flagvec]
    losvec = [(8 & value) >> 3 for value in flagvec]
    unknown = [(40 & value) >> 5 for value in flagvec]

    gs[iLUT] = GridSpec(3,1)
    gs[4].update(left=.36,right=0.67,bottom=0.07,top=0.47,wspace=0.05,hspace=0.05)

    ax0 = plt.subplot(gs[iLUT][0])
    ax0.set_title(linkList[iLUT])
    ax0.plot(tvec,rvec,'b.-')#,markersize=1,markerfacecolor='r')
    ax0.grid('on')
    ax0.set_xticks([]);
    plt.xlim([min(tvec),max(tvec)])
    #    ax0.set_yticks([])
    #    plt.ylabel('range (m)')
        #plt.suptitle(fn_in)

    ax1 = plt.subplot(gs[iLUT][1])
    ax1.plot(tvec,reevec,'g.-')#,markersize=1,markerfacecolor='g')
    ax1.grid('on')
    ax1.set_xticks([]);
    plt.xlim([min(tvec),max(tvec)])
    #    plt.ylabel('ree (m)')

    ax2 = plt.subplot(gs[iLUT][2])
    ax2.plot(tvec,satvec,'o-',color='c',markeredgecolor='c',markerfacecolor='none')
    losvec = np.array(losvec)+0.1
    ax2.plot(tvec,losvec,'.-',color='m')
    ax2.grid('on')
    ax2.set_yticks([])
    plt.xlim([min(tvec),max(tvec)])
    ax2.legend(['SAT','LOS'],loc=5,prop={'size':8})

    ############# Plot another Link Under Test
    iLUT = 5
    LUT = linkList[iLUT]
    rangeArray = rangeDict[LUT]
    tvec = rangeArray['tstamp'] - rangeArray['tstamp'][0]
    rvec = rangeArray['rmeas']
    reevec = rangeArray['ree']
    flagvec = [int(value[0],0) for value in rangeArray['ledflags']]
    satvec = [1 & value for value in flagvec]
    losvec = [(8 & value) >> 3 for value in flagvec]
    unknown = [(40 & value) >> 5 for value in flagvec]

    gs[iLUT] = GridSpec(3,1)
    gs[5].update(left=.68,right=0.99,bottom=0.07,top=0.47,wspace=0.05,hspace=0.05)

    ax0 = plt.subplot(gs[iLUT][0])
    ax0.set_title(linkList[iLUT])
    ax0.plot(tvec,rvec,'b.-')#,markersize=1,markerfacecolor='r')
    ax0.grid('on')
    ax0.set_xticks([]);
    plt.xlim([min(tvec),max(tvec)])

    ax1 = plt.subplot(gs[iLUT][1])
    ax1.plot(tvec,reevec,'g.-')#,markersize=1,markerfacecolor='g')
    ax1.grid('on')
    ax1.set_xticks([]);
    plt.xlim([min(tvec),max(tvec)])
    #    plt.ylabel('ree (m)')

    ax2 = plt.subplot(gs[iLUT][2])
    ax2.plot(tvec,satvec,'o-',color='c',markeredgecolor='c',markerfacecolor='none')
    losvec = np.array(losvec)+0.1
    ax2.plot(tvec,losvec,'.-',color='m')
    ax2.grid('on')
    ax2.set_yticks([])
    plt.xlim([min(tvec),max(tvec)])
    ax2.legend(['SAT','LOS'],loc=5,prop={'size':8})
    plt.draw()

    pdb.set_trace()


plot_stuff1(rangeDict)
#plot_2x3(rangeDict,fn_in)

pdb.set_trace()




#PlotRanges(rangeDict)
