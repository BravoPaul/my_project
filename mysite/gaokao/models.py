from django.db import models


# Create your models here.


# Create your models here.

class School(models.Model):
    sch_id = models.CharField(max_length=200, primary_key=True, default='-1', unique=True)
    diploma_desc = models.CharField(max_length=200, null=True, blank=True)
    grad_desc = models.CharField(max_length=200, null=True, blank=True)
    independent_desc = models.CharField(max_length=200, null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    province = models.CharField(max_length=200, null=True, blank=True)
    sch_competent_desc = models.CharField(max_length=200, null=True, blank=True)
    sch_create_time = models.CharField(max_length=200, null=True, blank=True)
    sch_english_name = models.CharField(max_length=200, null=True, blank=True)
    sch_logo = models.ImageField(null=True, blank=True)
    sch_name = models.CharField(max_length=200, null=True, blank=True)
    sch_run_type = models.CharField(max_length=200, null=True, blank=True)
    sch_run_type_desc = models.CharField(max_length=200, null=True, blank=True)
    sch_tags = models.CharField(max_length=200, null=True, blank=True)
    sch_type_desc = models.CharField(max_length=200, null=True, blank=True)
    sch_type_tag_desc = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.sch_id + '_' + self.sch_name + '_' + self.location


class SchoolDetail(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    canteen_desc = models.TextField(null=True, blank=True)
    sch_address = models.TextField(max_length=200, null=True, blank=True)
    sch_fellowship = models.TextField(max_length=200, null=True, blank=True)
    sch_intro = models.TextField(max_length=200, null=True, blank=True)
    sch_scholarship = models.TextField(max_length=200, null=True, blank=True)
    sch_tel_num = models.CharField(max_length=200, null=True, blank=True)
    sch_web_url = models.CharField(max_length=200, null=True, blank=True)
    stu_dorm_desc = models.CharField(max_length=200, null=True, blank=True)
    sch_master_ratio = models.FloatField(null=True, blank=True)
    sch_abroad_ratio = models.FloatField(null=True, blank=True)


class SchoolRank(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    rank_type_desc = models.CharField(max_length=200, null=True, blank=True)
    rank_year = models.IntegerField(null=True, blank=True)
    rank_idx = models.IntegerField(null=True, blank=True)
    rank_score = models.FloatField(null=True, blank=True)
    rank_type = models.CharField(max_length=200, null=True, blank=True)
    world_rank_idx = models.IntegerField(null=True, blank=True)


class SchoolFamous(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    celebrity_name = models.CharField(max_length=200, null=True, blank=True)
    celebrity_desc = models.CharField(max_length=200, null=True, blank=True)


class SchoolScore(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    # 条件
    academic_year = models.CharField(max_length=200, default='')
    wenli = models.CharField(max_length=200, default='')
    batch = models.CharField(max_length=200, default='')
    batch_name = models.CharField(max_length=200, default='')
    diploma_id = models.CharField(max_length=200, default='')
    # 信息
    admission_count = models.CharField(max_length=200, null=True, blank=True)
    enroll_plan_count = models.CharField(max_length=200, null=True, blank=True)
    max_score = models.CharField(max_length=200, null=True, blank=True)
    max_score_diff = models.CharField(max_length=200, null=True, blank=True)
    max_score_equal = models.CharField(max_length=200, null=True, blank=True)
    max_score_rank = models.CharField(max_length=200, null=True, blank=True)
    min_score = models.CharField(max_length=200, null=True, blank=True)
    min_score_diff = models.CharField(max_length=200, null=True, blank=True)
    min_score_equal = models.CharField(max_length=200, null=True, blank=True)
    min_score_rank = models.CharField(max_length=200, null=True, blank=True)
    avg_score = models.CharField(max_length=200, null=True, blank=True)
    avg_score_diff = models.CharField(max_length=200, null=True, blank=True)
    avg_score_equal = models.CharField(max_length=200, null=True, blank=True)
    avg_score_rank = models.CharField(max_length=200, null=True, blank=True)


class SchoolMajor(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    # 条件
    wenli = models.CharField(max_length=200, default='')
    academic_year = models.CharField(max_length=200, default='')
    batch = models.CharField(max_length=200, default='')
    batch_name = models.CharField(max_length=200, default='')
    diploma_id = models.CharField(max_length=200, default='')
    # 信息
    academic_rule = models.CharField(max_length=200, null=True, blank=True)
    admission_count = models.CharField(max_length=200, null=True, blank=True)
    avg_score = models.CharField(max_length=200, null=True, blank=True)
    avg_score_diff = models.CharField(max_length=200, null=True, blank=True)
    avg_score_rank = models.CharField(max_length=200, null=True, blank=True)
    enroll_major_code = models.CharField(max_length=200, null=True, blank=True)
    enroll_major_id = models.CharField(max_length=200, null=True, blank=True)
    enroll_major_name = models.CharField(max_length=200, null=True, blank=True)
    enroll_plan_count = models.CharField(max_length=200, null=True, blank=True)
    max_score = models.CharField(max_length=200, null=True, blank=True)
    max_score_diff = models.CharField(max_length=200, null=True, blank=True)
    max_score_rank = models.CharField(max_length=200, null=True, blank=True)
    min_score = models.CharField(max_length=200, null=True, blank=True)
    min_score_diff = models.CharField(max_length=200, null=True, blank=True)
    min_score_rank = models.CharField(max_length=200, null=True, blank=True)
    tuition = models.CharField(max_length=200, null=True, blank=True)


class Major(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    major_name = models.CharField(max_length=200)

    def __str__(self):
        return self.major_name
