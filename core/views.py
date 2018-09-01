from django.shortcuts import render, HttpResponseRedirect
from django.views import View
from datetime import datetime, timedelta

from .forms import TimeRangeForm


class StartView(View):
    def get(self, request):
        return render(request, template_name="start.html")


class DateSetView(View):  # Form Validation MISSING!!!
    def post(self, request):
        frm = datetime.strptime(request.POST['from'], '%Y-%m-%d').date()
        request.session['from'] = frm.strftime('%Y-%m-%d')
        to = datetime.strptime(request.POST['to'], '%Y-%m-%d').date()
        request.session['to'] = to.strftime('%Y-%m-%d')
        nxt = request.POST.get('next', '/')
        return HttpResponseRedirect(nxt)
