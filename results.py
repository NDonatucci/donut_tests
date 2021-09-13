import matplotlib.pyplot
import scipy.stats
from pathlib import Path


# TODO: Significance level
def report_test(p_values, test_name):
    dir = "out/" + test_name
    Path(dir).mkdir(parents=True, exist_ok=True)
    matplotlib.pyplot.hist(p_values, 10)
    matplotlib.pyplot.savefig(dir + "/" + test_name + ".png")
    matplotlib.pyplot.close()
    statistic, kspvalue = scipy.stats.kstest(p_values, 'uniform')

    print(test_name.upper() + ":")
    print("Kolmogorov-Smirnov: " + str(kspvalue))
    if kspvalue > 0.01:
        print("PASS")
    else:
        print("FAIL")
    print("------------")

    with open(dir + "/" + test_name + ".result", "w") as out:
        for p in p_values:
            if p > 0.01:
                out.write(str(p) + " PASS\n")
            else:
                out.write(str(p) + " FAIL\n")
        out.write("\n----------\n")
        out.write("KS VALUE: " + str(kspvalue) + "\n")

