import pandas as pd

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

PATH_DATA_ORIGIN = '../../data/data_origin/2019河北理科.xlsx'


def analyse_score(path):
    data = pd.read_excel(path)
    data = data.sort_values(by=['score'], ascending=False)
    print(data)


def analyse_score_run():
    analyse_score(PATH_DATA_ORIGIN)

if __name__ == '__main__':
    analyse_score_run()
