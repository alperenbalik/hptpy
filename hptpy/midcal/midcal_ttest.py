from scipy.stats import t as _t
import numpy as _np


def equal_var_df(v1, n1, v2, n2):
    # twosamp_indepent için varsansın eşit olduğunu
    # kabul ettiğimiz zaman serbestlik derecesi ve standart hata hesabı

    df = n1 + n2 - 2.0
    svar = ((n1 - 1) * v1 + (n2 - 1) * v2) / df
    stderr = _np.sqrt(svar * (1.0 / n1 + 1.0 / n2))
    return df, stderr


def unequal_var_df(v1, n1, v2, n2):
    # twosamp_indepent için varsansın eşit olmadığını kabul ettiğimiz
    # zaman serbestlik derecesi ve standart hata hesabı

    vn1 = v1 / n1
    vn2 = v2 / n2
    with _np.errstate(divide='ignore', invalid='ignore'):
        df = (vn1 + vn2)**2 / (vn1**2 / (n1 - 1) + vn2**2 / (n2 - 1))

    # If df is undefined, variances are zero (assumes n1 > 0 & n2 > 0).
    # Hence it doesn't matter what df is as long as it's not NaN.
    df = _np.where(_np.isnan(df), 1, df)
    stderr = _np.sqrt(vn1 + vn2)
    return df, stderr


def reject_notreject(pvalue, alpha):
    if pvalue < alpha:
        result = "Reject null hypothesis"
    else:
        result = "Cannot reject null hypothesis"

    return result


def confidence_int(test_name, alternative, statistic, pvalue, alpha, conf_level, df, popmean=0):
    if test_name == "onesamp":
        if alternative == "less":
            conf_int = [-_np.inf, statistic + _t.ppf(conf_level, df)]
            alter_hypot = "Alternative hypothesis: True mean is less than " + str(popmean)
            p_value = _t.cdf(statistic, df)
        elif alternative == "greater":
            conf_int = [statistic - _t.ppf(conf_level, df), _np.inf]
            alter_hypot = "Alternative hypothesis: True mean is greater than " + str(popmean)
            p_value = _t.sf(statistic, df)
        else:
            conf_int = _t.ppf(1 - alpha/2, df)
            conf_int = [-conf_int + statistic, conf_int + statistic]
            alter_hypot = "Alternative hypothesis: True mean is not equal to " + str(popmean)
            p_value = pvalue
    elif test_name == "twosamp_paired":
        if alternative == "less":
            conf_int = [-_np.inf, statistic + _t.ppf(conf_level, df)]
            alter_hypot = "Alternative hypothesis: True difference in means is less than " + str(popmean)
            p_value = _t.cdf(statistic, df)
        elif alternative == "greater":
            conf_int = [statistic - _t.ppf(conf_level, df), _np.inf]
            alter_hypot = "Alternative hypothesis: True difference in means is greater than " + str(popmean)
            p_value = _t.sf(statistic, df)
        else:
            conf_int = _t.ppf(1 - alpha/2, df)
            conf_int = [-conf_int + statistic, conf_int + statistic]
            alter_hypot = "Alternative hypothesis: True difference in means is not equal to " + str(popmean)
            p_value = pvalue
    else:
        if alternative == "less":
            conf_int = [-_np.inf, statistic + _t.ppf(conf_level, df)]
            alter_hypot = "Alternative hypothesis: True difference in means is less than " + str(popmean)
            p_value = _t.cdf(statistic, df)
        elif alternative == "greater":
            conf_int = [statistic - _t.ppf(conf_level, df), _np.inf]
            alter_hypot = "Alternative hypothesis: True difference in means is greater than " + str(popmean)
            p_value = _t.sf(statistic, df)
        else:
            conf_int = _t.ppf(1 - alpha/2, df)
            conf_int = [-conf_int + statistic, conf_int + statistic]
            alter_hypot = "Alternative hypothesis: True difference in means is not equal to " + str(popmean)
            p_value = pvalue

    return conf_int, alter_hypot, p_value


def test_output(test_name, args):
    if test_name == "onesamp":
        output = "One Sample T-test\n" \
                "\nNull hypothesis: True mean is equal to {0}" \
                "\n{1}\n" \
                "\nt = {2}, df = {3}, p-value = {4}\n" \
                "\nTest result for {5} confidence level: {6}\n" \
                "\n{7} confidence interval:" \
                "\n{8} {9}\n" \
                "\nmeans of x: {10}".format(*args)

    elif test_name == "twosamp_paired":
        output = "Paired Sample T-test\n" \
                "\nNull hypothesis: True difference in means is to {0}" \
                "\n{1}\n" \
                "\nt = {2}, df = {3}, p-value = {4}\n" \
                "\nTest result for {5} confidence level: {6}\n" \
                "\n{7} confidence interval:" \
                "\n{8} {9}\n" \
                "\nmeans of differences: {10}".format(*args)

    else:
        output = "Independent Sample T-test\n" \
                "\nNull hypothesis: True difference in means is to {0}" \
                "\n{1}\n" \
                "\nt = {2}, df = {3}, p-value = {4}\n" \
                "\nTest result for {5} confidence level: {6}\n" \
                "\n{7} confidence interval:" \
                "\n{8} {9}\n" \
                "\nmeans of x: {10}" \
                "\nmeans of y: {11}".format(*args)

    return output
