from django.shortcuts import get_object_or_404, render
from .models import School
from django.http import HttpResponse
from django.core import serializers
from itertools import chain
import json
from django.http import JsonResponse


# Create your views here.

# Create your views here.
def index(request):
    page_num_ex = int(request.POST.get('page_num_ex'))
    page_num_post = int(request.POST.get('page_num_post'))
    school_list = School.objects.all()[page_num_ex * 30:page_num_post * 30]
    result = serializers.serialize('json', school_list)
    return HttpResponse(result, content_type="application/json")


def detail(request):
    sch_id = request.POST.get('sch_id')
    school_intro = School.objects.get(sch_id=sch_id)
    school_detail = school_intro.schooldetail_set.all()
    school_rank = school_intro.schoolrank_set.all()
    school_famous = school_intro.schoolfamous_set.all()
    school_score = school_intro.schoolscore_set.all()
    school_major = school_intro.schoolmajor_set.all()
    school_intro = [school_intro]
    result_list = chain(school_intro, school_detail, school_rank, school_famous,school_score,school_major)
    result_final = serializers.serialize('json', result_list)
    return HttpResponse(result_final, content_type="application/json", charset='utf-8')


# def score(request):
#     sch_id = request.POST.get('sch_id')
#     school_intro = School.objects.get(sch_id=sch_id)
#     school_score = school_intro.schoolscore_set.all()
#     result_final = serializers.serialize('json', school_score)
#     return HttpResponse(result_final, content_type="application/json", charset='utf-8')
