import pandas as pd
import numpy as np

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

PATH_DATA_ORIGIN = '../../data/data_origin/2018河北理科.xlsx'

data = pd.read_excel('/Users/kunyue/project_personal/my_project/score_traitor/data/data_traited/所有大学-每学科统计.xlsx')


def get_university_rank(data):
    def score_cal(x):
        num = 0
        sum = 0
        for key, value in score_rank.items():
            if num==30:
                break
            if value + num > 30:
                value = 30-num
            sum += x[key] * value
            num = value + num
        return sum

    score_rank = {'A+': 22, 'A': 21, 'A-': 20, 'B+': 12, 'B': 11, 'B-': 10, 'C+': 3, 'C': 2, 'C-': 1}
    data_university = data.iloc[:, 1:11]
    data_university['score'] = data_university.apply(score_cal, axis=1)
    return data_university.sort_values(by=['score'], ascending=False)


print(get_university_rank(data))
