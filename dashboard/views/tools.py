import ast
from datetime import datetime
from urllib.parse import urlencode

import urllib3
from proxy.views import proxy_view
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from revproxy.views import ProxyView

from dashboard.forms.tools_account_actions import ToolsAccountActionForm
from dashboard.forms.tools_comments_settings import ToolsCommentsSettingsForm
from dashboard.forms.tools_comments_sources import ToolsCommentsSourcesForm
from dashboard.forms.tools_create_new_bot_group_from import ToolsCreateGroupForm
from dashboard.forms.tools_extract_members import ToolsExtractMembersForm
from dashboard.forms.tools_find_fiends import ToolsFindFriendsForm
from dashboard.forms.tools_find_groups import ToolsFindGroupsForm
from dashboard.forms.tools_find_pages import ToolsFindPagesForm
from dashboard.forms.tools_joiner import ToolsJoinerForm
from dashboard.forms.tools_use_members import ToolsUseMembersForm
from dashboard.models import Bots, CommentsSettings, CommentsSources, CommentsResults, ToolsFindGroups, \
    ToolsExtractedGroups, ToolsJoiner, ToolsDestinationList, Groups, ToolsFindPages, ToolsExtractedFriends, \
    ToolsFindFriends, ToolsExtractedPages, DestinationLists, ToolsAccountActions


class ToolsView(View):
    model = ToolsDestinationList
    template_name = "components/tools.html"

    def get(self, request, *args, **kwargs):
        all_dst = self.model.objects.all()
        return render(request, self.template_name, {'form': all_dst})

    def post(self, request, *args, **kwargs):
        print(request.POST)
        if request.is_ajax():
            data = []
            dst_id = request.POST.get("dst_id")
            dst = self.model.objects.filter(id=dst_id).values()
            for running in dst[0].get('running'):
                ip = Bots.objects.filter(login=running).values('local_ip')
                bot = {'bot_id': running, 'ip': ip[0].get('local_ip'), 'link': 'http://localhost:6080/vnc.html?host=localhost&port=6080'}
                data.append(bot)
            return JsonResponse(data, safe=False)

        if request.POST.get('delete'):
            print(request.POST.get('destination_list_name'))
            self.model.objects.filter(dst_name=request.POST.get('destination_list_name')).delete()
        return HttpResponseRedirect('/tools/')


class ToolsCreateBotsGroupView(View):
    form_class = ToolsCreateGroupForm
    model = Bots
    template_name = "components/tools/tools_create_new_bot_group.html"

    def get(self, request, *args, **kwargs):
        all_bots = self.model.objects.all()
        dst_model = DestinationLists
        bots_db_view = []
        for i in all_bots:
            dst = dst_model.objects.filter(profiles__contains=[i.login]).values_list('dst_name', flat=True)
            bots_db_view.append({'login': i.login,
                                 'name': '{0} {1}'.format(i.bot_first_name, i.bot_last_name),
                                 'vpn': i.vpn_provider,
                                 'region': i.vpn_region,
                                 'bot_dst': list(dst)})
        return render(request, self.template_name, {'bots': bots_db_view,
                                                    'form': self.form_class})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            if request.POST.getlist("total_id"):
                selected_bots = request.POST.get("total_id").split(',')
                destination_lists = ToolsDestinationList(dst_name=request.POST.get('group_name'),
                                                         profiles=selected_bots,
                                                         running='{}',
                                                         extraction='{}',
                                                         date=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                destination_lists.save()
                return HttpResponseRedirect('/tools/')
            else:
                from django.contrib import messages
                messages.error(request, 'Error: please select bot/bots')
                return HttpResponseRedirect('/tools/create_bots_group')


class ToolsBaseView(View):
    template_name = "components/tools/tools_base.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'dst_id': request.GET.get('dst_id')})


class ToolsFinderView(View):
    template_name = "components/tools/tools_finder.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'dst_id': request.GET.get('dst_id')})


# Finder
class ToolsFinderFindGroupsView(View):
    form_class = ToolsFindGroupsForm
    template_name = "components/tools/tools_finder_find_groups.html"

    def get(self, request, *args, **kwargs):
        extracted_groups = ToolsExtractedGroups.objects.filter(dst_id=request.GET.get('dst_id'))
        dst_list = ToolsDestinationList.objects.get(id=request.GET.get('dst_id'))
        return render(request, self.template_name, {'dst_id': request.GET.get('dst_id'),
                                                    'dst_name': dst_list.dst_name,
                                                    'total_bots': len(dst_list.profiles),
                                                    'form': self.form_class(dst_id=request.GET.get('dst_id')),
                                                    'extracted_groups': extracted_groups})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, dst_id=None)
        if form.is_valid():
            if request.POST.get('dst_id') is not None:
                tools_find_groups, created = ToolsFindGroups.objects.get_or_create(dst_id=request.POST.get('dst_id'))
                tools_find_groups.dst_id = request.POST.get('dst_id')
                tools_find_groups.keywords = [form.cleaned_data['keywords']]
                tools_find_groups.exclude_keywords = [form.cleaned_data['exclude_keywords']]
                tools_find_groups.groups_extra_urls = request.POST.get('groups_extra_urls').splitlines()
                tools_find_groups.min_users = form.cleaned_data['min_users']
                tools_find_groups.en_gr_groups = form.cleaned_data['en_gr_groups']
                tools_find_groups.opened_groups = form.cleaned_data['opened_groups']
                tools_find_groups.admin_post = form.cleaned_data['admin_post']
                tools_find_groups.min_users_count = form.cleaned_data['min_users_count']
                tools_find_groups.status = False
                tools_find_groups.date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                tools_find_groups.save()
        return HttpResponseRedirect('/tools/finder/find_groups?dst_id={0}'.format(request.POST.get('dst_id')))


class ToolsFinderFindPagesView(View):
    form_class = ToolsFindPagesForm
    template_name = "components/tools/tools_finder_find_pages.html"

    def get(self, request, *args, **kwargs):
        extracted_pages = ToolsExtractedPages.objects.filter(dst_id=request.GET.get('dst_id'))
        dst_list = ToolsDestinationList.objects.get(id=request.GET.get('dst_id'))
        return render(request, self.template_name, {'dst_id': request.GET.get('dst_id'),
                                                    'dst_name': dst_list.dst_name,
                                                    'total_bots': len(dst_list.profiles),
                                                    'form': self.form_class(dst_id=request.GET.get('dst_id')),
                                                    'extracted_pages': extracted_pages})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, dst_id=None)
        if form.is_valid():
            if request.POST.get('dst_id') is not None:
                tools_find_pages, created = ToolsFindPages.objects.get_or_create(dst_id=request.POST.get('dst_id'))
                tools_find_pages.dst_id = request.POST.get('dst_id')
                tools_find_pages.keywords = [form.cleaned_data['keywords']]
                tools_find_pages.exclude_keywords = [form.cleaned_data['exclude_keywords']]
                tools_find_pages.pages_extra_urls = [form.cleaned_data['pages_extra_urls']]
                tools_find_pages.min_likes = form.cleaned_data['min_likes']
                tools_find_pages.en_gr_pages = form.cleaned_data['en_gr_pages']
                tools_find_pages.min_likes_count = form.cleaned_data['min_likes_count']
                tools_find_pages.status = False
                tools_find_pages.date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                tools_find_pages.save()
        return HttpResponseRedirect('/tools/finder/find_pages?dst_id={0}'.format(request.POST.get('dst_id')))


class ToolsFinderFindFriendsView(View):
    form_class = ToolsFindFriendsForm
    template_name = "components/tools/tools_finder_find_friends.html"

    def get(self, request, *args, **kwargs):
        extracted_friends = ToolsExtractedFriends.objects.filter(dst_id=request.GET.get('dst_id'))
        dst_list = ToolsDestinationList.objects.get(id=request.GET.get('dst_id'))
        return render(request, self.template_name, {'dst_id': request.GET.get('dst_id'),
                                                    'dst_name': dst_list.dst_name,
                                                    'total_bots': len(dst_list.profiles),
                                                    'form': self.form_class(dst_id=request.GET.get('dst_id')),
                                                    'extracted_friends': extracted_friends})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, dst_id=None)
        if form.is_valid():
            if request.POST.get('dst_id') is not None:
                tools_find_friends, created = ToolsFindFriends.objects.get_or_create(dst_id=request.POST.get('dst_id'))
                tools_find_friends.dst_id = request.POST.get('dst_id')
                tools_find_friends.keywords = [form.cleaned_data['keywords']]
                tools_find_friends.exclude_keywords = [form.cleaned_data['exclude_keywords']]
                tools_find_friends.friends_extra_urls = [form.cleaned_data['friends_extra_urls']]
                tools_find_friends.min_mutual = form.cleaned_data['min_mutual']
                tools_find_friends.en_gr_friends = form.cleaned_data['en_gr_friends']
                tools_find_friends.opened_friends = form.cleaned_data['opened_friends']
                tools_find_friends.min_mutual_count = form.cleaned_data['min_mutual_count']
                tools_find_friends.status = False
                tools_find_friends.date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                tools_find_friends.save()
        return HttpResponseRedirect('/tools/finder/find_friends?dst_id={0}'.format(request.POST.get('dst_id')))


# Finder


class ToolsJoinerView(View):
    form_class = ToolsJoinerForm
    template_name = "components/tools/tools_joiner.html"

    def get(self, request, *args, **kwargs):
        print(request.GET.get('dst_id'))
        form_class = ToolsJoinerForm(dst_id=request.GET.get('dst_id'))
        dst_list = ToolsDestinationList.objects.get(id=request.GET.get('dst_id'))
        extracted_groups = ToolsExtractedGroups.objects.filter(dst_id=request.GET.get('dst_id'))
        return render(request, self.template_name, {'dst_id': request.GET.get('dst_id'),
                                                    'total_bots': len(dst_list.profiles),
                                                    'dst_name': dst_list.dst_name,
                                                    'extracted_groups': extracted_groups,
                                                    'form': form_class})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, dst_id=None)
        if request.is_ajax():
            data = []
            bots = request.POST.getlist("bot_ids")
            url = request.POST.get("group_url")
            if bots:
                print(url)
                for bot in ast.literal_eval(bots[0]):
                    print(bot)
                    bot_group = Groups.objects.filter(bot_id=bot, link=url).values()
                    data.append(bot_group[0])
            return JsonResponse(data, safe=False)
        if form.is_valid():
            print('From valid')
            print(request.POST.get('dst_id'))
            operate_on = []
            week = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']
            for i in week:
                if i in request.POST:
                    operate_on.append(i)
            bot_joiner, created = ToolsJoiner.objects.get_or_create(dst_id=request.POST.get('dst_id'))
            bot_joiner.wait_between = form.cleaned_data['wait_between']
            bot_joiner.wait_between_and = form.cleaned_data['wait_between_and']
            bot_joiner.execute_between = form.cleaned_data['execute_between']
            bot_joiner.execute_between_and = form.cleaned_data['execute_between_and']
            bot_joiner.random_sleep_time = form.cleaned_data['random_sleep_time']
            bot_joiner.join_between = form.cleaned_data['join_between']
            bot_joiner.join_between_and = form.cleaned_data['join_between_and']
            bot_joiner.auto_stop = form.cleaned_data['auto_stop']
            bot_joiner.reaching_groups = form.cleaned_data['reaching_groups']
            bot_joiner.join_between_peer_day = form.cleaned_data['join_between_peer_day']
            bot_joiner.join_between_and_peer_day = form.cleaned_data['join_between_and_peer_day']
            bot_joiner.auto_stop_peer_day = form.cleaned_data['auto_stop_peer_day']
            bot_joiner.reaching_groups_peer_day = form.cleaned_data['reaching_groups_peer_day']
            bot_joiner.operate_on = operate_on
            bot_joiner.date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            bot_joiner.save()
        return HttpResponseRedirect('/tools/joiner?dst_id={0}'.format(request.POST.get('dst_id')))


class ToolsJoinerShowGroupsView(View):
    form_class = ToolsJoinerForm
    template_name = "components/tools/tools_joiner_show_groups.html"

    def get(self, request, *args, **kwargs):
        print(request.GET.get('dst_id'))
        form_class = ToolsJoinerForm(dst_id=request.GET.get('dst_id'))
        dst_list = ToolsDestinationList.objects.get(id=request.GET.get('dst_id'))
        extracted_groups = ToolsExtractedGroups.objects.filter(dst_id=request.GET.get('dst_id'))
        return render(request, self.template_name, {'dst_id': request.GET.get('dst_id'),
                                                    'total_bots': len(dst_list.profiles),
                                                    'dst_name': dst_list.dst_name,
                                                    'extracted_groups': extracted_groups,
                                                    'form': form_class})


class ToolsJoinerShowPagesView(View):
    form_class = ToolsJoinerForm
    template_name = "components/tools/tools_joiner_show_pages.html"

    def get(self, request, *args, **kwargs):
        print(request.GET.get('dst_id'))
        form_class = ToolsJoinerForm(dst_id=request.GET.get('dst_id'))
        dst_list = ToolsDestinationList.objects.get(id=request.GET.get('dst_id'))
        extracted_pages = ToolsExtractedPages.objects.filter(dst_id=request.GET.get('dst_id'))
        return render(request, self.template_name, {'dst_id': request.GET.get('dst_id'),
                                                    'total_bots': len(dst_list.profiles),
                                                    'dst_name': dst_list.dst_name,
                                                    'extracted_pages': extracted_pages,
                                                    'form': form_class})


class ToolsCommentsView(View):
    template_name = "components/tools/tools_comments.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'dst_id': request.GET.get('dst_id')})


class ToolsCommentsSettingsView(View):
    model = CommentsSettings
    template_name = "components/tools/tools_comments_settings.html"

    def get(self, request, *args, **kwargs):
        form_class = ToolsCommentsSettingsForm(dst_id=request.GET.get('dst_id'))
        return render(request, self.template_name, {'dst_id': request.GET.get('dst_id'), 'form': form_class})

    def post(self, request, *args, **kwargs):
        if request.POST.get('confirm') is not None:
            form = ToolsCommentsSettingsForm(request.POST, dst_id=request.GET.get('dst_id'))
            operate_on = []
            week = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']
            for i in week:
                if i in request.POST:
                    operate_on.append(i)
            if form.is_valid():
                on_off = False
                random_sleep_time = False
                rotate_weekends_randomly = False
                maximum_single_source_per_day = False
                comments_post_maximum_age = False
                if request.POST.get('on_off') is not None:
                    on_off = True
                if request.POST.get('random_sleep_time') is not None:
                    random_sleep_time = True
                if request.POST.get('rotate_weekends_randomly') is not None:
                    rotate_weekends_randomly = True
                if request.POST.get('maximum_single_source_per_day') is not None:
                    maximum_single_source_per_day = True
                if request.POST.get('comments_post_maximum_age') is not None:
                    comments_post_maximum_age = True
                wait_between_start = 0
                if request.POST.get('wait_between_start'):
                    wait_between_start = request.POST.get('wait_between_start')
                wait_between_end = 0
                if request.POST.get('wait_between_end'):
                    wait_between_end = request.POST.get('wait_between_end')
                comments_maximum_start = 0
                if request.POST.get('comments_maximum_start'):
                    comments_maximum_start = request.POST.get('comments_maximum_start')
                comments_maximum_end = 0
                if request.POST.get('comments_maximum_end'):
                    comments_maximum_end = request.POST.get('comments_maximum_end')
                comments_increasing_start = 0
                if request.POST.get('comments_increasing_start'):
                    comments_increasing_start = request.POST.get('comments_increasing_start')
                comments_increasing_end = 0
                if request.POST.get('comments_increasing_end'):
                    comments_increasing_end = request.POST.get('comments_increasing_end')
                comments_single_source_maximum_start = 0
                if request.POST.get('comments_single_source_maximum_start'):
                    comments_single_source_maximum_start = request.POST.get('comments_single_source_maximum_start')
                comments_single_source_maximum_end = 0
                if request.POST.get('comments_single_source_maximum_end'):
                    comments_single_source_maximum_end = request.POST.get('comments_single_source_maximum_end')
                comments_maximum_days = 0
                if request.POST.get('comments_maximum_days'):
                    comments_maximum_days = request.POST.get('comments_maximum_days')
                execute_between_start = None
                if request.POST.get('execute_between_start'):
                    execute_between_start = request.POST.get('execute_between_start')
                execute_between_end = None
                if request.POST.get('execute_between_end'):
                    execute_between_end = request.POST.get('execute_between_end')
                comment = None
                if request.POST.get('comment'):
                    comment = request.POST.get('comment')
                keywords = None
                if request.POST.get('keywords'):
                    keywords = request.POST.get('keywords').split(',')
                exclude = None
                if request.POST.get('exclude'):
                    exclude = request.POST.get('exclude').split(',')
                try:
                    post = self.model.objects.get(dst_id=request.POST.get('dst_id'))
                    post.wait_between_start = wait_between_start
                    post.wait_between_end = wait_between_end
                    post.comments_maximum_start = comments_maximum_start
                    post.comments_maximum_end = comments_maximum_end
                    post.comments_increasing_start = comments_increasing_start
                    post.comments_increasing_end = comments_increasing_end
                    post.comments_single_source_maximum_start = comments_single_source_maximum_start
                    post.comments_single_source_maximum_end = comments_single_source_maximum_end
                    post.comments_maximum_days = comments_maximum_days
                    post.execute_between_start = execute_between_start
                    post.execute_between_end = execute_between_end
                    post.comment = comment
                    post.keywords = keywords
                    post.exclude = exclude
                    post.on_off = on_off
                    post.random_sleep_time = random_sleep_time
                    post.rotate_weekends_randomly = rotate_weekends_randomly
                    post.maximum_single_source_per_day = maximum_single_source_per_day
                    post.comments_post_maximum_age = comments_post_maximum_age
                    post.operate_on = operate_on
                    post.date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    post.save()
                except self.model.DoesNotExist:
                    post = self.model(
                        dst_id=request.POST.get('dst_id'),
                        on_off=on_off,
                        wait_between_start=wait_between_start,
                        wait_between_end=wait_between_end,
                        execute_between_start=execute_between_start,
                        execute_between_end=execute_between_end,
                        random_sleep_time=random_sleep_time,
                        rotate_weekends_randomly=rotate_weekends_randomly,
                        operate_on=operate_on,
                        comments_maximum_start=comments_maximum_start,
                        comments_maximum_end=comments_maximum_end,
                        comments_increasing_start=comments_increasing_start,
                        comments_increasing_end=comments_increasing_end,
                        maximum_single_source_per_day=maximum_single_source_per_day,
                        comments_single_source_maximum_start=comments_single_source_maximum_start,
                        comments_single_source_maximum_end=comments_single_source_maximum_end,
                        comments_post_maximum_age=comments_post_maximum_age,
                        comments_maximum_days=comments_maximum_days,
                        keywords=keywords,
                        exclude=exclude,
                        comment=comment,
                        date=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                    post.save()
        return HttpResponseRedirect('/tools/comments/settings?dst_id={0}'.format(request.POST.get('dst_id')))


class ToolsCommentsSourcesView(View):
    model = CommentsSources
    template_name = "components/tools/tools_comments_sources.html"

    def get(self, request, *args, **kwargs):
        form_class = ToolsCommentsSourcesForm(dst_id=request.GET.get('dst_id'))
        return render(request, self.template_name, {'dst_id': request.GET.get('dst_id'), 'form': form_class})

    def post(self, request, *args, **kwargs):
        if request.POST.get('confirm') is not None:
            form = ToolsCommentsSourcesForm(request.POST, dst_id=request.GET.get('dst_id'))
            operate_on = []
            week = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']
            for i in week:
                if i in request.POST:
                    operate_on.append(i)
            if form.is_valid():
                comment_like_in_pages = False
                comment_like_in_walls = False
                comment_like_in_searches = False
                comment_like_in_groups = False
                comment_like_in_permalinks = False
                if request.POST.get('comment_like_in_pages') is not None:
                    comment_like_in_pages = True
                if request.POST.get('comment_like_in_walls') is not None:
                    comment_like_in_walls = True
                if request.POST.get('comment_like_in_searches') is not None:
                    comment_like_in_searches = True
                if request.POST.get('comment_like_in_groups') is not None:
                    comment_like_in_groups = True
                if request.POST.get('comment_like_in_permalinks') is not None:
                    comment_like_in_permalinks = True
                keywords = None
                if request.POST.get('keywords'):
                    keywords = request.POST.get('keywords').split(',')
                exclude_keywords = None
                if request.POST.get('exclude_keywords'):
                    exclude_keywords = request.POST.get('exclude_keywords').split(',')
                url_text_area = None
                if request.POST.get('url_text_area'):
                    url_text_area = request.POST.get('url_text_area')
                try:
                    post = self.model.objects.get(dst_id=request.POST.get('dst_id'))
                    post.comment_like_in_pages = comment_like_in_pages
                    post.comment_like_in_walls = comment_like_in_walls
                    post.comment_like_in_searches = comment_like_in_searches
                    post.comment_like_in_groups = comment_like_in_groups
                    post.comment_like_in_permalinks = comment_like_in_permalinks
                    post.keywords = keywords
                    post.exclude_keywords = exclude_keywords
                    post.url_text_area = url_text_area
                    post.date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    post.save()
                except self.model.DoesNotExist:
                    post = self.model(
                        dst_id=request.POST.get('dst_id'),
                        comment_like_in_pages=comment_like_in_pages,
                        comment_like_in_walls=comment_like_in_walls,
                        comment_like_in_searches=comment_like_in_searches,
                        comment_like_in_groups=comment_like_in_groups,
                        comment_like_in_permalinks=comment_like_in_permalinks,
                        keywords=keywords,
                        exclude_keywords=exclude_keywords,
                        url_text_area=url_text_area,
                        date=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                    post.save()
        return HttpResponseRedirect('/tools/comments/sources?dst_id={0}'.format(request.POST.get('dst_id')))


class ToolsCommentsResultsView(View):
    template_name = "components/tools/tools_comments_results.html"

    def get(self, request, *args, **kwargs):
        form = CommentsResults.objects.all()
        return render(request, self.template_name, {'dst_id': request.GET.get('dst_id'), 'form': form})


class ToolsContactView(View):
    template_name = "components/tools/tools_contact.html"

    def get(self, request, *args, **kwargs):
        print(request.GET.get('login'))
        return render(request, self.template_name, {'login': request.GET.get('login')})


class ToolsContactExtractView(View):
    form_class = ToolsExtractMembersForm
    template_name = "components/tools/tools_contact_extract_members.html"

    def get(self, request, *args, **kwargs):
        print(request.GET.get('login'))
        return render(request, self.template_name, {'login': request.GET.get('login'), 'form': self.form_class})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        print(request.POST)
        print(request.POST.get('login'))
        if form.is_valid():
            print(request.POST.get('login'))
        return HttpResponseRedirect('/tools/contact/extract?login={0}'.format(request.POST.get('login')))


class ToolsContactUseView(View):
    form_class = ToolsUseMembersForm
    template_name = "components/tools/tools_contact_use_members.html"

    def get(self, request, *args, **kwargs):
        print(request.GET.get('login'))
        return render(request, self.template_name, {'login': request.GET.get('login'), 'form': self.form_class})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        print(request.POST)
        print(request.POST.get('login'))
        if form.is_valid():
            print(request.POST.get('login'))
        return HttpResponseRedirect('/tools/contact/use?login={0}'.format(request.POST.get('login')))


class ToolsContactResultsView(View):
    template_name = "components/tools/tools_contact_results.html"

    def get(self, request, *args, **kwargs):
        print(request.GET.get('login'))
        return render(request, self.template_name, {'login': request.GET.get('login')})


class ToolsAccountActionView(View):
    form_class = ToolsAccountActionForm
    template_name = "components/tools/tools_account_action.html"

    def get(self, request, *args, **kwargs):
        print(request.GET.get('dst_id'))
        dst_list = ToolsDestinationList.objects.get(id=request.GET.get('dst_id'))
        return render(request, self.template_name, {'dst_id': request.GET.get('dst_id'),
                                                    'dst_name': dst_list.dst_name,
                                                    'form': self.form_class(dst_id=request.GET.get('dst_id'))})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, dst_id=None)
        if form.is_valid():
            if request.POST.get('dst_id') is not None:
                operate_on = []
                week = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']
                for i in week:
                    if i in request.POST:
                        operate_on.append(i)
                account_actions, created = ToolsAccountActions.objects.get_or_create(dst_id=request.POST.get('dst_id'))
                account_actions.dst_id = request.POST.get('dst_id')
                account_actions.wait_between = form.cleaned_data['wait_between']
                account_actions.wait_between_and = form.cleaned_data['wait_between_and']
                account_actions.execute_between = form.cleaned_data['execute_between']
                account_actions.execute_between_and = form.cleaned_data['execute_between_and']
                account_actions.random_sleep_time = form.cleaned_data['random_sleep_time']
                account_actions.rotate_weekdays_randomly = form.cleaned_data['rotate_weekdays_randomly']
                account_actions.operate_on = operate_on
                account_actions.accept_per_login = form.cleaned_data['accept_per_login']
                account_actions.auto_accept_friends = form.cleaned_data['auto_accept_friends']
                account_actions.auto_like_news_feed_posts = form.cleaned_data['auto_like_news_feed_posts']
                account_actions.auto_like_news_feed_posts_num = form.cleaned_data['auto_like_news_feed_posts_num']
                account_actions.auto_like_news_feed_posts_keywords = form.cleaned_data['auto_like_news_feed_posts_keywords']
                account_actions.auto_like_news_feed_posts_keywords_num = form.cleaned_data['auto_like_news_feed_posts_keywords_num']
                account_actions.keywords = [form.cleaned_data['keywords']]
                account_actions.exclude_keywords = [form.cleaned_data['exclude_keywords']]
                account_actions.like_between_post_per_login = form.cleaned_data['like_between_post_per_login']
                account_actions.like_between_post_per_login_and = form.cleaned_data['like_between_post_per_login_and']
                account_actions.read_notifications_and_messages = form.cleaned_data['read_notifications_and_messages']
                account_actions.high_percent = form.cleaned_data['high_percent']
                account_actions.middle_percent = form.cleaned_data['middle_percent']
                account_actions.low_percent = form.cleaned_data['low_percent']
                account_actions.use_session_settings = form.cleaned_data['use_session_settings']
                account_actions.long_session_time_min = form.cleaned_data['long_session_time_min']
                account_actions.long_session_time_max = form.cleaned_data['long_session_time_max']
                account_actions.medium_session_time_min = form.cleaned_data['medium_session_time_min']
                account_actions.medium_session_time_max = form.cleaned_data['medium_session_time_max']
                account_actions.short_session_time_min = form.cleaned_data['short_session_time_min']
                account_actions.short_session_time_max = form.cleaned_data['short_session_time_max']
                account_actions.short_time_min = form.cleaned_data['short_time_min']
                account_actions.short_time_max = form.cleaned_data['short_time_max']
                account_actions.medium_time_min = form.cleaned_data['medium_time_min']
                account_actions.medium_time_max = form.cleaned_data['medium_time_max']
                account_actions.long_time_min = form.cleaned_data['long_time_min']
                account_actions.long_time_max = form.cleaned_data['long_time_max']
                account_actions.use_engagement_levels = form.cleaned_data['use_engagement_levels']
                account_actions.strong_time_min = form.cleaned_data['strong_time_min']
                account_actions.strong_time_max = form.cleaned_data['strong_time_max']
                account_actions.moderate_time_min = form.cleaned_data['moderate_time_min']
                account_actions.moderate_time_max = form.cleaned_data['moderate_time_max']
                account_actions.weak_time_min = form.cleaned_data['weak_time_min']
                account_actions.weak_time_max = form.cleaned_data['weak_time_max']
                account_actions.date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                account_actions.save()
        return HttpResponseRedirect('/tools/account/action?dst_id={0}'.format(request.POST.get('dst_id')))
