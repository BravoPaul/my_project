from service.dataService import dataService
import pandas as pd

pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)


def choose_unversity_by_score(score, year, km, major):
    ds = dataService()
    rank = ds.getRank_by_score(score, year, km)
    score, university_max, university_middle, university_min = ds.getUniversityList_by_rank(rank, year, km, major=major)
    print('将您的分数换算到{0}年，相当于{1}分,根据{0}年各大学录取分数，为您推荐如下大学:'.format((year - 1), score))
    print('------冲一冲的大学如下：----')
    print(ds.format_university(university_max)),
    print(('-----稳妥的大学如下：------'))
    print(ds.format_university(university_middle))
    print(('-----保底的大学如下：------'))
    print(ds.format_university(university_min))


def choose_unversity_by_score_evaluate(score, year, km, major):
    ds = dataService()
    rank = ds.getRank_by_score(score, year, km)
    score, university_max, university_middle, university_min = ds.getUniversityList_by_rank(rank, year, km, major=major)
    print('将您的分数换算到{0}年，相当于{1}分,根据{0}年各大学录取分数，为您推荐如下大学:'.format((year - 1), score))
    print('------冲一冲的大学如下：----')
    print(ds.format_university(university_max)),
    print(('-----稳妥的大学如下：------'))
    print(ds.format_university(university_middle))
    print(('-----保底的大学如下：------'))
    print(ds.format_university(university_min))


def choose_unversity_by_score_run():
    while True:
        try:
            score = int(input('请输入成绩\n'))
            # wlk = str(input('请输入文理科\n'))
            # if wlk=='理科':
            #     wlk = 'lk'
            # elif wlk=='文科':
            #     wlk = 'wk'
            # else:
            #     print("输入错误，重新输入")
            #     continue
            # major = str(input('请输入专业\n'))
        except ValueError:
            print("Not an integer! Try again.")
            continue
        else:
            choose_unversity_by_score(score, 2019, 'lk', None)


if __name__ == '__main__':
    choose_unversity_by_score_run()
