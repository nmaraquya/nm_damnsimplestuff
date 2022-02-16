import os
import nmlogparcer_v5 as nm
import matplotlib.pyplot as plt

ifile = "Data/ninjaprobe3/RMDT_sender.log"
x, y = nm.parceRMDT(ifile)
plt.figure("prototypetitle")
plt.suptitle("prototypesubtitle")
fig = plt.figure(1)
ax = fig.add_subplot(111, label="1")
ax2 = fig.add_subplot(111, label="2", frame_on=False)

ax.set_ylabel('Inflight, Bytes', color="red")
ax.scatter(x,
           nm.parceRMDT(ifile, PosValPattern="INFL_")[1],
           color='r',
           alpha=0.4,
           s=4,
           label="INFL")
ax.plot(x, nm.parceRMDT(ifile, PosValPattern="INFL_")[1], color='r', alpha=0.4)
ax.axhline(y=25e4, color='black', linestyle=':', linewidth=2, label="BDP")
ax.axhline(y=60e4, color='black', linestyle=':', linewidth=2, label="BDP+buff")
ax2.set_ylabel('RTT, mks', color="blue")
ax2.scatter(x,
            nm.parceRMDT(ifile, PosValPattern="RTT")[1],
            color='b',
            alpha=0.4,
            s=1,
            label="RTT")
ax2.yaxis.tick_right()
ax2.yaxis.set_label_position('right')
ax.set_ylim(0, 70e4)
ax2.set_ylim(0, 1e5)
ax.grid(True)
ax.fill_between(x,
                0,
                nm.parceRMDT(ifile, PosValPattern="INFL_")[1],
                step="pre",
                color='gray',
                alpha=0.1,
                hatch='xx')
ax.fill_between(x, 0, 25e4, step="pre", color='b', alpha=0.1)
ax.fill_between(x, 25e4, 60e4, step="pre", color='g', alpha=0.1)
ax.fill_between(x, 60e4, 70e4, step="pre", color='r', alpha=0.1)

ax.legend(loc='upper left', shadow=True)
ax2.legend(loc='upper right', shadow=True)
#ax.legend(bbox_to_anchor=(.4, 1.15), bbox_transform=ax.transAxes)
#ax2.legend(bbox_to_anchor=(.8, 1.15), bbox_transform=ax.transAxes)
plt.show()

#22:36:39.731311 [rmdt] <INFO     > makeSubmissionLog  →  BQLCCA::Logging:;ID_: 1;TR_num_: 15;RTT_: 2142;SBR_:986742225;RBR_: 997106726;PLR_: 0;INFL_:385108;INFL_MAX_:2825535;OVER_:0;RTT_mean_: 1227;INFLkalman_:1.53277e+06;Perr_: 0;Ierr_: 0;Derr_: 0;Presp_: 0;Iresp_: 0;Dresp_: 0;Fresp_: 0;SPrtt_: 125000;ipiamount_: 142;ipiamountbase_: 68;ipir_: 7.13829e-05;ipis_: 7.23701e-05;probeR_: 7.30984e-05;probeS_: 3.42184e-05;probeA_: 67;probeI_: 3.36487e-05;bnckAVB_: 986492160;evalAVB_: 9.86504e+08;bnckCPU_: 2.10418e+09;bnckR_: 2143024416;bnckIOR_: 0;bnckIOW_: 0;ipis_host_: 7.30809e-05;ipidiff_: 0.0638973;ipidiffLast_: 0.0138304;RATE_fromIPIR_: 1010144896;RATE_fromPIPIR_: 986492160;SDRipi_: 996371504;INFLind_:387602;Kalman_: 1247.43;bCounter_: 1.24488e+06;ninjaAVB_: 9.86633e+08;ninjaAVBlast_: 9.86492e+08;ninjaSync_: 0.976531;ninjaSyncLog_: -0.00287554;ipisum_: 10.554;probeDISP_: -0.0305473;probeDIF_: -0.509831;probeDIF2_: 0.0009123;Host2sent_: 0.00982142;probe2resdiff_: inf;probeRate_: 2.14308e+09 ('BQLCCA.cpp:217')