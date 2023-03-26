from django.views.generic import TemplateView
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from dashboard.models import Bots, ToolsDestinationList, Action
from scheduler.launcher import InstancesLauncher


class SocialView(TemplateView):
    model = Bots
    tools_model = ToolsDestinationList
    launcher = InstancesLauncher()
    template_name = "components/social_profiles.html"

    def get(self, request, *args, **kwargs):
        all_bots = self.model.objects.all()
        action_model = Action
        bots_db_view = []
        for i in all_bots:
            tools_dst = self.tools_model.objects.filter(profiles__contains=[i.login]).values_list('dst_name', flat=True)
            act = None
            try:
                act = action_model.objects.filter(bot_id=i.login).order_by('-id')[0]
                act = act.date
            except:
                pass
            # Check if bot running status
            bots_db_view.append({'bot_name': '{0} {1}'.format(i.bot_first_name, i.bot_last_name),
                                 'bot_id': i.login,
                                 'last_action': act,
                                 'running': i.used_status,
                                 'bot_dst': list(tools_dst)})
        return render(request, self.template_name, {'form': bots_db_view})

    def post(self, request, *args, **kwargs):
        # Update bot running status
        bot = self.model.objects.get(login=request.POST.get('bot_id'))
        if bot.total_errors > 1000:
            print('Bot blocked')
            return HttpResponse('Bot blocked')
        else:
            tools_dst = self.tools_model.objects.filter(profiles__contains=[request.POST.get('bot_id')])
            for dst in tools_dst:
                try:
                    dst.running.append(request.POST.get('bot_id'))
                except:
                    dst.running = [request.POST.get('bot_id')]
                dst.save()
            self.model.objects.filter(login=request.POST.get('bot_id')).update(used_status=True)
            self.launcher.launch_instance(request.POST.get('bot_id'))
            return HttpResponse('Launched Successfully')