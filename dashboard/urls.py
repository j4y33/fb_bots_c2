from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.LoginView.as_view(), name="login"),
    url(r'^index/$', views.IndexView.as_view(), name="index"),
    url(r'^destination_lists/$', views.DestinationView.as_view(), name="destination_lists"),
    url(r'^destination_lists/add$', views.DestinationAddView.as_view(), name="destination_lists_add"),

    url(r'^campaigns/$', views.CampaignsView.as_view(), name="campaigns"),
    url(r'^campaigns/overview/$', views.CampaignsOverviewView.as_view(), name="campaigns_overview"),
    url(r'^campaigns/overview/add_campaign/$', views.CampaignsAddView.as_view(), name="add_campaign"),
    url(r'^campaigns/what_publish/$', views.CampaignsWhatPublishView.as_view(), name="campaigns_what_publish"),
    url(r'^campaigns/what_publish/add_post$', views.CampaignsWhatPublishAddPostView.as_view(), name="campaigns_what_publish_post"),
    url(r'^campaigns/what_publish/scrap_and_share_post$', views.CampaignsWhatPublishScrapAndSharePostView.as_view(), name="campaigns_what_publish_scrap_and_share_post"),
    url(r'^campaigns/what_publish/rss_post$', views.CampaignsWhatPublishRssPostView.as_view(), name="campaigns_what_publish_rss_post"),
    url(r'^campaigns/what_publish/monitor_folders$', views.CampaignsWhatPublishMonitorFoldersView.as_view(),
        name="campaigns_what_publish_monitor_folders"),
    url(r'^campaigns/what_publish/comment_like$', views.CampaignsWhatPublishCommentLikeView.as_view(),
        name="campaigns_what_publish_comment_like"),
    url(r'^campaigns/where_publish/$', views.CampaignsWherePublishView.as_view(), name="campaigns_where_publish"),
    url(r'^campaigns/when_publish$', views.CampaignsWhenPublishView.as_view(), name="campaigns_when_publish"),
    url(r'^campaigns/post_list/$', views.CampaignsPostListView.as_view(), name="campaigns_post_list"),
    url(r'^campaigns/history$', views.CampaignsHistoryView.as_view(), name="campaigns_history"),


    url(r'^tools/$', views.ToolsView.as_view(), name="tools"),
    #url(r'^tools/stream/$', views.ToolsStream.as_view(), name="tools_stream"),
    url(r'^tools/create_bots_group$', views.ToolsCreateBotsGroupView.as_view(), name="create_bots_group"),
    url(r'^tools/base$', views.ToolsBaseView.as_view(), name="tools_base"),
    url(r'^tools/finder$', views.ToolsFinderView.as_view(), name="tools_finder"),
    url(r'^tools/finder/find_groups$', views.ToolsFinderFindGroupsView.as_view(), name="tools_finder_find_groups"),
    url(r'^tools/finder/find_pages$', views.ToolsFinderFindPagesView.as_view(), name="tools_finder_find_pages"),
    url(r'^tools/finder/find_friends$', views.ToolsFinderFindFriendsView.as_view(), name="tools_finder_find_friends"),

    url(r'^tools/joiner$', views.ToolsJoinerView.as_view(), name="tools_joiner"),
    url(r'^tools/joiner/show_groups$', views.ToolsJoinerShowGroupsView.as_view(), name="tools_joiner_show_groups"),
    url(r'^tools/joiner/show_pages$', views.ToolsJoinerShowPagesView.as_view(), name="tools_joiner_show_pages"),
    url(r'^tools/comments$', views.ToolsCommentsView.as_view(), name="tools_comments"),
    url(r'^tools/comments/settings$', views.ToolsCommentsSettingsView.as_view(), name="tools_comments_settings"),
    url(r'^tools/comments/sources$', views.ToolsCommentsSourcesView.as_view(), name="tools_comments_sources"),
    url(r'^tools/comments/results$', views.ToolsCommentsResultsView.as_view(), name="tools_comments_results"),
    url(r'^tools/contact$', views.ToolsContactView.as_view(), name="tools_contact"),
    url(r'^tools/contact/extract$', views.ToolsContactExtractView.as_view(), name="tools_contact_extract_members"),
    url(r'^tools/contact/use$', views.ToolsContactUseView.as_view(), name="tools_contact_use_members"),
    url(r'^tools/contact/results$', views.ToolsContactResultsView.as_view(), name="tools_contact_results"),
    url(r'^tools/account/action$', views.ToolsAccountActionView.as_view(), name="tools_account_action"),

    url(r'^activity/$', views.ActivityView.as_view(), name="activity"),

    url(r'^social/$', views.SocialView.as_view(), name="social"),
    url(r'^cloud/$', views.CloudView.as_view(), name="cloud"),
]
