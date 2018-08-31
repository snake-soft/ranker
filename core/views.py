from django.shortcuts import render, HttpResponseRedirect
from django.views import View
from datetime import datetime


class StartView(View):
    def get(self, request):
        return render(request, template_name="start.html")


class DateSetView(View):
    def post(self, request):
        frm = datetime.strptime(request.POST['from'], '%Y-%m-%d').date()
        request.session['from'] = frm.strftime('%Y-%m-%d')
        to = datetime.strptime(request.POST['to'], '%Y-%m-%d').date()
        request.session['to'] = to.strftime('%Y-%m-%d')
        nxt = request.POST.get('next', '/')
        import pdb; pdb.set_trace()  # <---------
        return HttpResponseRedirect(nxt)
