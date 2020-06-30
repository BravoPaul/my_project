# update sqlite_sequence set seq = 0 where name = 'gaokao_schooldetail';
# delete from sqlite_sequence where name = 'gaokao_schooldetail';
# delete from sqlite_sequence;

# python manage.py shell < /Users/kunyue/project_personal/my_project/mysite/gaokao/processor/data_traitor.py

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

    def university_score_sqlite(self):
        import pickle
        from gaokao.models import School, SchoolScore
        data_origin = pickle.load(open(self.basic_path + 'spider_all_school_score.pkl', "rb"))
        print('正在执行')
        for sch_detail in data_origin:
            try:
                result_detail = sch_detail['result']
                if result_detail is not None:
                    for one_result in result_detail:
                        sch_id = one_result['sch_id']
                        true_data = one_result['enroll_info_list']
                        for one_true_data in true_data:
                            data_kargs = {}
                            data_kargs['academic_year'] = one_true_data['academic_year']
                            data_kargs['wenli'] = one_true_data['wenli']
                            data_kargs['batch'] = one_true_data['batch']
                            data_kargs['batch_name'] = one_true_data['batch_name']
                            data_kargs['diploma_id'] = one_true_data['diploma_id']
                            data_kargs['admission_count'] = one_true_data['admission_count']
                            data_kargs['enroll_plan_count'] = one_true_data['enroll_plan_count']
                            data_kargs['max_score'] = one_true_data['max_score']
                            data_kargs['max_score_diff'] = one_true_data['max_score_diff']
                            data_kargs['max_score_equal'] = one_true_data['max_score_equal']
                            data_kargs['max_score_rank'] = one_true_data['max_score_rank']
                            data_kargs['min_score'] = one_true_data['min_score']
                            data_kargs['min_score_diff'] = one_true_data['min_score_diff']
                            data_kargs['min_score_equal'] = one_true_data['min_score_equal']
                            data_kargs['min_score_rank'] = one_true_data['min_score_rank']
                            data_kargs['avg_score'] = one_true_data['avg_score']
                            data_kargs['avg_score_diff'] = one_true_data['avg_score_diff']
                            data_kargs['avg_score_equal'] = one_true_data['avg_score_equal']
                            data_kargs['avg_score_rank'] = one_true_data['avg_score_rank']
                            school = School.objects.get(sch_id=sch_id)
                            SchoolScore.objects.create(**data_kargs, school=school)
            except KeyError:
                continue

    def university_major_sqlite(self):
        import pickle
        from gaokao.models import School, SchoolMajor
        data_origin = pickle.load(open(self.basic_path + 'spider_all_major_score.pkl', "rb"))
        print('正在执行')
        for sch_detail in data_origin:
            try:
                data_kargs = {}
                sch_id = sch_detail['sch_id']
                data_kargs['wenli'] = sch_detail['wenli']
                data_kargs['academic_year'] = sch_detail['academic_year']
                data_kargs['batch'] = sch_detail['batch']
                data_kargs['batch_name'] = sch_detail['batch_name']
                data_kargs['diploma_id'] = sch_detail['diploma_id']
                result_detail = sch_detail['result']
                if result_detail is not None and type(result_detail) is list:
                    for one_result in result_detail:
                        data_kargs['academic_rule'] = one_result['academic_rule']
                        data_kargs['admission_count'] = one_result['admission_count']
                        data_kargs['avg_score'] = one_result['avg_score']
                        data_kargs['avg_score_diff'] = one_result['avg_score_diff']
                        data_kargs['avg_score_rank'] = one_result['avg_score_rank']
                        data_kargs['enroll_major_code'] = one_result['enroll_major_code']
                        data_kargs['enroll_major_id'] = one_result['enroll_major_id']
                        data_kargs['enroll_major_name'] = one_result['enroll_major_name']
                        data_kargs['enroll_plan_count'] = one_result['enroll_plan_count']
                        data_kargs['max_score'] = one_result['max_score']
                        data_kargs['max_score_diff'] = one_result['max_score_diff']
                        data_kargs['max_score_rank'] = one_result['max_score_rank']
                        data_kargs['min_score'] = one_result['min_score']
                        data_kargs['min_score_diff'] = one_result['min_score_diff']
                        data_kargs['min_score_rank'] = one_result['min_score_rank']
                        data_kargs['tuition'] = one_result['tuition']
                        school = School.objects.get(sch_id=sch_id)
                        SchoolMajor.objects.create(**data_kargs, school=school)
            except KeyError:
                continue



print('执行了么')
dt = DataTraitor()
dt.university_major_sqlite()
