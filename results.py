import matplotlib.pyplot
import scipy.stats


# TODO: Significance level
def report_test(p_values, test_name):
    matplotlib.pyplot.hist(p_values, 10)
    matplotlib.pyplot.savefig(test_name + ".png")
    statistic, kspvalue = scipy.stats.kstest(p_values, 'uniform')

    with open(test_name + ".result", "w") as out:
        for p in p_values:
            if p > 0.01:
                out.write(str(p) + " PASS\n")
            else:
                out.write(str(p) + " FAIL\n")
        out.write("\n----------\n")
        out.write("KS VALUE: " + str(kspvalue) + "\n")

