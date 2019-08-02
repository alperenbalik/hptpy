import inspect as _inspect
import scipy.stats as _stats
import statsmodels.api as _sm
from statsmodels.formula.api import ols as _ols
from statsmodels.stats.multicomp import MultiComparison as _MultiComparison
import hptpy.midcal.midcal_anova as _aov_mc


def anova(formula, data):
    results = _ols(formula, data=data).fit()
    aov_table = _sm.stats.anova_lm(results, typ=2)

    p_value = aov_table['PR(>F)'][0]
    result = _aov_mc.reject_notreject(p_value)

    t_results = _aov_mc.anova_output(aov_table, result)
    print(t_results)

    return results


def tukey_hsd(factor, group, data):
    mc = _MultiComparison(data[factor], data[group])
    mc_results = mc.tukeyhsd()

    print(mc_results)


def homogeneity(factor, group, data):
    factor = factor
    group = group

    # Data değişkeninin ismini data_n değikenine kaydeder.
    for fi in reversed(_inspect.stack()):
            names = [var_name for var_name, var_val in fi.frame.f_locals.items() if var_val is data]
            if len(names) > 0:
                data_n = names[0]

    codes = []

    for i in data[group].unique():
        output = "{0}['{1}'][{2}['{3}'] == '{4}']".format(data_n, factor, data_n, group, i)
        codes.append(output)

    codes_1 = ",".join(codes)
    out = "_stats.levene({})".format(codes_1)
    stat, p_value = eval(out)
    df = len(data[group].unique()) - 1

    result = _aov_mc.reject_notreject(p_value)

    args = (round(stat, 5),
            df,
            round(p_value, 9),
            result)

    t_output = _aov_mc.homogeneity_output(args)
    print(t_output)

    return stat, p_value


def normality(factor, group, data):
    factor = factor
    group = group

    # Data değişkeninin ismini data_n değikenine kaydeder.
    for fi in reversed(_inspect.stack()):
            names = [var_name for var_name, var_val in fi.frame.f_locals.items() if var_val is data]
            if len(names) > 0:
                data_n = names[0]

    results = {}

    for i in data[group].unique():
        output = "{0}['{1}'][{2}['{3}'] == '{4}']".format(data_n, factor, data_n, group, i)
        out = "_stats.shapiro({})".format(output)
        stat, p_value = eval(out)
        results[str(i)] = {"stat": stat, "p_value": p_value}

    t_output = _aov_mc.normality_output(results)
    t_output

    return results
