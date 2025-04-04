#!/usr/bin/env python
#--------------------------------------------------------------------------------------
# Aapted by Mathews Chirindo - South African Radio Astronomy Obsevatory
# With the authority from:
# COMPANY              : PERALEX ELECTRONICS (PTY) LTD
#--------------------------------------------------------------------------------------
# COPYRIGHT NOTICE :
#
# The copyright, manufacturing and patent rights stemming from this document
# in any form are vested in PERALEX ELECTRONICS (PTY) LTD.
#
# (c) PERALEX ELECTRONICS (PTY) LTD 2021
#
# PERALEX ELECTRONICS (PTY) LTD has ceded these rights to its clients
# where contractually agreed.
#--------------------------------------------------------------------------------------
# DESCRIPTION :
#
# This script uploads a spectometer fpg file to a one or more SKARAB systems that contain one 
# or more SKARAB ADC boards, and then computes and plots the spectrum of the synchronised ADC sample data.
# This script reads the spectrum values from the memory blocks, interleaves the values and
# plots the spctrum of the input signal.  
# The user of this script needs to provide the test parameters under the "2. SCRIPT 
# CONFIG" code section. Some of these test parameters include the channels of the SKARAB ADC boards 
# to plot data from. 
# The script then uses the provided test parameters, the command line parameters along with the 
# information in the fpg file to (automatically) identify the Master and Slave SKARAB ADC boards 
# (if any) among the SKARAB systems, their corresponding SKARAB ADC Yellow Blocks and their bandwidth 
# modes (DDC or Bypass). In this tutorial we are only concerned with the Bypass mode and one ADC board
# configured as Master. 
# The script then uses the identified information to create a Skarab Adc object (from the casperfpga 
# Python library) for the SKARAB ADC board.
# These objects are used to provide a simple means of controlling and configuring the
# SKARAB ADC board(s) so that synchronised sample data can be captured. The sample data is written 
# to text files so that it can be plotted/examined if required.
# The sample data of each ADC channel is stored in a separate text file under the adc_data_byp 
# directory which is automatically generated by this script.

# To run this script you need to execute the following on the command line:

# ```bash
# python tut_spec_byp.py <skarab IP or hostname> -l <accumulation length> -b <fpgfile name>
# ```

# replacing <skarab IP or hostname> with the IP address of your Skarab, <accumulation length> is the 
# number of accumulations, and <fpgfile name> with your fpgfile.

#--------------------------------------------------------------------------------------

import casperfpga
from casperfpga import skarab_definitions as sd
import sys
import os.path
from os import path

import time,numpy,struct,logging,pylab,matplotlib
import matplotlib.pyplot as plt
import datetime as dt
import numpy as np
import time

actual_channels_ddc_centre_freq = 0.0



def get_data():
	#get the data...    
	#acc_n = skarabs[0].read_uint('acc_cnt')
	#a_1=struct.unpack('>256Q',skarabs[0].read('mem1',256*8,0))
	#a_2=struct.unpack('>256Q',skarabs[0].read('mem2',256*8,0))
	#a_3=struct.unpack('>256Q',skarabs[0].read('mem3',256*8,0))
	#a_4=struct.unpack('>256Q',skarabs[0].read('mem4',256*8,0))
	#a_5=struct.unpack('>256Q',skarabs[0].read('mem5',256*8,0))
	#a_6=struct.unpack('>256Q',skarabs[0].read('mem6',256*8,0))
	#a_7=struct.unpack('>256Q',skarabs[0].read('mem7',256*8,0))
	#a_8=struct.unpack('>256Q',skarabs[0].read('mem8',256*8,0))
        #a_1=struct.unpack('>1024h',skarabs[0].read('sxr_re_0',1024*2,0))
	a_1=struct.unpack('>256h',skarabs[0].read('packet_buffer_sxl_re_1',256*2,0))
	#a_2=struct.unpack('>256h',skarabs[0].read('packet_buffer_sxl_re_3',256*2,0))
	#a_3=struct.unpack('>256h',skarabs[0].read('packet_buffer_sxl_re_0',256*2,0))
	#a_4=struct.unpack('>256h',skarabs[0].read('packet_buffer_sxl_re_1',256*2,0))
	#a_5=struct.unpack('>256B',skarabs[0].read('mem_left_0_4',256*1,0))
	#a_6=struct.unpack('>256B',skarabs[0].read('mem_left_0_5',256*1,0))
	#a_7=struct.unpack('>256B',skarabs[0].read('mem_left_0_6',256*1,0))
	#a_8=struct.unpack('>256B',skarabs[0].read('mem_left_0_7',256*1,0))
	#a_1=struct.unpack('>2048L',skarabs[0].read('mem32',2048*4,0))
	#a_1=struct.unpack('>2048L',skarabs[0].read('mem31',2048*4,0))
	#a_2=struct.unpack('>256L',skarabs[0].read('mem26',256*4,0))
	#a_3=struct.unpack('>256L',skarabs[0].read('mem27',256*4,0))
	#a_4=struct.unpack('>256L',skarabs[0].read('mem28',256*4,0))
	#a_5=struct.unpack('>256L',skarabs[0].read('mem29',256*4,0))
	#a_6=struct.unpack('>256L',skarabs[0].read('mem30',256*4,0))
	#a_7=struct.unpack('>256L',skarabs[0].read('mem31',256*4,0))
	#a_8=struct.unpack('>256L',skarabs[0].read('mem32',256*4,0))

	interleave_a=[]

	#for i in range(256):
	for i in range(256):
		 interleave_a.append(a_1[i])
		#interleave_a.append(a_2[i])
		#interleave_a.append(a_3[i])
		#interleave_a.append(a_4[i])
		#interleave_a.append(a_5[i])
		#interleave_a.append(a_6[i])
		#interleave_a.append(a_7[i])
		#interleave_a.append(a_8[i])
	#return acc_n, numpy.array(interleave_a,dtype=numpy.float)
	return numpy.array(interleave_a,dtype=numpy.float)




        #for i in range(256):
	#for i in range(2048):
                #interleave_a.append(a_1[i])
                #interleave_a.append(a_2[i])
                #interleave_a.append(a_3[i])
                #interleave_a.append(a_4[i])
                #interleave_a.append(a_5[i])
                #interleave_a.append(a_6[i])
                #interleave_a.append(a_7[i])
                #interleave_a.append(a_8[i])
        #return acc_n, numpy.array(interleave_a,dtype=numpy.float)




def plot_spectrum():
        freq_range_mhz = [0,256]
        matplotlib.pyplot.clf()  # la funzione clf() di pyplot serve a ripulire la figura attuale/precedente
        interleave_a = get_data()
       # interleave_a = interleave_a[::-1]
        peak = np.amax(interleave_a)
        indx = np.argmax(interleave_a)
        print indx, peak
        print(np.linspace(0,256.,256).shape,interleave_a.shape)
        matplotlib.pylab.plot(np.linspace(0,256./2-1,256)*(175.*16.)/256.,interleave_a,'b')
        matplotlib.pylab.title('Campioni complessi')
        #matplotlib.pylab.ylabel('Power (dB)')
        matplotlib.pylab.grid()
        matplotlib.pylab.xlabel('Numero del campione')
        matplotlib.pylab.xlim(freq_range_mhz[0], freq_range_mhz[1])
        fig.canvas.draw()
        fig.canvas.manager.window.after(100, plot_spectrum)


#START OF MAIN:
if __name__ == '__main__':

    from optparse import OptionParser
    p = OptionParser()
    p.set_usage('spectrometer.py <SKARAB_HOSTNAME_or_IP> [options]')
    p.set_description(__doc__)
    p.add_option('-l', '--acc_len', dest='acc_len', type='int',default=1430,
    help='Set the number of vectors to accumulate between dumps. default is 2*(2^28)/4096, or just under 2 seconds.')
    p.add_option('-b', '--fpg', dest='fpgfile',type='str', default='',
            help='Specify the fpg file to load')
    p.add_option('-u', '--upload_file', dest='upload_file', type='str', default = 'y')
    p.add_option('-d', '--decimation', dest='decimation', type='int', default=32,
            help='Decimation factor [16, 32, 64, 128]')
    p.add_option('-s', '--sampling_rate', dest='sampling_rate', type='int', default=3000,
            help='Sampling rate in MHz [3000, 2560, 2048]')
    p.add_option('-f', '--centre_frequency', dest='centre_frequency', type='float', default=1000.0,
            help='centre frequency in MHz rate in MHz [default 1000.]')
    opts, args = p.parse_args(sys.argv[1:])

    opts, args = p.parse_args(sys.argv[1:])
    if args==[]:
        print 'Please specify a SKARAB board. Run with the -h flag to see all options.\nExiting.'
        exit()
    else:
        skarab_ip = args[0]
    if opts.fpgfile != '':
            bitstream = opts.fpgfile
    if opts.fpgfile != '':
        bitstream = opts.fpgfile
    if opts.sampling_rate == 2560:
        sampling_rate = 1
    elif opts.sampling_rate == 2048:
        sampling_rate = 2
    else:
        sampling_rate = 0  # default, 3 GHz
    decimation = opts.decimation

try:
    # -----------------------------------------------------------------
    # 1. PRINT TEST HEADER
    # -----------------------------------------------------------------
    print("------------------------------------------------------")
    print("SKARAB ADC SYNCHRONISED SAMPLING AND SPECTROMETER TEST")
    print("------------------------------------------------------")

    # -----------------------------------------------------------------
    # 2. SCRIPT CONFIG
    # -----------------------------------------------------------------
    # 2.1 SET THE FPG FILE DIRECTORY
    #  bitstream = 'tut_spec_byp_3_2021-07-21_2340.fpg'
    #fpg_file_dir = "tut_spec_byp_3_2021-07-12_1350.fpg"
    #fpg_file_dir = "tut_spec_byp_3_2021-07-06_1429.fpg"

    # 2.2 ENABLE FPG FILE UPLOAD OR NOT 
    # - If the fpg file is already uploaded it is not required to 
    #   do it again. This allows the script to execute faster.
    upload_fpg_file = opts.upload_file   #'y' # Other options: 'n'

    # 2.3 SET THE SKARAB IP(s)
    # - If there are more than one SKARAB systems in the hardware setup, 
    #   the IP of the Master SKARAB system should be listed first
    #   (leftmost). The SKARAB ADC board that has a corresponding
    #   Master SKARAB ADC Yellow Block in the fpg file uploaded to 
    #   its SKARAB system will be the master while all other SKARAB ADC 
    #   boards in the hardware setup will be the slaves.
    skarab_ips = [skarab_ip] # Other options: ['10.0.7.3']; etc

    # 2.4 SET THE NYQUIST ZONE FOR WHICH THE SKARAB ADC BOARDS SHOULD BE OPTIMISED
    # - Available Options: sd.FIRST_NYQ_ZONE  (First Nyquist zone)
    #                      sd.SECOND_NYQ_ZONE (Second Nyquist zone)
    nyquist_zone = sd.FIRST_NYQ_ZONE # Other options: sd.SECOND_NYQ_ZONE

    # 2.5 SET THE SKARAB ADC BOARD DATA MODE 
    # - Available Options: sd.ADC_DATA_MODE:  Default ADC sample data mode
    #                      sd.RAMP_DATA_MODE: Ramp pattern test mode
    # - Note that if the data mode is set to RAMP MODE, the 
    #   ramp patterns will not be synchronised since the ramp pattern 
    #   generators of the SKARAB ADC boards are not synchronised.
    data_mode=sd.ADC_DATA_MODE # Other options: sd.RAMP_DATA_MODE

    # 2.6 SET THE GAIN OF THE SKARAB ADC BOARD AMPLIFIERS
    # - Available gain options (dB): -6 to 15 (must be integers)
    #   where [ch0 gain, ch1 gain, ch2 gain, ch3 gain]
    channels_gain = [-6, -6, -6, -6] # Other options: [0, -6, 0, -6]; etc

    # 2.7 SET THE DDC CENTRE FREQUENCY
    # - This only has effect when the SKARAB ADC boards are used 
    #   in the DDC bandwidth mode.
    # - Note that the accuracy of the DDC frequency is limited by
    #   a 16-bit register value. Please review the skarabadc.py
    #   source file from the casperfpga library for more 
    #   information.
    channels_ddc_centre_freq = 1000000000 # Other options: 400000000; etc
    #channels_ddc_centre_freq = int(np.round(opts.centre_frequency*1.0e6))

    # 2.8 SET THE CHANNELS (0 TO 3) THAT SHOULD BE INCLUDED IN TEST
    # channels_to_test = [0, 1, 2, 3] # Other options: [0]; [0, 2]; etc
    channels_to_test = [0, 1] # Other options: [0]; [0, 2]; etc

    # -----------------------------------------------------------------
    # 3. CONNECT TO SKARAB HARDWARE AND UPLOAD FPG FILE
    # -----------------------------------------------------------------
    if upload_fpg_file == 'y':
        print("------------------")
        print("UPLOAD FPG FILE(s)")
        print("------------------")
    skarab_num = len(skarab_ips)
    skarabs = [None] * 4
    for i in range(skarab_num):
        print(skarab_ips[i])
        skarabs[i] = casperfpga.CasperFpga(skarab_ips[i])
        if upload_fpg_file == 'y':
                skarabs[i].upload_to_ram_and_program(bitstream)
        else:
                skarabs[i].get_system_information(bitstream)
    if upload_fpg_file == 'y':
        print("FPG files uploaded to SKARAB(s) successfully")
    raw_input("Press Enter to continue with the ADC data captures")

    # -----------------------------------------------------------------
    # 4. DETERMINE TEST PARAMATERS
    # - Note that the Yellow Block tags are used to identify the  
    #   SKARAB ADC Yellow Blocks from the fpg file
    #     DDC Mode SKARAB ADC Yellow Block tag: xps:skarab_adc4x3g_14
    #     Bypass Mode SKARAB ADC Yellow Block tag: xps:skarab_adc4x3g_14
    # -----------------------------------------------------------------
    # 4.1 GET NUMBER OF ADCS PER SKARAB
    adcs_per_skarab_num = 0
    for memory_device_name in skarabs[0].memory_devices:
        memory_device = skarabs[0].memory_devices[memory_device_name]
        if hasattr(memory_device, 'device_info'):
            if memory_device.device_info['tag'] == 'xps:skarab_adc4x3g_14' or memory_device.device_info['tag'] == 'xps:skarab_adc4x3g_14_byp':
                adcs_per_skarab_num = adcs_per_skarab_num + 1
    if adcs_per_skarab_num == 0:
        print("ERROR: No SKARAB ADC Yellow Blocks found in uploaded design")
        exit()

    # 4.2 GET SKARAB ADC YELLOW BLOCK NAMES AND MEZZANINE SITES
    skarab_adc_yb_names = [None] * adcs_per_skarab_num
    skarab_mez_sites = [None] * adcs_per_skarab_num
    itr = 0
    device_tag = ''
    for memory_device_name in skarabs[0].memory_devices:
        memory_device = skarabs[0].memory_devices[memory_device_name]
        if hasattr(memory_device, 'device_info'):
            if memory_device.device_info['tag'] == 'xps:skarab_adc4x3g_14' or memory_device.device_info['tag'] == 'xps:skarab_adc4x3g_14_byp':
                if memory_device.master_slave == 'Master':
                    device_tag = memory_device.device_info['tag']
                    skarab_adc_yb_names[itr] = memory_device.name
                    skarab_mez_sites[itr] = memory_device.mezzanine_site
                    itr = itr + 1
    for memory_device_name in skarabs[0].memory_devices:
        memory_device = skarabs[0].memory_devices[memory_device_name]
        if hasattr(memory_device, 'device_info'):
            if memory_device.device_info['tag'] == 'xps:skarab_adc4x3g_14' or memory_device.device_info['tag'] == 'xps:skarab_adc4x3g_14_byp':
                if memory_device.master_slave == 'Slave':
                    skarab_adc_yb_names[itr] = memory_device.name
                    skarab_mez_sites[itr] = memory_device.mezzanine_site
                    itr = itr + 1

    # 4.3 GET NUMBER of SKARAB ADC Yellow BLOCKS PER SKARAB
    skarab_adc_yb_per_skarab_num = len(skarab_adc_yb_names)

    # 4.4 GET NUMBER OF SKARABS
    skarab_adc_num = skarab_num * adcs_per_skarab_num

    # 4.5 GET USER IP CLOCK SOURCE
    user_ip_clock_source = skarabs[0].system_info['clk_src']

    # -----------------------------------------------------------------
    # 5 CREATE SKARAB ADC OBJECT FOR EACH SKARAB ADC BOARD
    # ----------------------------------------------------------------- 
    # 5.1 CREATE SKARAB ADC OBJECTS
    skarab_adcs = [None]*skarab_adc_num
    for i in range(skarab_num):
        for j in range(adcs_per_skarab_num):
            skarab_adcs[adcs_per_skarab_num*i+j] = skarabs[i].memory_devices[skarab_adc_yb_names[j]]

    # 5.2 CREATE SKARAB ADC SLAVE OBJECTS
    skarab_adc_slaves = []
    if skarab_adc_num > 1:
        skarab_adc_slave_num = skarab_adc_num-1
        skarab_adc_slaves = [None]*skarab_adc_slave_num
        for i in range(skarab_adc_slave_num):
            skarab_adc_slaves[i]=skarab_adcs[i+1]
    yb_type = skarab_adcs[0].yb_type
    # -----------------------------------------------------------------
    # 6.0
    # Synchronize to PPS
    # -----------------------------------------------------------------
    print("Synchronizing to PPS")
    software_pps = False   # True if self_generated PPS must be used
    if software_pps: 
        sw_pps_mask = 0x2
    else:
        sw_pps_mask = 0x0

    frac_time = np.mod(time.time(),1.0) # ensure to be not too close to PPS
    if frac_time > 0.8: 
        time.sleep(1.1-frac_time)
        frac_time = np.mod(time.time(),1.0)

    utc_time = int(time.time()) + 1  # sync to next PPS
    for i in range(skarab_num):
	skarabs[i].write_int('utc_time', utc_time)
        skarabs[i].write_int('sw_pps', sw_pps_mask) 

    if software_pps: 		        # if PPS generated by SW wait for next UTC boundary
        time.sleep(1.0-frac_time)

    for i in range(skarab_num):	# Trigger PPS capture. 
        skarabs[i].write_int('sw_pps', sw_pps_mask | 0x5) 
    if not software_pps:                # For HW pps, wait for it to occur
        time.sleep(1.0)
    for i in range(skarab_num):     # deassert LOAD_PPS signal and check that time has been captured
        skarabs[i].write_int('sw_pps', sw_pps_mask) 
	# print(str("Skarab ")+str(i)+str(" time counter: ")+str(
        #       skarabs[i].read_uint('utc_time_count')))
 
    # -----------------------------------------------------------------
    # 6. CONFIGURE SKARAB ADC BOARD
    # - Note that the configure_skarab_adc function automatically 
    #   determines the bandwidth (sampling) mode for which the SKARAB   
    #   ADC board(s) need to be configured based on the specific SKARAB   
    #   ADC Yellow Block in the fpg file. Thus, no argument except the   
    #   Nyquist zone is provided.
    # -----------------------------------------------------------------
    for i in range(skarab_adc_num):
        skarab_adcs[i].enable_skarab_adc_dout(False)
    print("")
    print("------------------------")
    print("SETTING UP SKARAB ADC(s)")
    print("------------------------")
    print("Configuring SKARAB ADC boards...")
    for i in range(skarab_adc_num):
        #skarab_adcs[i].configure_skarab_adc(nyquist_zone,32)
    #skarab_adcs[i].configure_skarab_adc(nyquist_zone, 32)
         skarab_adcs[i].configure_skarab_adc(nyquist_zone, decimation, sampling_rate)

    # -----------------------------------------------------------------
    # 7. SET DATA MODE
    # -----------------------------------------------------------------
    print("Setting data mode of SKARAB ADC boards...")
    for i in range(skarab_adc_num):
        skarab_adcs[i].set_skarab_adc_data_mode(data_mode)

    # -----------------------------------------------------------------
    # 8. SET CHANNEL GAIN
    # -----------------------------------------------------------------
    print("Setting channel gain of SKARAB ADC boards...")
    for i in range(skarab_adc_num):
        for j in range(4):
            skarab_adcs[i].set_skarab_adc_channel_gain(j, channels_gain[j])

    # -----------------------------------------------------------------
    # 9. SET DDC FREQUENCY
    # - Note that the DDCs are tuned to 1 GHz by default, and 
    #   thus, it is not required to run this function to set it 
    #   again if this is already the desired DDC frequency.
    # -----------------------------------------------------------------
    actual_channels_ddc_centre_freq = 0
    if yb_type == sd.YB_SKARAB_ADC4X3G_14:
        print("Setting DDC centre frequency of SKARAB ADC boards...")
        for i in range(skarab_adc_num):
            for j in range(4):
                actual_channels_ddc_centre_freq = skarab_adcs[i].configure_skarab_adc_ddcs(j, channels_ddc_centre_freq)[0]

        skarabs[i].write_int('center_freq',int(round(actual_channels_ddc_centre_freq)))
    # -----------------------------------------------------------------
    # 10. RESET ALL SNAPSHOT BLOCK CAPTURE COMPONENTS
    # -----------------------------------------------------------------
    # 10.1 IF THE USER IP CLOCK SOURCE IS SET TO SYS_CLK, RESET THE 
    #      SKARAB ADC BOARDS BEFORE ARMING SNAPSHOT COMPONENTS
    if user_ip_clock_source == 'sys_clk':
        for i in range(skarab_adc_num):
            skarab_adcs[i].reset_skarab_adc()

    # 10.2 ARM ALL SNAPSHOT BLOCK CAPTURE COMPONENTS
    #for i in range(skarab_num):
    #    skarabs[i].write_int('clr_bc', 1)
    #    skarabs[i].write_int('clr_bc', 0)
    #    for snapshot in skarabs[i].snapshots:
    #            if "adc" in snapshot.name:
    #                    snapshot.arm()

    # 10.3 IF THE USER IP CLOCK SOURCE IS SET TO ADC_CLK, RESET THE 
    #      SKARAB ADC BOARDS AFTER ARMING SNAPSHOT COMPONENTS
    if user_ip_clock_source == 'adc_clk':
        for i in range(skarab_adc_num):
            skarab_adcs[i].reset_skarab_adc()

    # -----------------------------------------------------------------
    # 11. PERFORM A SYNCHRONISED CAPTURE
    # -----------------------------------------------------------------
    print("")
    print("----------------")
    print("ADC DATA CAPTURE")
    print("----------------")
    skarab_adcs[0].sync_skarab_adc(skarab_adc_slaves)

    for i in range(skarab_adc_num):
        skarab_adcs[i].enable_skarab_adc_dout(True)
    # -----------------------------------------------------------------
    # 12. PRINT TEST PARAMETERS
    # -----------------------------------------------------------------
    print("")
    print("---------------")
    print("TEST PARAMETERS")
    print("---------------")

    print(str("FPG file directory: " + str(bitstream)))
    print(str("Number of SKARABS: " + str(skarab_num)))
    print(str("SKARAB IP(s): " + str(skarab_ips).strip('[]')))
    print(str("Number of SKARAB ADCs per SKARAB: " + str(adcs_per_skarab_num)))
    print(str("SKARAB ADC Yellow Block Names: " + str(skarab_adc_yb_names).strip('[]')))
    print(str("SKARAB ADC Mezzanine Sites: " + str(skarab_mez_sites).strip('[]')))

    if yb_type == sd.YB_SKARAB_ADC4X3G_14:
        print("SKARAB ADC Yellow Block type: 3 GHz, dec-by-4, DDC mode (YB_SKARAB_ADC4X3G_14)")
    elif yb_type == sd.YB_SKARAB_ADC4X3G_14_BYP:
        print("SKARAB ADC Yellow Block type: 2.8 GHz, full-bandwidth   (YB_SKARAB_ADC4X3G_14_BYP)")

    print(str("Total Number of SKARAB ADCs: " + str(skarab_adc_num)))

    if user_ip_clock_source == 'sys_clk':
        print("User IP clock source: SYS_CLK")
    elif user_ip_clock_source == 'adc_clk':
        print("User IP clock source: ADC_CLK")

    if yb_type == sd.YB_SKARAB_ADC4X3G_14:
        print(str("Specified DDC Centre Frequency: " + str(channels_ddc_centre_freq)))
        print(str("Actual DDC Centre Frequency: " + str(actual_channels_ddc_centre_freq)))

    if nyquist_zone == sd.ADC_DATA_MODE:
        print("SKARAB ADC data mode: ADC DATA")
    elif nyquist_zone == sd.RAMP_DATA_MODE:
        print("SKARAB ADC data mode: Ramp")
        
    print(str("Channel 0 gain (dB): " + str(channels_gain[0])))
    print(str("Channel 1 gain (dB): " + str(channels_gain[1])))
    print(str("Channel 2 gain (dB): " + str(channels_gain[2])))
    print(str("Channel 3 gain (dB): " + str(channels_gain[3])))

    if nyquist_zone == sd.FIRST_NYQ_ZONE:
        print("Nyquist zone optimisation: First")
    elif nyquist_zone == sd.SECOND_NYQ_ZONE:
        print("Nyquist zone optimisation: Second")

    # Set registers.
    print 'Configuring accumulation period...',
    sys.stdout.flush()
    for i in range(skarab_num):
        skarabs[i].write_int('acc_len',opts.acc_len)
        #skarabs[i].write_int('dest_ip1', DEST_IP)
        #skarabs[i].write_int('dest_port1', DEST_PORT)
    print 'done'

    for i in range(skarab_num):
        #skarabs[i].write_int('fft_shift', 0x00ff)
        skarabs[i].write_int('fft_shift', 32768)

    print 'Resetting counters...',
    sys.stdout.flush()
    for i in range(skarab_num):
        
        skarabs[i].write_int('rst_cpoge',1)
        skarabs[i].write_int('rst_cpoge',0)
        skarabs[i].write_int('cnt_rst',1)
        skarabs[i].write_int('cnt_rst',0)
        # skarabs[i].write_int('shift',20)
        
    print 'done'

    # Sync the ADC
    #   print 'Syncing the ADC...'
    sys.stdout.flush()

    # -----------------------------------------------------------------
    # 15. PRINT TEST FOOTER
    # -----------------------------------------------------------------
    print("---------------------------------------------------------------")
    print("SKARAB ADC SYNCHRONISED SAMPLING AND SPECTROMETER TEST COMPLETE")
    print("---------------------------------------------------------------")

    counter = 0
    central_freq_MHZ = channels_ddc_centre_freq / 1000000
    inicio = dt.datetime.now()
    inicio_str = inicio.strftime("_%Y-%m-%d_%H%M%S")
    aux_inicio_str = inicio_str
    print("---------------------------------------------------------------")
    print("---------------------------------------------------------------")
    print 'STARTING ACCUMULATING DATA...'
    aux_meusdados = []
    try:
        while True:
            my_interleave_a = get_data()
	    counter += 1
	    aux_meusdados.append(my_interleave_a)
	    if ((counter % 2000) == 0):
			
	    	print 'Checkpoint!'

	    	aux_final = dt.datetime.now()
	    	aux_final_str = aux_final.strftime("_%Y-%m-%d_%H%M%S")
	    	aux_file_name = 'Pulsar_dados_Fc%d_MHz_Ti%s_Tf%s' % (central_freq_MHZ, aux_inicio_str, aux_final_str)

	    	np.save(aux_file_name, np.array(aux_meusdados))

	    	aux_inicio_str = aux_final_str
	    	aux_meusdados = []
    except KeyboardInterrupt:
        final = dt.datetime.now()
        tempo = final - inicio
        print tempo
        final_str=final.strftime("_%Y-%m-%d_%H%M%S")
        file_name = 'Pulsar_dados_Fc%d_MHz_Ti%s_Tf%s' % (central_freq_MHZ, inicio_str, final_str)
        #np.save(file_name,np.array(meusdados))
        #os.remove(str(aux_file_name) + '.npy')
	print 'SKARAB STOPPED RUNNING.'

except KeyboardInterrupt:
    exit()
