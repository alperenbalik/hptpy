from scipy.stats import ttest_1samp as _ttest_1samp
from scipy.stats import ttest_rel as _ttest_rel
from scipy.stats import ttest_ind as _ttest_ind
import numpy as _np
import hptpy.midcal.midcal_ttest as _tt_mc


def onesamp(x, popmean, alternative="two_sided", conf_level=0.95, axis=None, nan_policy="propagate"):
    test_name = "onesamp"
    # Serberstlik derecesi
    df = len(x) - 1
    # Alfa
    alpha = 1 - conf_level
    # Standart Sapma
    stder = _np.sqrt((x.var() / len(x)))
    # X'in ortalaması
    mean_x = float(x.mean().values)

    # İki yönlü tek örneklem hipotez testi
    statistic, pvalue = _ttest_1samp(x, popmean, axis, nan_policy)

    # p değerinin alfa güven düzeyine göre H0
    # hipotezinin reddedilip reddedilemeyeceği testi
    test_result = _tt_mc.reject_notreject(pvalue, alpha)

    # Testin yönüne göre p değeri ve
    # ortalamanın güven aralıklarının hesaplanması
    conf_int, alter_hypot, p_value = _tt_mc.confidence_int(test_name,
                                                           alternative,
                                                           statistic,
                                                           pvalue,
                                                           alpha,
                                                           conf_level,
                                                           df,
                                                           popmean=0)

    # alt ve üst güven aralıklarının hesaplanıp değişkenlere atanması
    lower = float(popmean + conf_int[0] * stder)
    upper = float(popmean + conf_int[1] * stder)

    # test çıktısında olacak değişkenler
    args = (popmean, alter_hypot, round(statistic, 5), df,
            round(p_value, 9), conf_level, test_result, conf_level,
            round(lower, 5), round(upper, 5),
            round(mean_x, 5))

    # Testin çıktılarının alınması
    t_output = _tt_mc.test_output(test_name, args)
    print(t_output)

    return statistic, p_value, df


def twosamp_paired(x, y, alternative="two_sided", conf_level=0.95, axis=None, nan_policy="propagate"):
    test_name = "twosamp_paired"
    # Serbestlik derecesi
    df = len(x) - 1
    # Alfa
    alpha = 1 - conf_level
    # iki örneklem arasındaki fark
    d = x - y
    # Standart Sapma
    stder = _np.sqrt((d.var() / len(d)))
    # X'in ortalaması
    mean_d = float(d.mean())

    # İki yönlü bağımlı 2 örneklem hipotez tesi
    statistic, pvalue = _ttest_rel(x, y, axis, nan_policy)

    # p değerinin alfa güven düzeyine göre
    # H0 hipotezinin reddedilip reddedilemeyeceği testi
    test_result = _tt_mc.reject_notreject(pvalue, alpha)

    # Testin yönüne göre p değeri ve
    # ortalamanın güven aralıklarının hesaplanması
    conf_int, alter_hypot, p_value = _tt_mc.confidence_int(test_name,
                                                           alternative,
                                                           statistic,
                                                           pvalue,
                                                           alpha,
                                                           conf_level,
                                                           df,
                                                           popmean=0)

    # alt ve üst güven aralıklarının hesaplanıp değişkenlere atanması
    popmean = 0
    lower = float(popmean + conf_int[0] * stder)
    upper = float(popmean + conf_int[1] * stder)

    # test çıktısında olacak değişkenler
    args = (popmean, alter_hypot, round(statistic, 5), df,
            round(p_value, 9), conf_level, test_result, conf_level,
            round(lower, 5), round(upper, 5),
            round(mean_d, 5))

    # Testin çıktılarının alınması
    t_output = _tt_mc.test_output(test_name, args)
    print(t_output)

    return statistic, p_value, df


def twosamp_independent(x, y, equal_var, alternative="two_sided", conf_level=0.95, axis=0, nan_policy="propagate"):
    test_name = "twosamp_independent"
    alpha = 1 - conf_level
    v1 = _np.var(x, axis, ddof=1)
    v2 = _np.var(y, axis, ddof=1)
    n1 = len(x)
    n2 = len(y)
    mean_x = float(x.mean())
    mean_y = float(y.mean())

    if equal_var:
        df, stder = _tt_mc.equal_var_df(v1, n1, v2, n2)
    else:
        df, stder = _tt_mc.unequal_var_df(v1, n1, v2, n2)

    # İki yönlü bağımlı 2 örneklem hipotez tesi
    statistic, pvalue = _ttest_ind(x, y, axis, equal_var, nan_policy)

    # p değerinin alfa güven düzeyine göre H0
    # hipotezinin reddedilip reddedilemeyeceği testi
    test_result = _tt_mc.reject_notreject(pvalue, alpha)

    # Testin yönüne göre p değeri ve ortalamanın
    # güven aralıklarının hesaplanması
    conf_int, alter_hypot, p_value = _tt_mc.confidence_int(test_name,
                                                           alternative,
                                                           statistic,
                                                           pvalue,
                                                           alpha,
                                                           conf_level,
                                                           df,
                                                           popmean=0)

    # alt ve üst güven aralıklarının hesaplanıp değişkenlere atanması
    popmean = 0
    lower = float(popmean + conf_int[0] * stder)
    upper = float(popmean + conf_int[1] * stder)

    # test çıktısında olacak değişkenler
    args = (popmean, alter_hypot, round(statistic, 5), df,
            round(p_value, 9), conf_level, test_result, conf_level,
            round(lower, 5), round(upper, 5),
            round(mean_x, 5), round(mean_y, 5))

    t_output = _tt_mc.test_output(test_name, args)
    print(t_output)

    return statistic, p_value, df
