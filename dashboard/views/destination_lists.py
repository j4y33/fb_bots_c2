import ast
import json
import random
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.generic.base import View
from dashboard.forms.dst_list_add_from import DestinationAddForm
from datetime import datetime
from dashboard.models import DestinationLists, Groups, CampaignsWhereToPublish, Bots, ToolsDestinationList
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.core.serializers.json import DjangoJSONEncoder

class DestinationView(View):
    model = DestinationLists
    template_name = "components/destination_lists.html"

    def get(self, request, *args, **kwargs):
        groups_model = Groups
        dst_db_view = []
        all_dst = self.model.objects.all()
        for i in all_dst:
            total_groups = 0
            bots = i.profiles
            for bot in bots:
                total_groups += groups_model.objects.filter(bot_id=bot).count()
            dst_db_view.append({'dst_name': i.dst_name,
                                'profiles': len(i.profiles),
                                'groups': total_groups,
                                'campaigns': CampaignsWhereToPublish.objects.filter(dst_lists=i.dst_name).count(),
                                'walls': len(i.walls)})
        return render(request, self.template_name, {'form': dst_db_view})

    def post(self, request, *args, **kwargs):
        print(request.POST)
        if request.POST.get('delete'):
            print(request.POST.get('destination_list_name'))
            self.model.objects.filter(dst_name=request.POST.get('destination_list_name')).delete()
        return HttpResponseRedirect('/destination_lists/')


class DestinationAddView(View):
    form_class = DestinationAddForm
    model = Bots
    groups_model = Groups
    template_name = "components/destination_lists_add.html"

    def get(self, request, *args, **kwargs):

        all_bots = self.model.objects.all()
        tools_model = ToolsDestinationList
        bots_db_view = []
        for i in all_bots:
            bot_groups = []
            groups = self.groups_model.objects.filter(bot_id=i.login).values('group_name')
            tools_dst = tools_model.objects.filter(profiles__contains=[i.login]).values_list('dst_name', flat=True)
            if groups:
                for group in groups:
                    bot_groups.append(group['group_name'])
            bots_db_view.append({'login': i.login,
                                 'vpn': i.vpn_provider,
                                 'region': i.vpn_region,
                                 'bot_dst_groups': list(tools_dst),
                                 'bot_groups': bot_groups,
                                 'friends': random.randint(50, 1000),
                                 'groups_length': len(bot_groups)})
        form = self.form_class()
        return render(request, self.template_name, {'all_bots': bots_db_view, 'form': form})

# Server side - not used
    def _datatables(self, request):
        print(request.POST)
        print(request.POST.get("data"))
        datatables = request.POST
        # Ambil draw
        draw = int(datatables.get('draw'))
        # Ambil start
        start = int(datatables.get('start'))
        # Ambil length (limit)
        length = int(datatables.get('length'))
        # Ambil data search
        search = datatables.get('search[value]')
        # Set record total
        records_total = self.model.objects.all().exclude(
            Q(login=None) | Q(vpn_provider=None)).count()
        # Set records filtered
        records_filtered = records_total
        # Ambil semua invoice yang valid
        bots = self.model.objects.all().exclude(Q(login=None) | Q(vpn_provider=None)).order_by('-creation_date')

        if search:
            bots = self.model.objects.filter(
                Q(login=search) |
                Q(vpn_provider=search)
            ).order_by('-creation_date')
            records_total = bots.count()
            records_filtered = records_total

        # Atur paginator
        paginator = Paginator(bots, length)

        try:
            object_list = paginator.page(draw).object_list
        except PageNotAnInteger:
            object_list = paginator.page(draw).object_list
        except EmptyPage:
            object_list = paginator.page(paginator.num_pages).object_list
        data = [
            {
                'login': inv.login
            } for inv in object_list
        ]

        return {
            'draw': draw,
            'recordsTotal': records_total,
            'recordsFiltered': records_filtered,
            'data': data,
        }

    def post(self, request, *args, **kwargs):
        #invoices = self._datatables(request)
        #return HttpResponse(json.dumps(invoices, cls=DjangoJSONEncoder), content_type='application/json')
        #datatables = request.POST
        print(request.POST)
        form = self.form_class(request.POST)
        if request.is_ajax():
            if request.POST.get("checked[]"):
                print('Update DB')
                print(request.POST.get("checked[]"))
                all_bot_groups = self.groups_model.objects.filter(bot_id=request.POST.get("bot_id"))
                for group in all_bot_groups:
                    group.dst_select_status = False
                    group.save()
                selected_groups = request.POST.getlist("checked[]")
                for group in selected_groups:
                    t = self.groups_model.objects.get(id=group)
                    t.dst_select_status = True
                    t.save()
                return JsonResponse(data=None, safe=False)
            elif request.POST.get("checked") == '':
                all_bot_groups = self.groups_model.objects.filter(bot_id=request.POST.get("bot_id"))
                for group in all_bot_groups:
                    group.dst_select_status = False
                    group.save()
            data = list(self.groups_model.objects.filter(bot_id=request.POST.get("bot_id")).values())
            return JsonResponse(data, safe=False)

        if request.POST.get("botId"):
            # Process modal from with BotId
            print(request.POST.get("botId"))
            return HttpResponseRedirect('/destination_lists/add')
        if form.is_valid():
            if request.POST.getlist("total_id"):
                bot_walls = []
                bot_comment = []
                selected_bots = request.POST.get("total_id").split(',')
                walls = request.POST.get("total_walls").split(',')
                comment = request.POST.get("total_comments").split(',')
                for i in selected_bots:
                    if i not in walls:
                        bot_walls.append(i)
                    if i not in comment:
                        bot_comment.append(i)
                destination_lists = DestinationLists(dst_name=request.POST.get('dst_name'),
                                                     profiles=selected_bots,
                                                     campaigns='{}',
                                                     walls=bot_walls,
                                                     comment=bot_comment,
                                                     date=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                destination_lists.save()
                return HttpResponseRedirect('/destination_lists/')
            else:
                from django.contrib import messages
                messages.error(request, 'Error: please select bot/bots')
                return HttpResponseRedirect('/destination_lists/add')
