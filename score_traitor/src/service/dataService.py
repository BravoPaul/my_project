import pandas as pd
from tabulate import tabulate
import numpy as np


class dataService(object):
    def __init__(self):
        self.path_origin = '../../data/data_traited/'
        data_2019_score = pd.read_excel(self.path_origin + '2019河北一分一档表.xlsx')
        data_2019_lk = pd.read_excel(self.path_origin + '2019河北理科投档线.xlsx')
        data_2019_wk = pd.read_excel(self.path_origin + '2019河北文科投档线.xlsx')
        data_2018_score = pd.read_excel(self.path_origin + '2018河北一分一档表.xlsx')
        data_2018_lk = pd.read_excel(self.path_origin + '2018河北理科投档线.xlsx')
        data_2018_wk = pd.read_excel(self.path_origin + '2018河北文科投档线.xlsx')
        data_major = pd.read_excel(self.path_origin + '所有大学-每学科统计.xlsx')
        self.data_origin = {
            '2019_score': data_2019_score,
            '2019_lk': data_2019_lk,
            '2019_wk': data_2019_wk,
            '2018_score': data_2018_score,
            '2018_lk': data_2018_lk,
            '2018_wk': data_2018_wk,
            'major': Major(data_major)
        }

    def getRank_by_score(self, score, year, km):
        data = self.data_origin[str(year) + '_score']
        rank = data[data['score'] == score]['rank_' + km].values[0]
        rank_cum = data[data['score'] == score]['rank_' + km + '_' + 'cum'].values[0]
        print('{0}年,获得{1}分的同学,一共有{2}人'.format(year, score, rank))
        print('此分数的排名为: ', int(rank_cum))
        return int(rank_cum)

    def getUniversityList_by_rank(self, rank, year, km, major=None):
        data_score = self.data_origin[str(year - 1) + '_score']
        score_min = data_score[data_score['rank_' + km + '_' + 'cum'] >= rank].head(1)['score'].values[0]
        score_max = data_score[data_score['rank_' + km + '_' + 'cum'] <= rank].tail(1)['score'].values[0]
        data_university = self.data_origin[str(year - 1) + '_' + km]
        data_university = data_university.sort_values(by=['score'], ascending=False)
        data_university = pd.merge(data_university, data_score[['score', 'rank_' + km + '_' + 'cum']], on=['score'])
        data_university = data_university.rename(columns={'rank_' + km + '_' + 'cum': 'rank'})
        if major is not None:
            major_rank = self.data_origin['major'].university_major
            major_rank = major_rank[major_rank['major'] == major]
            data_university = pd.merge(data_university, major_rank, on=['university'])

        # data_university_max = data_university[
        #                           (data_university['score'] >= score_max)][-50:-5]
        # data_university_middle = data_university[
        #                              (data_university['score'] <= score_min)][-5:6]
        # data_university_min = data_university[
        #                           (data_university['score'] <= score_min)][6:20]

        return score_min, data_university



    def getMajorRank(self, major):
        return self.data_origin['major'].get_major_rank(major)

    def format_university(self, data):
        data = data.rename(
            columns={'university': '大学', 'score': '投档线', 'rank': '排名', 'yw': '语文成绩', 'sx': '数学成绩', 'yy': '英语成绩',
                     'major': '专业', 'level': '专业等级'})
        if '专业' in data.columns:
            result = data.reset_index()[['大学', '投档线', '排名', '语文成绩', '数学成绩', '英语成绩', '专业', '专业等级']]
        else:
            result = data.reset_index()[['大学', '投档线', '排名', '语文成绩', '数学成绩', '英语成绩']]
        return tabulate(result, headers='keys', tablefmt='psql')


class Major(object):
    def __init__(self, df_origin):
        self.data = df_origin
        self.major = self.__get_all_major()
        self.university_major = self.__get_university_major()
        self.university_rank = self.__get_university_rank()

    def __get_all_major(self):
        data_major = pd.DataFrame(self.data.iloc[:, 11:].columns)

        def map_func(x):
            if x.split(' ')[0] < '0700':
                return '人文社科类' + '_' + x.split(' ')[1]
            elif x.split(' ')[0] < '0800':
                return '理学' + '_' + x.split(' ')[1]
            elif x.split(' ')[0] < '0900':
                return '工学' + '_' + x.split(' ')[1]
            elif x.split(' ')[0] < '1000':
                return '农学' + '_' + x.split(' ')[1]
            elif x.split(' ')[0] < '1200':
                return '医学' + '_' + x.split(' ')[1]
            elif x.split(' ')[0] < '1300':
                return '管理学' + '_' + x.split(' ')[1]
            elif x.split(' ')[0] < '1400':
                return '艺术学' + '_' + x.split(' ')[1]
            else:
                raise ValueError

        data_major['major_1'] = data_major[0].map(lambda x: map_func(x).split('_')[0])
        data_major['major_2'] = data_major[0].map(lambda x: map_func(x).split('_')[1])
        return data_major[['major_1', 'major_2']]

    def __get_university_major(self):
        length_col = len(self.data.columns)
        data_university = self.data.iloc[:, np.r_[1, 11:length_col]]
        data_university.columns = data_university.columns.map(
            lambda x: x.split(' ')[1] if len(x.split(' ')) == 2 else x)
        result = data_university.set_index(['学校名称']).stack().reset_index()
        result.rename(columns={'学校名称': 'university', 'level_1': 'major', 0: 'level'}, inplace=True)
        return result

    def __get_university_rank(self):

        def score_cal(x):
            num = 0
            sum = 0
            for key, value in score_rank.items():
                if num == 30:
                    break
                if value + num > 30:
                    value = 30 - num
                sum += x[key] * value
                num = value + num
            return sum

        score_rank = {'A+': 12, 'A': 11, 'A-': 10, 'B+': 8, 'B': 7, 'B-': 6, 'C+': 4, 'C': 3, 'C-': 2}
        data_university = self.data.iloc[:, 1:11]
        data_university['score'] = data_university.apply(score_cal, axis=1)
        result = data_university.sort_values(by=['score'], ascending=False).rename(columns={'学校名称': 'university'})
        return result

    def get_major_rank(self, major):
        if major not in self.major['major_2'].unique():
            raise ValueError
        rank_order = {'A+': 9, 'A': 8, 'A-': 7, 'B+': 6, 'B': 5, 'B-': 4, 'C+': 3, 'C': 2, 'C-': 1}
        university_major = self.university_major[self.university_major['major'] == major]
        university_major['rank_num'] = university_major['rank'].map(lambda x: rank_order[x])
        university_major = university_major.sort_values(by=['rank_num'])
        university_major_rank = pd.merge(self.university_rank, university_major, on=['university'])
        result = university_major_rank.sort_values(by=['rank_num', 'score'], ascending=False)
        return result
