import os
import nmlogparcer_v5 as nm
import matplotlib.pyplot as plt

ifile = "data/iperf3/iperf_fra_json.json"
x, y = nm.parceIPERFJSON(
    ifile, keyPattern="rtt", streamID="0", zero=True, timeshift=10)
plt.figure("title")
plt.suptitle("subtitle")

plt.plot(x, y, label="rtt")
plt.grid(True)
legend = plt.legend(loc="upper left", shadow=True)
plt.show()


# run from rootdir
