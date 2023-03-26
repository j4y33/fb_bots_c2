import base64
import io
import os
import os.path
from datetime import datetime

from PIL import Image
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView

from dashboard.forms.campaign_add_from import CampaignAddForm
from dashboard.forms.campaign_add_post_from import CampaignAddPost
from dashboard.forms.campaign_history_form import HistoryForm
from dashboard.forms.what_publish_from import WhatPublishForm
from dashboard.forms.when_publish_from import WhenPublishForm
from dashboard.forms.where_publish_comment_like import WherePublishCommentLikeForm
from dashboard.forms.where_publish_from import WherePublishForm
from dashboard.forms.where_publish_monitor_folders import WherePublishMonitorFoldersForm
from dashboard.forms.where_publish_rss_from import WherePublishRSSForm
from dashboard.models import Action, CampaignsPosts, CampaignsWhereToPublish, Groups, DestinationLists, Campaigns, \
    CampaignsScrapAndSharePosts, CampaignsScheduler, Errors, CampaignsMonitorFolders, CampaignsCommentLike, \
    CampaignsScrapedPosts


class CampaignsView(TemplateView):
    template_name = "components/campaigns.html"

    def get_context_data(self, **kwargs):
        context = super(CampaignsView, self).get_context_data(**kwargs)
        context.update({'title': "Campaigns Page"})
        return context


class CampaignsOverviewView(View):
    model = Campaigns
    template_name = "components/campaigns/overview.html"

    def get(self, request, *args, **kwargs):
        campaign_db_view = []
        all_campaigns = self.model.objects.all()
        for i in all_campaigns:
            total_posts = CampaignsPosts.objects.filter(campaign_id=i.id).count()
            # total_campaigns = campaigns_model.objects.filter(dst_lists__contains=i.id).count()
            campaign_db_view.append({'campaign_name': i.campaign_name,
                                     'errors': i.errors,
                                     'dst_lists': i.dst_lists,
                                     'posts': total_posts,
                                     'posts_done': None})
        return render(request, self.template_name, {'campaign': self.model.objects.all()})


class CampaignsAddView(View):
    form_class = CampaignAddForm
    name = {'key': 'value'}
    template_name = "components/campaigns/add_campaign.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        print(request.POST)
        form = self.form_class(request.POST)
        if form.is_valid():
            stop_after_single_error = False
            do_not_publish_in_parallel = False
            stop_campaign_after_errors = False
            if request.POST.get('stop_account') is not None:
                stop_after_single_error = True
            if request.POST.get('stop_publish') is not None:
                do_not_publish_in_parallel = True
            if request.POST.get('stop_campaign') is not None:
                stop_campaign_after_errors = True
            for dst_list in request.POST.getlist('select'):
                print(dst_list)
                dst_list_obj = DestinationLists.objects.get(id=dst_list)
                if dst_list_obj.campaigns is not None:
                    dst_list_obj.campaigns.append(request.POST.get('name'))
                    dst_list_obj.save()
                else:
                    DestinationLists.objects.filter(id=dst_list).update(campaigns=[request.POST.get('name')])
            campaign = Campaigns(campaign_name=request.POST.get('name'),
                                 description=request.POST.get('description'),
                                 dst_lists=request.POST.getlist('select'),
                                 stop_after_single_error=stop_after_single_error,
                                 do_not_publish_in_parallel=do_not_publish_in_parallel,
                                 stop_campaign_after_errors=stop_campaign_after_errors,
                                 errors='{}',
                                 date=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            campaign.save()
            return HttpResponseRedirect('/campaigns/overview/')

        return HttpResponseRedirect("/campaigns/overview/")


class CampaignsWhatPublishView(TemplateView):
    template_name = "components/campaigns/what_publish.html"

    def get_context_data(self, **kwargs):
        context = super(CampaignsWhatPublishView, self).get_context_data(**kwargs)
        context.update({'title': "What to publish"})
        return context


class CampaignsWhatPublishAddPostView(View):
    form_class = CampaignAddPost
    name = {'key': 'value'}
    template_name = "components/campaigns/what_publish/add_posts.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        # content = request.FILES.getlist('content')
        form = self.form_class(request.POST)
        encoded_image = None
        if form.is_valid():
            # for file in content:
            file_directory_within_bucket = None
            if request.POST.get('content') != "":
                content = request.FILES['content']
                in_mem_file = io.BytesIO()
                pil_image = Image.open(content)
                pil_image.save(in_mem_file, format=pil_image.format)
                encoded_image = base64.b64encode(in_mem_file.getvalue())
                encoded_image = encoded_image.decode('utf-8')
                file_directory_within_bucket = '{campaign}/{filename}'.format(
                    campaign=request.POST.get('select'),
                    filename=content.name)
                default_storage.save(file_directory_within_bucket, content)
            post = CampaignsPosts(campaign_id=request.POST.get('select'),
                                  post_text=request.POST.get('post_text'),
                                  content=file_directory_within_bucket,
                                  screen=encoded_image,
                                  status='pending',
                                  src='manual post',
                                  published_by=request.POST.get('published_by'),
                                  date=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                  running=[],
                                  posted=[])
            post.save()
            return HttpResponseRedirect('/campaigns/what_publish/')

        return HttpResponseRedirect("/campaigns/what_publish/")


class CampaignsWhatPublishScrapAndSharePostView(View):
    model = CampaignsScrapAndSharePosts
    template_name = "components/campaigns/what_publish/scrape_share_posts.html"

    def get(self, request, *args, **kwargs):
        form_class = WhatPublishForm(camp=request.GET.get('campaign'))
        return render(request, self.template_name, {'campaign': form_class})

    def post(self, request, *args, **kwargs):
        form = WhatPublishForm(request.POST, camp=None)

        if form.is_valid() and request.POST.get('update') is not None:
            post_content_text = None
            if request.POST.get('content') != "":
                content = request.FILES['content']
                if content:
                    posts_text = content.read().splitlines()
                    for i in posts_text:
                        if post_content_text is None:
                            post_content_text = i.decode("utf-8")
                        else:
                            post_content_text = post_content_text + '|' + i.decode("utf-8")
            if post_content_text is None:
                post_content_text = form.cleaned_data['post_text']
            post, created = CampaignsScrapAndSharePosts.objects.get_or_create(campaign_id=request.POST.get('select'))
            post.campaign_id = form.cleaned_data['select']
            post.process_name = form.cleaned_data['process_name']
            post.url = form.cleaned_data['url']
            post.keywords = form.cleaned_data['keywords']
            post.exclude_keywords = form.cleaned_data['exclude_keywords']
            post.ignore_items_without_images = form.cleaned_data['ignore_items_without_images']
            post.maximum_posts = form.cleaned_data['maximum_posts']
            post.post_text = post_content_text
            post.date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            post.save()
        return HttpResponseRedirect(
            '/campaigns/what_publish/scrap_and_share_post?campaign={0}'.format(request.POST.get('select')))


class CampaignsWhatPublishRssPostView(TemplateView):
    form_class = WherePublishRSSForm
    template_name = "components/campaigns/what_publish/rss_posts.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'campaign': self.form_class})


class CampaignsWhatPublishMonitorFoldersView(TemplateView):
    form = WherePublishMonitorFoldersForm
    model = CampaignsMonitorFolders
    template_name = "components/campaigns/what_publish/monitor_folders.html"

    def get(self, request, *args, **kwargs):
        form_class = WherePublishMonitorFoldersForm(camp=request.GET.get('campaign'))
        return render(request, self.template_name, {'campaign': form_class})

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST, camp=None)
        if form.is_valid():
            if request.POST.get('add'):
                folders = request.POST.get('url_text_area').split(',')
                dir_path = os.path.dirname(os.path.realpath(__file__))
                print(dir_path)
                status = 'wait'
                if request.POST.get('add_post_as_pending') is not None:
                    status = 'pending'
                elif request.POST.get('add_post_as_publishing') is not None:
                    status = 'publishing'
                valid_images = [".jpg", ".png", ".jpeg"]
                for folder in folders:
                    for file in os.listdir(folder):
                        ext = os.path.splitext(file)[1]
                        if ext.lower() not in valid_images:
                            continue
                        file_directory_within_bucket = '{campaign}/{filename}'.format(
                            campaign=request.POST.get('select'),
                            filename=file)
                        in_mem_file = io.BytesIO()
                        pil_image = Image.open(os.path.join(folder, file))
                        pil_image.save(in_mem_file, format=pil_image.format)
                        default_storage.save(file_directory_within_bucket, ContentFile(in_mem_file.getvalue()))
                        encoded_image = base64.b64encode(in_mem_file.getvalue())
                        post = CampaignsPosts(campaign_id=request.POST.get('select'),
                                              content=file_directory_within_bucket,
                                              screen=encoded_image.decode('utf-8'),
                                              status=status,
                                              src='folder',
                                              date=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                              running=[],
                                              posted=[])
                        post.save()
                campaigns_monitor_folders, created = CampaignsMonitorFolders.objects.get_or_create(
                    campaign_id=request.POST.get('select'))
                campaigns_monitor_folders.folders = [form.cleaned_data['url_text_area']]
                campaigns_monitor_folders.save()
        return HttpResponseRedirect(
            '/campaigns/what_publish/monitor_folders?campaign={0}'.format(request.POST.get('select')))


class CampaignsWhatPublishCommentLikeView(TemplateView):
    form = WherePublishCommentLikeForm
    model = CampaignsCommentLike
    template_name = "components/campaigns/what_publish/comment_like.html"

    def get(self, request, *args, **kwargs):
        form_class = WherePublishCommentLikeForm(camp=request.GET.get('campaign'))
        return render(request, self.template_name, {'campaign': form_class})

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST, camp=None)
        if form.is_valid():
            if request.POST.get('confirm'):
                campaigns_comment_like, created = self.model.objects.get_or_create(
                    campaign_id=request.POST.get('select'))
                campaigns_comment_like.keywords = [form.cleaned_data['keywords']]
                campaigns_comment_like.exclude = [form.cleaned_data['exclude']]
                campaigns_comment_like.like_all_posts_in_history = form.cleaned_data['like_all_posts_in_history']
                campaigns_comment_like.save()
        return HttpResponseRedirect(
            '/campaigns/what_publish/comment_like?campaign={0}'.format(request.POST.get('select')))


class CampaignsWherePublishView(View):
    model = DestinationLists
    form_class = WherePublishForm
    template_name = "components/campaigns/where_publish.html"

    def get(self, request, *args, **kwargs):
        groups_model = Groups
        dst_db_view = []
        all_dst = self.model.objects.all()
        for i in all_dst:
            total_groups = 0
            bots = i.profiles
            for bot in bots:
                total_groups += groups_model.objects.filter(bot_id=bot).count()
            # total_campaigns = campaigns_model.objects.filter(dst_lists__contains=i.id).count()
            dst_db_view.append({'dst_name': i.dst_name,
                                'profiles': len(i.profiles),
                                'groups': total_groups,
                                'campaigns': CampaignsWhereToPublish.objects.filter(dst_lists=i.dst_name).count(),
                                'walls': len(i.walls)})

        return render(request, self.template_name, {'form': dst_db_view, 'select': self.form_class})

    def post(self, request, *args, **kwargs):
        print(request.POST)
        dst_lists = request.POST.getlist('selected_dst')
        campaign_id = request.POST.get('select')
        for dst in dst_lists:
            try:
                CampaignsWhereToPublish.objects.get(campaign_id=campaign_id, dst_lists=dst)
                from django.contrib import messages
                messages.success(request, 'Destination list already exist')
            except CampaignsWhereToPublish.DoesNotExist:
                where_publish_model = CampaignsWhereToPublish(campaign_id=campaign_id,
                                                              dst_lists=dst,
                                                              date=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                where_publish_model.save()
                from django.contrib import messages
                messages.success(request, 'Added new destination list to campaign')
        return HttpResponseRedirect('/campaigns/where_publish/')


class CampaignsWhenPublishView(View):
    model = CampaignsScheduler
    form_class = WhenPublishForm
    template_name = "components/campaigns/when_publish.html"

    def get(self, request, *args, **kwargs):
        print(request.GET.get('campaign'))
        form_class = WhenPublishForm(camp=request.GET.get('campaign'))
        return render(request, self.template_name, {'campaign': form_class})

    def post(self, request, *args, **kwargs):
        if request.POST.get('confirm') is not None:
            print(request.POST)
            form = self.form_class(request.POST, camp=None)
            operate_on = []
            week = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']
            for i in week:
                if i in request.POST:
                    operate_on.append(i)
            if form.is_valid():
                randomise_interval_each_day = False
                randomise_number_of_posts = False
                rotate_weekdays_randomly = False
                wait = False
                if request.POST.get('randomise_interval_each_day') is not None:
                    randomise_interval_each_day = True
                if request.POST.get('randomise_number_of_posts') is not None:
                    randomise_number_of_posts = True
                if request.POST.get('rotate_weekdays_randomly') is not None:
                    rotate_weekdays_randomly = True
                if request.POST.get('wait') is not None:
                    wait = True
                try:
                    post = self.model.objects.get(campaign_id=request.POST.get('select'))
                    if request.POST.get('post_per_day'):
                        post.posts_per_day = request.POST.get('post_per_day')
                    if request.POST.get('publish_time_start'):
                        post.post_interval_start = request.POST.get('publish_time_start')
                    if request.POST.get('publish_time_end'):
                        post.post_interval_finish = request.POST.get('publish_time_end')
                    post.randomise_interval_each_day = randomise_interval_each_day
                    post.randomise_number_of_posts = randomise_number_of_posts
                    if request.POST.get('randomise_number_of_posts_maximum'):
                        post.maximum_randomise_posts = request.POST.get('randomise_number_of_posts_maximum')
                    post.wait = wait
                    if request.POST.get('wait_seconds'):
                        post.wait_before_publishing_with_same_account = request.POST.get('wait_seconds')
                    post.rotate_weekdays_randomly = rotate_weekdays_randomly
                    post.operate_on = operate_on
                    post.date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    post.save()
                except self.model.DoesNotExist:
                    maximum_randomise_posts = 0
                    wait_seconds = 0
                    if request.POST.get('randomise_number_of_posts_maximum'):
                        maximum_randomise_posts = request.POST.get('randomise_number_of_posts_maximum')
                    if request.POST.get('wait_seconds'):
                        wait_seconds = request.POST.get('wait_seconds')
                    post = self.model(campaign_id=request.POST.get('select'),
                                      posts_per_day=request.POST.get('post_per_day'),
                                      post_interval_start=request.POST.get('publish_time_start'),
                                      post_interval_finish=request.POST.get('publish_time_end'),
                                      randomise_interval_each_day=randomise_interval_each_day,
                                      randomise_number_of_posts=randomise_number_of_posts,
                                      maximum_randomise_posts=maximum_randomise_posts,
                                      wait=wait,
                                      wait_before_publishing_with_same_account=wait_seconds,
                                      rotate_weekdays_randomly=rotate_weekdays_randomly,
                                      operate_on=operate_on,
                                      date=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                    post.save()
        return HttpResponseRedirect('/campaigns/when_publish?campaign={0}'.format(request.POST.get('select')))


class CampaignsPostListView(View):
    model = CampaignsPosts

    template_name = "components/campaigns/post_list.html"

    def get(self, request, *args, **kwargs):

        return render(request, self.template_name, {'form': self.model.objects.all().select_related()})

    def post(self, request, *args, **kwargs):
        print(request.POST)
        if request.POST.get('delete'):
            print(request.POST.get('selected_post_list'))
            self.model.objects.filter(id=request.POST.get('selected_post_list')).delete()
        if request.POST.get('delete_all'):
            self.model.objects.all().delete()
        return HttpResponseRedirect('/campaigns/post_list/')


class CampaignsHistoryView(View):
    model = Action
    template_name = "components/campaigns/history.html"

    def get(self, request, *args, **kwargs):
        # and Join errors table, group by date
        dst = DestinationLists
        camp_id = request.GET.get('campaign')
        campaign_name = None
        history_dst = None
        if camp_id is not None and camp_id != '':
            campaign_name = Campaigns.objects.get(id=camp_id)
            history_dst = dst.objects.filter(campaigns__contains=[campaign_name.campaign_name]).values_list('profiles',
                                                                                                            flat=True)
        actions_db_view = []
        all_actions = self.model.objects.filter().exclude(action_id='none').exclude(action_id='news_feed').exclude(
            action_id='login').order_by('-date')[:100]
        all_errors = Errors.objects.all().order_by('-date')[:100]
        # Require review
        for i in all_actions:
            if camp_id is not None and camp_id != '':
                if i.bot_id not in history_dst:
                    continue
                if i.action_id is None:
                    continue
            actions_db_view.append({'bot_id': i.bot_id,
                                    'action_priority': i.action_priority,
                                    'action_id': i.action_id,
                                    'date': i.date,
                                    'image': i.image})
        for i in all_errors:
            if camp_id is not None and camp_id != '':
                if i.bot_id not in history_dst:
                    continue
            actions_db_view.append({'bot_id': i.bot_id,
                                    'stacktrace': i.error,
                                    'action_id': 'error',
                                    'date': i.date,
                                    'image': i.image})
        form_class = HistoryForm(camp=camp_id)
        return render(request, self.template_name, {'form': actions_db_view, 'campaign': form_class})

    def post(self, request, *args, **kwargs):
        return HttpResponseRedirect('/campaigns/history?campaign={0}'.format(request.POST.get('select')))
