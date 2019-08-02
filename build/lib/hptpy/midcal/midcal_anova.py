def homogeneity_output(args):
    output = "Levene's Test of Homogeneity of Variance\n" \
                "\nNull hypothesis: Variances are equal across groups" \
                "\nAlternative hypothesis: Variances are not equal across groups\n" \
                "\nW = {0}, df = {1}, p-value = {2}\n" \
                "\nTest result for 0.95 confidence level: {3}\n".format(*args)
    return output


def normality_output(results):
    output = "Shapiro-Wilks Test of Normality\n" \
        "\nNull hypothesis: Population is normally distributed" \
        "\nAlternative hypothesis: Population is not normally distributed\n" \
        "\nTest result for 0.95 confidence level:" \
        "\n---Populations:"

    print(output)

    for i in results.keys():
        key = i
        w_stat = results[i]["stat"]
        p_value = results[i]["p_value"]
        output = "\t{:>8}: W:{:>8}, p value:{:>8}, null hypothesis: {:>8}".format(key,
                                                                                  round(w_stat, 8),
                                                                                  round(p_value, 8),
                                                                                  reject_notreject(p_value))
        print(output)


def anova_output(aov_table, results):
    output = "One Way ANOVA\n" \
        "\nNull hypothesis: There is no difference between the means" \
        "\nAlternative hypothesis: There is difference between the means\n" \
        "\n{0}\n" \
        "\nTest result for 0.95 confidence level: {1}".format(aov_table, results)
    return output


def reject_notreject(pvalue):
    if pvalue < 0.05:
        result = "Reject null hypothesis"
    else:
        result = "Cannot reject null hypothesis"

    return result
