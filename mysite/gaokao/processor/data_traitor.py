# update sqlite_sequence set seq = 0 where name = 'gaokao_schooldetail';
# delete from sqlite_sequence where name = 'gaokao_schooldetail';
# delete from sqlite_sequence;


class DataTraitor(object):
    def __init__(self):
        import sqlite3
        self.basic_path = '/Users/kunyue/project_personal/my_project/mysite/data/'
        self.conn = sqlite3.connect("../../db.sqlite3")
        self.cur = self.conn.cursor()

    def university_save_sqlite(self):
        import pickle
        from gaokao.models import School
        data_origin = pickle.load(open(self.basic_path + 'university.pkl', "rb"))
        print('正在执行')
        for sch in data_origin:
            new_education = School(**sch)
            new_education.save()

    def university_detail_sqlite(self):
        import pickle
        from gaokao.models import School, SchoolRank, SchoolDetail, SchoolFamous
        data_origin = pickle.load(open(self.basic_path + 'spider_all_university_detail.pkl', "rb"))
        print('正在执行')
        for sch_detail in data_origin:
            sch_id = sch_detail['sch_id']
            detail_kargs = {}
            result_detail = sch_detail['result']
            detail_kargs['canteen_desc'] = result_detail['sch_detail_info']['canteen_desc']
            detail_kargs['sch_address'] = result_detail['sch_detail_info']['sch_address']
            detail_kargs['sch_fellowship'] = result_detail['sch_detail_info']['sch_fellowship']
            detail_kargs['sch_intro'] = result_detail['sch_detail_info']['sch_intro']
            detail_kargs['sch_scholarship'] = result_detail['sch_detail_info']['sch_scholarship']
            detail_kargs['sch_tel_num'] = result_detail['sch_detail_info']['sch_tel_num']
            detail_kargs['sch_web_url'] = result_detail['sch_detail_info']['sch_web_url']
            detail_kargs['stu_dorm_desc'] = result_detail['sch_detail_info']['stu_dorm_desc']
            detail_kargs['sch_master_ratio'] = result_detail['sch_detail_info']['sch_master_ratio']
            detail_kargs['sch_abroad_ratio'] = result_detail['sch_detail_info']['sch_abroad_ratio']
            school = School.objects.get(sch_id=sch_id)
            SchoolDetail.objects.create(**detail_kargs, school=school)

            if result_detail['sch_rank_info'] is not None:
                for sch_rank in result_detail['sch_rank_info']:
                    rank_kargs = {}
                    rank_kargs['rank_type_desc'] = sch_rank['rank_type_desc']
                    rank_kargs['rank_year'] = sch_rank['rank_year']
                    rank_kargs['rank_idx'] = sch_rank['rank_idx']
                    rank_kargs['rank_score'] = sch_rank['rank_score']
                    rank_kargs['rank_type'] = sch_rank['rank_type']
                    rank_kargs['world_rank_idx'] = sch_rank['world_rank_idx']
                    school = School.objects.get(sch_id=sch_id)
                    SchoolRank.objects.create(**rank_kargs, school=school)

            if result_detail['sch_celebrity_info'] is not None:
                for sch_celebrity in result_detail['sch_celebrity_info']:
                    celebrity_kargs = {}
                    celebrity_kargs['celebrity_name'] = sch_celebrity['celebrity_name']
                    celebrity_kargs['celebrity_desc'] = sch_celebrity['celebrity_desc']
                    school = School.objects.get(sch_id=sch_id)
                    SchoolFamous.objects.create(**celebrity_kargs, school=school)


print('执行了么')
dt = DataTraitor()
dt.university_detail_sqlite()
