#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Imports
import sys
import re
import matplotlib.pyplot as plt
import argparse
import csv
import json
import random
import datetime


def createParser():
    parser = argparse.ArgumentParser(
        prog='nmlogparcer',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='An utility to plot with matplotlib stuff fast',
        epilog='''usage examples:
        IPERF:
            nmlogparcer_v5.py -if ../../../Data/LOGsamples/iperf3/iperf_fra_plain.txt --format IPERF -k Retr
            nmlogparcer_v5.py -if ../../../Data/LOGsamples/iperf3/iperf_fra_plain_V.txt --format IPERF -k Cwnd --fin
        IPERF_JSON:
            nmlogparcer_v5.py -if ../../../Data/LOGsamples/iperf3/iperf_fra_json.json --format IPERF_JSON -k rtt --streamid 0 --timeshift 7200 --labely iperfR11 -d 1000
            nmlogparcer_v5.py --fin --labely "RTT [mks]" --logy
            nmlogparcer_v5.py -if ../../../Data/LOGsamples/iperf3/iperf_fra_json.json --format IPERF_JSON -k bits_per_second --labely iperfR11 -d 1e9
            nmlogparcer_v5.py --fin --labely "RAte [Gbps]" 
        NETROPY:
            nmlogparcer_v5.py -if ../../../Data/LOGsamples/netropy/netropy_history_1.csv -k 6 --format NETROPY --labely Rate
        RMDT:
            nmlogparcer_v5.py -if ../../../Data/LOGsamples/rmdt/RMDT_sender_plain.log -k SDR 
            nmlogparcer_v5.py -if ../../../Data/LOGsamples/rmdt/RMDT_sender_plain.log -k RBR 
            nmlogparcer_v5.py -of ../../../Data/LOGsamples/sample2.png --figuretitle 2 --outputfile_dpi 121 -fs 24,12
    IPERF KEYS: Transfer, Bitrate, Retr, Cwnd
    IPERF JSON KEYS: bits_per_second, retransmits, bytes, snd_cwnd, rtt, rttvar, pmtu
    ''')
    parser.add_argument(  # DONE
        "-if",
        "--inputfile",
        nargs="?",
        type=str,
        default="",
        help="read and parse logs from this .log file. Default is `None`",
    )
    parser.add_argument(  # DONE
        "-of",
        "--outputfile",
        nargs="?",
        type=str,
        default="",
        help="save plot as static picture, examples: fig.png, etc/fig.jpeg. Default is None",
    )
    parser.add_argument(  # DONE
        "--format",
        nargs="?",
        type=str,
        default="RMDT",
        help="read and parse logs in the some format. Possible variants: RMDT, RMDT_IPI, NETROPY, IPERF, IPERF_JSON, DRAW_HLINE. Default is RMDT",
    )
    parser.add_argument(  # DONE
        "-fs",
        "--figsize",
        nargs="?",
        type=str,
        default="12, 6",
        help="Figure size in format `XX,YY`. Default is `12,6`",
    )
    parser.add_argument(  # DONE
        "-k",
        "--key",
        nargs="?",
        type=str,
        default="None",
        help="key for the parce and curve. Default is `None`",
    )
    parser.add_argument(  # DONE
        "-d",
        "--delimeter",
        nargs="?",
        type=float,
        default=1,
        help="delimeter for plot. Default is 1",
    )
    parser.add_argument(  # DONE
        "--figuretitle",
        nargs="?",
        type=str,
        default="None",
        help="Can be used to separate plots. For the same plots should be identical. Default is `None`",
    )
    parser.add_argument(  # DONE
        "--subtitle",
        nargs="?",
        type=str,
        default="None",
        help="subtitle for sertain plot. Default is `None`",
    )
    parser.add_argument(  # DONE
        "--labely",
        nargs="?",
        type=str,
        default=None,
        help="Label for legend or for Y. Default is None and --key is used.",
    )
    parser.add_argument(  # DONE
        "--labelx",
        nargs="?",
        type=str,
        default=None,
        help="Label for X. Default is None and --key is used.",
    )
    parser.add_argument(  # DONE
        "--logy",
        action="store_true",
        help="Plot with logy. Default is False.",
    )
    parser.add_argument(  # DONE
        "--logx",
        action="store_true",
        help="Plot with logx. Default is False.",
    )
    parser.add_argument(  # DONE
        "--ylim",
        nargs="?",
        type=str,
        default=None,
        help="Limit the Y by a range. Format is like `0, 1e10`. Default is None.",
    )
    parser.add_argument(  # DONE
        "--xlim",
        nargs="?",
        type=str,
        default=None,
        help="Limit the X by a range. Format is like `0, 1e10`. Default is None.",
    )
    parser.add_argument(  # DONE
        "--timex",
        action="store_true",
        help="Plot with localtime HH:MM:SS insdead of time index [s]. Default is index.",
    )
    parser.add_argument(  # DONE
        "--timeshift",
        nargs="?",
        type=int,
        default=0,
        help="Time shift, to eliminate clock shift.",
    )
    parser.add_argument(
        "--zero",
        action="store_true",
        help="Plot from zero time.",
    )
    parser.add_argument(  # DONE
        "--fin",
        action="store_true",
        help="Key to instant call plt.show(). Default is False.",
    )
    parser.add_argument(  # DONE
        "--rmdt_negativekey",
        nargs="?",
        type=str,
        default="None",
        help="Search logline NOT by a sertain pattern. Default is `None`",
    )
    parser.add_argument(  # DONE
        "--rmdt_mainpattern",
        nargs="?",
        type=str,
        default="::Logging:",
        help="Search logline by a sertain pattern. Default is `::Logging:`",
    )
    parser.add_argument(  # DONE
        "--rmdt_idpattern",
        nargs="?",
        type=str,
        default=";ID_: ",
        help="Search for sertain ID pattern. Default is `;ID_: 1`",
    )
    parser.add_argument(  # DONE
        "--outputfile_dpi",
        nargs="?",
        type=int,
        default=140,
        help="DPI of figure so save. default is 140",
    )
    parser.add_argument(  # DONE
        "--streamid",
        nargs="?",
        type=str,
        default="SUM",
        help="Search stream by a sertain id. Default is `SUM`",
    )
    parser.add_argument(  # DONE
        "--linewidth",
        nargs="?",
        type=float,
        default=1.0,
        help="Plot with certain linewidth",
    )
    parser.add_argument(  # DONE
        "--linestyle",
        nargs="?",
        type=str,
        default="-",
        help="Plot with certain linewidth, default is '-'",
    )
    parser.add_argument(  # DONE
        "--linemarker",
        nargs="?",
        type=str,
        default="",
        help="Plot with certain lie marker, default is no marker",
    )
    parser.add_argument(  # DONE
        "--linemarkersize",
        nargs="?",
        type=float,
        default=2,
        help="Plot with certain lie marker size, default is 2",
    )
    parser.add_argument(  # DONE
        "--hline",
        nargs="?",
        type=str,
        default="",
        help="Plot a horizontail line with coordinates 'Y,Xmin,Xmax'",
    )
    parser.add_argument(  # DONE
        "--linecolor",
        nargs="?",
        type=str,
        default="",
        help="Plot a horizontail line with coordinates 'Y,Xmin,Xmax'",
    )
    parser.add_argument(  # DONE
        "--legendtoright",
        action="store_true",
        help="Put legend to the right side of the plot",
    )
    parser.add_argument(  # DONE
        "--csvdelimeter",
        nargs="?",
        type=str,
        default=",",
        help="Delimeter for CSV parcing,default is ','",
    )
    parser.add_argument(  # DONE
        "--xcolumn",
        nargs="?",
        type=int,
        default=0,
        help="Column in CSV contains the X value (isdigit), default is 0",
    )
    parser.add_argument(  # DONE
        "--ycolumn",
        nargs="?",
        type=int,
        default=5,
        help="Column in CSV contains the Y value (isdigit), default is 5",
    )
    return parser


def parceNETROPY(filename,
                 column=5,
                 timeshift=0,
                 zero=False,
                 csvdelimeter=','):
    time, Par = [], []
    with open(filename, newline='') as csvfile:
        scvreader = csv.reader(csvfile, delimiter=csvdelimeter, quotechar='|')
        for row in scvreader:
            if row[0].isdigit():
                TimeSample = row[1].split(":")
                time.append(
                    float(TimeSample[0]) * 3600 + float(TimeSample[1]) * 60 +
                    float(TimeSample[2]))
                Par.append(int(row[column]))
    if (zero == True or timeshift != 0):
        if (zero):
            timeshift = timeshift - min(time)
        for i in range(len(time)):
            time[i] = time[i] + timeshift
    return time, Par


def parceCSV(filename,
             MainLinePattern="Registered",
             SideLinePattern="LTE",
             xcolumn=0,
             ycolumn=5,
             timeshift=0,
             zero=False,
             csvdelimeter=','):
    time, Par = [], []
    counter = 0
    with open(filename, newline='') as csvfile:
        scvreader = csv.reader(csvfile, delimiter=csvdelimeter, quotechar='|')
        for row in scvreader:
            if MainLinePattern in row and SideLinePattern in row:
                counter += 1
                try:
                    # timesample = datetime.datetime.fromtimestamp( float(row[xcolumn]) / 1000)
                    time.append(float(row[xcolumn]) / 1000)
                except:
                    exit("error X value (not a digit) " + row[xcolumn])
                    TimeSample = row[1].split(":")
                    time.append(
                        float(TimeSample[0]) * 3600 +
                        float(TimeSample[1]) * 60 + float(TimeSample[2]))
                try:
                    Par.append(float(row[ycolumn]))
                except:
                    exit("error Y value (not a digit) " + row[ycolumn])
            else:
                continue
    if (zero == True or timeshift != 0):
        if (zero):
            timeshift = timeshift - min(time)
        for i in range(len(time)):
            time[i] = time[i] + timeshift
    print("lines in CSV:" + str(counter))
    return time, Par


def parceRMDT(filename,
              MainLinePattern="::Logging:",
              SideLinePattern=";ID_: 1",
              ValValSplitPattern=";",
              ValParSplitPattern=":",
              PosValPattern="RTT_:",
              NegValPattern="None",
              delimeter=1,
              zero=True,
              timeshift=0):
    time, Par = [], []
    with open(filename, "r") as f:
        for line in f.readlines():
            if MainLinePattern in line and SideLinePattern in line:
                ValVal = line.split(ValValSplitPattern)
                for Val in ValVal:
                    if PosValPattern in Val and NegValPattern not in Val:
                        ValPar = Val.split(ValParSplitPattern)[1]
                        TimeSample = re.search(
                            r"(([0-2]?[0-9]):([0-5]?[0-9]):([0-5]?[0-9]).([0-9])*)",
                            line)[1].split(":")
                        time.append(
                            float(TimeSample[0]) * 3600 +
                            float(TimeSample[1]) * 60 + float(TimeSample[2]))
                        try:
                            Par.append(
                                float(
                                    re.search(r"-?[\d]*\.?[\d]+(?:e-?\+?\d+)?",
                                              ValPar)[0]) / delimeter)
                        except:
                            Par.append(0)
                        break
    if (zero == True or timeshift != 0):
        if (zero):
            timeshift = timeshift - min(time)
        for i in range(len(time)):
            time[i] = time[i] + timeshift

    return time, Par


def parceIPERF(filename,
               PosValPattern="Bitrate",
               streamID=5,
               zero=True,
               timeshift=0,
               delimeter=1):
    time, Par = [], []
    body, timer = False, 0
    with open(filename, "r") as f:
        for line in f.readlines():
            if body:
                splitted = line.split()
                if "Interval" in line or "Complete" in line:
                    break
                if "- - -" in line:
                    continue
                if streamID == splitted[1].split("]")[0] or streamID == "SUM":
                    if (PosValPattern == "Transfer"):
                        Par.append(float(splitted[4]) / delimeter)
                    elif (PosValPattern == "Bitrate"):
                        Par.append(float(splitted[6]) / delimeter)
                    elif (PosValPattern == "Retr"):
                        Par.append(float(splitted[8]) / delimeter)
                    elif (PosValPattern == "Cwnd"):
                        Par.append(float(splitted[9]) / delimeter)
                    else:
                        exit("waka")
                    timer += float(splitted[2].split("-")[1]) - float(
                        splitted[2].split("-")[0])
                    time.append(timer)
            else:
                if "Interval" in line:
                    body = True
        if (zero == True or timeshift != 0):
            if (zero):
                timeshift = timeshift - min(time)
            for i in range(len(time)):
                time[i] = time[i] + timeshift
    return time, Par


def parceIPERFJSON(filename,
                   streamID='0',
                   keyPattern="bits_per_second",
                   timeshift=0,
                   zero=True,
                   delimeter=1):
    time, Par = [], []
    data = ""
    with open(filename, "r") as f:
        for line in f.readlines():
            data += line
            if line == "}\n":
                break
    obj = json.loads(data)
    TimeSample = re.search(
        r"(([0-2]?[0-9]):([0-5]?[0-9]):([0-5]?[0-9]).([0-9])*)",
        obj["start"]["timestamp"]["time"])[0].split(":")
    start = float(TimeSample[0]) * 3600 + float(TimeSample[1]) * 60 + float(
        TimeSample[2])
    for i in obj["intervals"]:
        if streamID == "SUM":
            Par.append(float(i["sum"][keyPattern]) / delimeter)
        elif streamID.isdecimal():
            Par.append(
                float(i["streams"][int(streamID)][keyPattern]) / delimeter)
        else:
            exit("streamID ERROR")
        time.append(float(i["sum"]["start"]) + start)

    if (zero == True or timeshift != 0):
        if (zero):
            timeshift = timeshift - min(time)
        for i in range(len(time)):
            time[i] = time[i] + timeshift
    return time, Par


def exit(msg):
    print(msg)
    sys.exit()


if __name__ == "__main__":
    parsed = createParser().parse_args()
    if parsed.inputfile:
        if parsed.format == "RMDT":
            X, Y = parceRMDT(filename=parsed.inputfile,
                             PosValPattern=parsed.key,
                             NegValPattern=parsed.rmdt_negativekey,
                             MainLinePattern=parsed.rmdt_mainpattern,
                             SideLinePattern=parsed.rmdt_idpattern,
                             delimeter=parsed.delimeter,
                             timeshift=parsed.timeshift)
        elif parsed.format == "RMDT_IPI":  # DODELAI
            print("Attempt to read as RMDT ipi receiver plain")
        elif parsed.format == "NETROPY":
            X, Y = parceNETROPY(filename=parsed.inputfile,
                                column=int(parsed.key),
                                timeshift=parsed.timeshift,
                                zero=parsed.zero,
                                csvdelimeter=parsed.csvdelimeter)
        elif parsed.format == "CSV":
            X, Y = parceCSV(
                filename=parsed.inputfile,
                xcolumn=int(parsed.xcolumn),
                ycolumn=int(parsed.ycolumn),
                timeshift=parsed.timeshift,
                zero=parsed.zero,
                csvdelimeter=parsed.csvdelimeter,
                MainLinePattern="Registered",
                SideLinePattern="LTE",
            )
        elif parsed.format == "IPERF":
            X, Y = parceIPERF(filename=parsed.inputfile,
                              PosValPattern=parsed.key,
                              streamID=parsed.streamid,
                              timeshift=parsed.timeshift,
                              delimeter=parsed.delimeter)
        elif parsed.format == "IPERF_JSON":
            X, Y = parceIPERFJSON(filename=parsed.inputfile,
                                  streamID=parsed.streamid,
                                  keyPattern=parsed.key,
                                  timeshift=parsed.timeshift,
                                  delimeter=parsed.delimeter)
        else:
            exit("Not known format.")

        if not parsed.labely:
            labely = parsed.key
        else:
            labely = parsed.labely
        clr = parsed.linecolor if parsed.linecolor else (random.random(),
                                                         random.random(),
                                                         random.random())

        plt.figure(parsed.figuretitle)
        plt.suptitle(parsed.subtitle)
        plt.plot(X,
                 Y,
                 label=labely,
                 ls=parsed.linestyle,
                 linewidth=parsed.linewidth,
                 marker=parsed.linemarker,
                 markersize=parsed.linemarkersize,
                 color=clr)
        plt.xlabel(parsed.labelx)
        plt.ylabel(parsed.labely)
        plt.grid(True)
        legend = plt.legend(loc="upper left", shadow=True)
    else:
        clr = parsed.linecolor if parsed.linecolor else (random.random(),
                                                         random.random(),
                                                         random.random())

        if parsed.hline:
            hline = [float(i) for i in parsed.hline.split(",")]
            plt.hlines(hline[0],
                       hline[1],
                       hline[2],
                       color=clr,
                       label=parsed.labely,
                       ls=parsed.linestyle,
                       linewidth=parsed.linewidth)

            plt.xlabel(parsed.labelx)
            plt.ylabel(parsed.labely)
            legend = plt.legend(loc="upper left", shadow=True)

    if parsed.fin:
        fsize = tuple([int(i) for i in parsed.figsize.split(",")])
        plt.figure(parsed.figuretitle).set_size_inches((fsize[0], fsize[1]),
                                                       forward=True)
        plt.xlabel(parsed.labelx)
        plt.ylabel(parsed.labely)
        plt.suptitle(parsed.subtitle)
        if parsed.xlim:
            fsize = tuple([float(i) for i in parsed.xlim.split(",")])
            plt.xlim(fsize[0], fsize[1])
        if parsed.ylim:
            fsize = tuple([float(i) for i in parsed.ylim.split(",")])
            plt.ylim(fsize[0], fsize[1])
        if parsed.logy:
            plt.semilogy()
        if parsed.logx:
            plt.semilogx()
        if parsed.legendtoright:
            plt.legend(bbox_to_anchor=(1.04, 1), loc="upper left")
    #        plt.legend(bbox_to_anchor=(1.35, .9))
        if parsed.outputfile:
            plt.figure(parsed.figuretitle).savefig(parsed.outputfile,
                                                   dpi=parsed.outputfile_dpi,
                                                   transparent=True,
                                                   bbox_inches="tight")
        plt.show()
