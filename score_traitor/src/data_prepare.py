import pandas as pd

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

PATH_BASIC = '../data/data_origin/'


def data_read_df(path):
    df = pd.read_excel(path,header=0)
    df = df.dropna(subset=['score'])
    df.rename(columns={'Unnamed: 0': 'university', 'Unnamed: 1': 'score', 'Unnamed: 2': 'yw', 'Unnamed: 3': 'sx',
                       'Unnamed: 4': 'yy'}, inplace=True)
    return df


def data_read_df_run():
    path_w = PATH_BASIC + '2019河北文科_tmp.xlsx'
    path_l = PATH_BASIC + '2019河北理科_tmp.xlsx'
    data_like = data_read_df(path_l)
    data_wenke = data_read_df(path_w)
    data_like.to_excel(PATH_BASIC + '2019河北理科.xlsx')
    data_wenke.to_excel(PATH_BASIC + '2019河北文科.xlsx')


if __name__ == '__main__':
    data_origin = data_read_df_run()

    print(data_origin)
