import random

from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render
from django.views import View
from datetime import datetime
from datetime import timedelta

from dashboard.models import Bots, ToolsAccountActions, ToolsDestinationList, Action, Errors, Tracks, Logs
from scheduler.launcher import InstancesLauncher


class ActivityView(View):
    model = Tracks
    bot_model = Bots
    logs_model = Logs
    launcher = InstancesLauncher()
    tools_model = ToolsDestinationList
    template_name = "components/activity.html"

    # If no errors show green progress bar
    # if errors show red
    # if finish show blue
    def get(self, request, *args, **kwargs):
        # progress-bar-success
        # progress-bar-info
        # progress-bar-warning
        # progress-bar-danger
        if request.is_ajax():
            if request.GET.get('logs'):
                bot = request.GET.get('bot_id')
                time_threshold = datetime.now() - timedelta(hours=1)
                #, date__lt=time_threshold
                results = self.logs_model.objects.filter(bot_id=bot).order_by('-id')
                logs = []
                for i in results:
                    logs.append(i.log)
                print(logs)
                return JsonResponse(logs, safe=False)
            elif request.GET.get('actions'):
                all_actions = []
                all_errors = []
                bot = request.GET.get('bot_id')
                last_login_date = Action.objects.filter(bot_id=bot, action_id='login').order_by('-id')
                if last_login_date:
                    last_login_date = last_login_date[0]
                    print('Bot: {0}, last login: {1}'.format(bot, last_login_date.date))
                    all_actions = Action.objects.filter(bot_id=bot).filter(Q(date__gte=last_login_date.date))
                    all_errors = Errors.objects.filter(bot_id=bot).filter(Q(date__gte=last_login_date.date))
                actions = []
                for action in all_actions:
                    if action.action_id != 'none':
                        actions.append({
                            'action_id': action.action_id,
                            'action_date': action.date.strftime('%Y-%m-%d %H:%M:%S')
                        })
                return JsonResponse(actions, safe=False)
            else:
                print('Get ajax')
                # Get all running bots
                track = {}
                all_bots = list(self.model.objects.order_by('bot_id').values('bot_id').distinct())
                bots_ids = []
                for i in all_bots:
                    bots_ids.append(i['bot_id'])
                form = {'all_bots': bots_ids, 'tracks': []}
                for bot in bots_ids:
                    print(bot)
                    login = self.bot_model.objects.get(login=bot)
                    latest_track = self.model.objects.filter(bot_id=bot).latest('id')
                    form['tracks'].append({
                        'bot_id': bot,
                        'bot_name': '{0} {1}'.format(login.bot_first_name, login.bot_last_name),
                        'progress': latest_track.running_percent
                    })
                print(form)
                return JsonResponse(form, safe=False)

        # Get all running bots
        # Require bot used status- running/pending
        all_running_bots = self.bot_model.objects.filter(used_status=True)
        form = []
        for bot in all_running_bots:
            latest_track = self.model.objects.filter(bot_id=bot.login).order_by('-id')
            if latest_track:
                form.append({
                    'bot_id': bot.login,
                    'bot_name': '{0} {1}'.format(bot.bot_first_name, bot.bot_last_name),
                    'progress': latest_track[0].track[-1][1]
                })
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        print('Terminate command')
        bot = self.bot_model.objects.get(login=request.POST.get('bot_id'))
        #self.model.objects.filter(bot_id=request.POST.get('bot_id')).delete()
        tools_dst = self.tools_model.objects.filter(running__contains=[request.POST.get('bot_id')])
        for dst in tools_dst:
            dst.running.remove(request.POST.get('bot_id'))
            dst.save()
        self.bot_model.objects.filter(login=request.POST.get('bot_id')).update(used_status=False)
        self.launcher.terminate_instance(bot.instance_id)
        return HttpResponse('Terminated')
