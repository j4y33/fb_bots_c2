import random

from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render
from django.views import View
from datetime import datetime
from datetime import timedelta

from dashboard.models import Bots, ToolsAccountActions, ToolsDestinationList, Action, Errors
from scheduler.launcher import InstancesLauncher


class CloudView(View):
    model = Bots
    launcher = InstancesLauncher()
    template_name = "components/cloud.html"

    def get(self, request, *args, **kwargs):
        bot_instance = []
        instances = self.launcher.describe_instances()
        for i in instances:
            print(i)
            bot = self.model.objects.filter(instance_id=i.id)
            if bot:
                bot_instance.append({'instance_id': i.id,
                                     'local_ip': bot[0].local_ip,
                                     'bot_name': '{0} {1}'.format(bot[0].bot_first_name, bot[0].bot_last_name)})
            else:
                bot_instance.append({'instance_id': i.id,
                                     'local_ip': 'waiting...',
                                     'bot_name': 'Starting/Already off'})
        return render(request, self.template_name, {'form': bot_instance})

    def post(self, request, *args, **kwargs):
        print('Terminate command')
        self.launcher.terminate_instance(request.POST.get('instance_id'))
        return HttpResponse('Terminated')
