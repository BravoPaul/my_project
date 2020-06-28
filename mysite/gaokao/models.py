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


class Major(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    major_name = models.CharField(max_length=200)

    def __str__(self):
        return self.major_name
