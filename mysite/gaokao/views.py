from django.shortcuts import get_object_or_404, render
from .models import Major, School
from django.http import HttpResponse
from django.core import serializers
import json
from django.http import JsonResponse


# Create your views here.

# Create your views here.
def index(request):
    name = request.POST.get('name')
    school_list = School.objects.get(school_name=name)
    # result = serializers.serialize('json', school_list)
    return HttpResponse(str(school_list), content_type="application/json")  # 返回json数据


def detail(request, question_id):
    major_list = get_object_or_404(School, pk=question_id)
    return render(request, 'polls/detail.html', {'major_list': major_list})
