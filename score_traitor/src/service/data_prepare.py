import pandas as pd

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

PATH_BASIC = '../data/data_origin/'
PATH_TRAITED = '../data/data_traited/'


def data_read_df(path):
    df = pd.read_excel(path, header=0)
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


def trait_score_rank(data):
    def score_t(x):
        try:
            return int(x)
        except:
            index = str(x).find('及以上')
            if index > 0:
                return x[0:index]
            else:
                return -1

    print(data)
    data['score'] = data.iloc[:, 0].map(score_t)
    result = data[data['score'] != -1]
    result_df = pd.DataFrame.from_dict(
        {'score': result['score'], 'rank_wk': result.iloc[:, 1], 'rank_wk_cum': result.iloc[:, 2],
         'rank_lk': result.iloc[:, 3], 'rank_lk_cum': result.iloc[:, 4]})
    return result_df[['score', 'rank_wk', 'rank_wk_cum', 'rank_lk', 'rank_lk_cum']]


def trait_score_rank_run():
    data = pd.read_excel(PATH_BASIC + '2018河北一分一档pdf_excel.xlsx', sheet_name=None)
    result_final = pd.DataFrame.from_dict(
        {'score': [], 'rank_wk': [], 'rank_wk_cum': [], 'rank_lk': [], 'rank_lk_cum': []})
    for key, data_one in data.items():
        result = trait_score_rank(data_one)
        result_final = pd.concat([result_final, result])
    result_final.to_excel(PATH_TRAITED + '2018河北一分一档表.xlsx')


def trait_score_university(data):
    try:
        data = data.dropna(subset=['院校名称'])
        result = pd.DataFrame.from_dict(
            {'university': data.iloc[:, 0], 'score': data.iloc[:, 1], 'yw': data.iloc[:, 2], 'sx': data.iloc[:, 3],
             'yy': data.iloc[:, 4]})
        result['university'] = result['university'].map(lambda x: x.replace('ft', '山'))
        return result[['university', 'score', 'yw', 'sx', 'yy']]
    except:
        return pd.DataFrame.from_dict(
            {'university': [], 'score': [], 'yw': [], 'sx': [], 'yy': []})


def trait_score_university_run():
    data = pd.read_excel(PATH_BASIC + '2018年本科一批理pdf_excel.xlsx', sheet_name=None)
    result_final = pd.DataFrame.from_dict(
        {'university': [], 'score': [], 'yw': [], 'sx': [], 'yy': []})
    for key, data_one in data.items():
        result = trait_score_university(data_one)
        result_final = pd.concat([result_final, result])
    result_final.to_excel(PATH_TRAITED + '2018河北理科投档线.xlsx')


def merge_score(data_all, data_merge, year):
    result = pd.concat([data_all, data_merge], axis=1)
    return result

def merge_score_run():
    data_all = pd.read_excel(PATH_TRAITED + '2019河北一分一档表.xlsx')
    data_merge = pd.read_excel(PATH_TRAITED + '2018河北一分一档表.xlsx')
    merge_score(data_all,data_merge,2018)





if __name__ == '__main__':
    # data_origin = data_read_df_run()
    # print(data_origin)
    # trait_score_university_run()
    print(merge_score())
