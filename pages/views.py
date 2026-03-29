from django.shortcuts import render
from django.views.generic import View

from fundraisers.models import FundraisingAnnouncement


# Create your views here.
class HomePageView(View):
    template_name = 'pages/index.html'

    def get(self, request):
        recents = FundraisingAnnouncement.objects.filter(is_closed=False).order_by('date')[:4]
        context = {'recents': recents}
        return render(request, self.template_name, context)