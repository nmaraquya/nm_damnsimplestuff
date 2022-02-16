import os
import nmlogparcer_v5 as nm
import matplotlib.pyplot as plt

ifile = "data/iperf3/iperf_ger_json.json"
x, y = nm.parceIPERFJSON(
    ifile, keyPattern="bits_per_second", streamID="0", zero=True, timeshift=10)
plt.figure("title")
plt.suptitle("subtitle")

plt.plot(x, y, label="bits_per_second")
plt.grid(True)
legend = plt.legend(loc="upper left", shadow=True)
plt.show()


# run from rootdir
