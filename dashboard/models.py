from django.db import models
from django.contrib.postgres.fields import ArrayField


class Accounts(models.Model):
    account = models.TextField(primary_key=True)
    bot_id = models.TextField(blank=True, null=True)
    bot_friend = models.BooleanField(blank=True, null=True)
    creation_date = models.DateTimeField(blank=True, null=True)
    parsed_date = models.DateTimeField(blank=True, null=True)
    parsed = models.BooleanField(blank=True, null=True)
    error = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'accounts'


class Action(models.Model):
    bot_id = models.TextField(blank=True, null=True)
    groups_id = models.IntegerField(blank=True, null=True)
    dst_id = models.IntegerField(blank=True, null=True)
    action_priority = models.TextField(blank=True, null=True)
    action_id = models.TextField(blank=True, null=True)
    action_status = models.BooleanField(blank=True, null=True)
    image = models.TextField(blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'action'


class Groups(models.Model):
    bot_id = models.TextField(blank=True, null=True)
    link = models.TextField(blank=True, null=True)
    group_name = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    dst_select_status = models.BooleanField(blank=True, null=True)
    screen = models.TextField(blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'groups'


class Bots(models.Model):
    #login = models.OneToOneField(Groups, to_field='bot_id', primary_key=True, on_delete=models.CASCADE)
    login = models.TextField(primary_key=True)
    password = models.TextField(blank=True, null=True)
    vpn_provider = models.TextField(blank=True, null=True)
    vpn_region = models.TextField(blank=True, null=True)
    vpn_login = models.TextField(blank=True, null=True)
    vpn_password = models.TextField(blank=True, null=True)
    cookies = models.TextField(blank=True, null=True)
    used_status = models.BooleanField(blank=True, null=True)
    block_status = models.TextField(blank=True, null=True)
    bot_first_name = models.TextField(blank=True, null=True)
    bot_last_name = models.TextField(blank=True, null=True)
    bot_gender = models.TextField(blank=True, null=True)
    bot_birth_day = models.TextField(blank=True, null=True)
    bot_birth_month = models.TextField(blank=True, null=True)
    bot_birth_year = models.TextField(blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    screen = models.TextField(blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    school = models.TextField(blank=True, null=True)
    university = models.TextField(blank=True, null=True)
    job = models.TextField(blank=True, null=True)
    profile_picture = models.TextField(blank=True, null=True)
    bot_images_list = models.TextField(blank=True, null=True)
    creation_date = models.DateTimeField(blank=True, null=True)
    last_used_date = models.DateTimeField(blank=True, null=True)
    total_friends = models.IntegerField(blank=True, null=True)
    scraped_profiles = models.IntegerField(blank=True, null=True)
    total_actions = models.IntegerField(blank=True, null=True)
    total_errors = models.IntegerField(blank=True, null=True)
    proxy_ip = models.TextField(blank=True, null=True)
    proxy_port = models.TextField(blank=True, null=True)
    proxy_user = models.TextField(blank=True, null=True)
    proxy_password = models.TextField(blank=True, null=True)
    local_ip = models.TextField(blank=True, null=True)
    public_ip = models.TextField(blank=True, null=True)
    instance_id = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bots'


class Errors(models.Model):
    bot_id = models.TextField(blank=True, null=True)
    error = models.TextField(blank=True, null=True)
    image = models.TextField(blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'errors'


class Following(models.Model):
    bot_id = models.TextField(blank=True, null=True)
    link = models.TextField(blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'following'


class Friends(models.Model):
    bot_id = models.TextField(blank=True, null=True)
    friend_link = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'friends'


class BotGroups(models.Model):
    group_id = models.TextField(blank=True, null=True)
    link = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bot_groups'


class Images(models.Model):
    bot_id = models.TextField(blank=True, null=True)
    gender = models.TextField(blank=True, null=True)
    profile = models.TextField(blank=True, null=True)
    image = models.TextField(blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'images'


class Campaigns(models.Model):
    campaign_name = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    dst_lists = ArrayField(models.TextField(blank=True, null=True))
    errors = ArrayField(models.TextField(blank=True, null=True))
    stop_after_single_error = models.BooleanField(blank=True, null=True)
    do_not_publish_in_parallel = models.BooleanField(blank=True, null=True)
    stop_campaign_after_errors = models.BooleanField(blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'campaigns'


class CampaignsPosts(models.Model):
    campaign = models.ForeignKey(Campaigns, on_delete=models.CASCADE)
    #campaign_id = models.IntegerField(blank=True, null=True)
    post_text = models.TextField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    screen = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    src = models.TextField(blank=True, null=True)
    published_by = models.IntegerField(blank=True, null=True)
    running = ArrayField(models.TextField(blank=True, null=True))
    posted = ArrayField(models.TextField(blank=True, null=True))
    posted_groups = ArrayField(models.TextField(blank=True, null=True))
    posted_walls = ArrayField(models.TextField(blank=True, null=True))
    date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'campaigns_posts'


class CampaignsScrapAndSharePosts(models.Model):
    campaign = models.ForeignKey(Campaigns, on_delete=models.CASCADE)
    process_name = models.TextField(blank=True, null=True)
    #campaign_id = models.IntegerField(blank=True, null=True)
    url = models.TextField(blank=True, null=True)
    keywords = models.TextField(blank=True, null=True)
    exclude_keywords = models.TextField(blank=True, null=True)
    ignore_items_without_images = models.BooleanField(blank=True, null=True)
    maximum_posts = models.IntegerField(blank=True, null=True)
    post_text = models.TextField(blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'campaigns_scrap_and_share_posts'


class CampaignsScrapedPosts(models.Model):
    url = models.TextField(blank=True, null=True)
    campaign_id = models.IntegerField(blank=True, null=True)
    screen = models.TextField(blank=True, null=True)
    shared_bots = ArrayField(models.TextField(blank=True, null=True))
    shared_groups = ArrayField(models.TextField(blank=True, null=True))
    shared_pages = ArrayField(models.TextField(blank=True, null=True))
    date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'campaigns_scraped_posts'

class CampaignsWhereToPublish(models.Model):
    campaign_id = models.IntegerField(blank=True, null=True)
    dst_lists = models.TextField(blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'campaigns_where_to_publish'


class CampaignsMonitorFolders(models.Model):
    campaign_id = models.IntegerField(blank=True, null=True)
    folders = ArrayField(models.TextField(blank=True, null=True))
    date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'campaigns_monitor_folders'


class CampaignsCommentLike(models.Model):
    campaign_id = models.IntegerField(blank=True, null=True)
    keywords = ArrayField(models.TextField(blank=True, null=True))
    exclude = ArrayField(models.TextField(blank=True, null=True))
    like_all_posts_in_history = models.BooleanField(blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'campaigns_comment_like'


class CampaignsScheduler(models.Model):
    campaign_id = models.IntegerField(blank=True, null=True)
    posts_per_day = models.IntegerField(blank=True, null=True)
    post_interval_start = models.TextField(blank=True, null=True)
    post_interval_finish = models.TextField(blank=True, null=True)
    randomise_interval_each_day = models.BooleanField(blank=True, null=True)
    randomise_number_of_posts = models.BooleanField(blank=True, null=True)
    maximum_randomise_posts = models.IntegerField(blank=True, null=True)
    wait = models.BooleanField(blank=True, null=True)
    wait_before_publishing_with_same_account = models.IntegerField(blank=True, null=True)
    rotate_weekdays_randomly = models.BooleanField(blank=True, null=True)
    operate_on = ArrayField(models.TextField(blank=True, null=True))
    date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'campaigns_scheduler'


class DestinationLists(models.Model):
    dst_name = models.TextField(blank=True, null=True)
    profiles = ArrayField(models.TextField(blank=True, null=True))
    campaigns = ArrayField(models.TextField(blank=True, null=True))
    walls = ArrayField(models.TextField(blank=True, null=True))
    comment = ArrayField(models.TextField(blank=True, null=True))
    date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'destination_lists'


class CommentsSettings(models.Model):
    dst_id = models.IntegerField(blank=True, null=True)
    on_off = models.BooleanField(blank=True, null=True)
    wait_between_start = models.IntegerField(blank=True, null=True)
    wait_between_end = models.IntegerField(blank=True, null=True)
    execute_between_start = models.TextField(blank=True, null=True)
    execute_between_end = models.TextField(blank=True, null=True)
    random_sleep_time = models.BooleanField(blank=True, null=True)
    rotate_weekends_randomly = models.BooleanField(blank=True, null=True)
    operate_on = ArrayField(models.TextField(blank=True, null=True))
    comments_maximum_start = models.IntegerField(blank=True, null=True)
    comments_maximum_end = models.IntegerField(blank=True, null=True)
    comments_increasing_start = models.IntegerField(blank=True, null=True)
    comments_increasing_end = models.IntegerField(blank=True, null=True)
    maximum_single_source_per_day = models.BooleanField(blank=True, null=True)
    comments_single_source_maximum_start = models.IntegerField(blank=True, null=True)
    comments_single_source_maximum_end = models.IntegerField(blank=True, null=True)
    comments_post_maximum_age = models.BooleanField(blank=True, null=True)
    comments_maximum_days = models.IntegerField(blank=True, null=True)
    keywords = ArrayField(models.TextField(blank=True, null=True))
    exclude = ArrayField(models.TextField(blank=True, null=True))
    comment = models.TextField(blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'comments_settings'


class CommentsSources(models.Model):
    dst_id = models.IntegerField(blank=True, null=True)
    comment_like_in_pages = models.BooleanField(blank=True, null=True)
    comment_like_in_walls = models.BooleanField(blank=True, null=True)
    comment_like_in_searches = models.BooleanField(blank=True, null=True)
    keywords = ArrayField(models.TextField(blank=True, null=True))
    exclude_keywords = ArrayField(models.TextField(blank=True, null=True))
    comment_like_in_groups = models.BooleanField(blank=True, null=True)
    comment_like_in_permalinks = models.BooleanField(blank=True, null=True)
    url_text_area = models.TextField(blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'comments_sources'


class CommentsResults(models.Model):
    dst_id = models.IntegerField(blank=True, null=True)
    keywords = ArrayField(models.TextField(blank=True, null=True))
    exclude_keywords = ArrayField(models.TextField(blank=True, null=True))
    posted_link = models.TextField(blank=True, null=True)
    action_type = models.TextField(blank=True, null=True)
    story_text = models.TextField(blank=True, null=True)
    action_screen = models.TextField(blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'comments_results'


class ToolsFindGroups(models.Model):
    dst_id = models.IntegerField(blank=True, null=True)
    keywords = ArrayField(models.TextField(blank=True, null=True))
    exclude_keywords = ArrayField(models.TextField(blank=True, null=True))
    groups_extra_urls = ArrayField(models.TextField(blank=True, null=True))
    min_users = models.BooleanField(blank=True, null=True)
    en_gr_groups = models.BooleanField(blank=True, null=True)
    opened_groups = models.BooleanField(blank=True, null=True)
    admin_post = models.BooleanField(blank=True, null=True)
    min_users_count = models.IntegerField(blank=True, null=True)
    status = models.BooleanField(blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tools_find_groups'


class ToolsFindPages(models.Model):
    dst_id = models.IntegerField(blank=True, null=True)
    keywords = ArrayField(models.TextField(blank=True, null=True))
    exclude_keywords = ArrayField(models.TextField(blank=True, null=True))
    pages_extra_urls = ArrayField(models.TextField(blank=True, null=True))
    min_likes = models.BooleanField(blank=True, null=True)
    en_gr_pages = models.BooleanField(blank=True, null=True)
    min_likes_count = models.IntegerField(blank=True, null=True)
    status = models.BooleanField(blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tools_find_pages'


class ToolsFindFriends(models.Model):
    dst_id = models.IntegerField(blank=True, null=True)
    keywords = ArrayField(models.TextField(blank=True, null=True))
    exclude_keywords = ArrayField(models.TextField(blank=True, null=True))
    friends_extra_urls = ArrayField(models.TextField(blank=True, null=True))
    min_mutual = models.BooleanField(blank=True, null=True)
    en_gr_friends = models.BooleanField(blank=True, null=True)
    opened_friends = models.BooleanField(blank=True, null=True)
    min_mutual_count = models.IntegerField(blank=True, null=True)
    status = models.BooleanField(blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tools_find_friends'


class ToolsExtractedGroups(models.Model):
    dst_id = models.IntegerField(blank=True, null=True)
    url = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    members = models.IntegerField(blank=True, null=True)
    activity_today = models.IntegerField(blank=True, null=True)
    activity_last_30 = models.IntegerField(blank=True, null=True)
    created = models.TextField(blank=True, null=True)
    author = models.TextField(blank=True, null=True)
    joined = ArrayField(models.TextField(blank=True, null=True))
    bot_error = ArrayField(models.TextField(blank=True, null=True))
    required_answer = models.BooleanField(blank=True, null=True)
    admins = ArrayField(models.TextField(blank=True, null=True))
    access = models.BooleanField(blank=True, null=True)
    keywords = ArrayField(models.TextField(blank=True, null=True))
    exclude_keywords = ArrayField(models.TextField(blank=True, null=True))
    date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tools_extracted_groups'


class ToolsExtractedPages(models.Model):
    dst_id = models.IntegerField(blank=True, null=True)
    url = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    likes = models.IntegerField(blank=True, null=True)
    follow = ArrayField(models.TextField(blank=True, null=True))
    bot_error = ArrayField(models.TextField(blank=True, null=True))
    required_answer = models.BooleanField(blank=True, null=True)
    access = models.BooleanField(blank=True, null=True)
    keywords = ArrayField(models.TextField(blank=True, null=True))
    exclude_keywords = ArrayField(models.TextField(blank=True, null=True))
    date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tools_extracted_pages'


class ToolsExtractedFriends(models.Model):
    dst_id = models.IntegerField(blank=True, null=True)
    url = models.TextField(blank=True, null=True)
    total_friends = models.IntegerField(blank=True, null=True)
    friends = ArrayField(models.TextField(blank=True, null=True))
    bot_error = ArrayField(models.TextField(blank=True, null=True))
    required_answer = models.BooleanField(blank=True, null=True)
    access = models.BooleanField(blank=True, null=True)
    keywords = ArrayField(models.TextField(blank=True, null=True))
    exclude_keywords = ArrayField(models.TextField(blank=True, null=True))
    date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tools_extracted_friends'


class ToolsJoiner(models.Model):
    dst_id = models.IntegerField(blank=True, null=True)
    wait_between = models.IntegerField(blank=True, null=True)
    wait_between_and = models.IntegerField(blank=True, null=True)
    execute_between = models.TextField(blank=True, null=True)
    execute_between_and = models.TextField(blank=True, null=True)
    random_sleep_time = models.BooleanField(blank=True, null=True)
    join_between = models.IntegerField(blank=True, null=True)
    join_between_and = models.IntegerField(blank=True, null=True)
    auto_stop = models.BooleanField(blank=True, null=True)
    reaching_groups = models.IntegerField(blank=True, null=True)
    join_between_peer_day = models.IntegerField(blank=True, null=True)
    join_between_and_peer_day = models.IntegerField(blank=True, null=True)
    auto_stop_peer_day = models.BooleanField(blank=True, null=True)
    reaching_groups_peer_day = models.IntegerField(blank=True, null=True)
    operate_on = ArrayField(models.TextField(blank=True, null=True))
    date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tools_joiner'


class ToolsDestinationList(models.Model):
    dst_name = models.TextField(blank=True, null=True)
    profiles = ArrayField(models.TextField(blank=True, null=True))
    running = ArrayField(models.TextField(blank=True, null=True))
    extraction = models.TextField(blank=True, null=True)
    configuration = models.IntegerField(blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tools_destination_lists'


class ToolsAccountActions(models.Model):
    dst_id = models.IntegerField(blank=True, null=True)
    wait_between = models.IntegerField(blank=True, null=True)
    wait_between_and = models.IntegerField(blank=True, null=True)
    execute_between = models.TextField(blank=True, null=True)
    execute_between_and = models.TextField(blank=True, null=True)
    random_sleep_time = models.BooleanField(blank=True, null=True)
    rotate_weekdays_randomly = models.BooleanField(blank=True, null=True)
    operate_on = ArrayField(models.TextField(blank=True, null=True))
    accept_per_login = models.IntegerField(blank=True, null=True)
    auto_accept_friends = models.BooleanField(blank=True, null=True)
    auto_like_news_feed_posts = models.BooleanField(blank=True, null=True)
    auto_like_news_feed_posts_num = models.IntegerField(blank=True, null=True)
    auto_like_news_feed_posts_keywords = models.BooleanField(blank=True, null=True)
    auto_like_news_feed_posts_keywords_num = models.IntegerField(blank=True, null=True)
    keywords = ArrayField(models.TextField(blank=True, null=True))
    exclude_keywords = ArrayField(models.TextField(blank=True, null=True))
    like_between_post_per_login = models.IntegerField(blank=True, null=True)
    like_between_post_per_login_and = models.IntegerField(blank=True, null=True)
    read_notifications_and_messages = models.BooleanField(blank=True, null=True)
    # Percent of actions
    high_percent = models.IntegerField(blank=True, null=True)
    middle_percent = models.IntegerField(blank=True, null=True)
    low_percent = models.IntegerField(blank=True, null=True)
    # Session settings
    use_session_settings = models.BooleanField(blank=True, null=True)
    long_session_time_min = models.IntegerField(blank=True, null=True)
    long_session_time_max = models.IntegerField(blank=True, null=True)
    medium_session_time_min = models.IntegerField(blank=True, null=True)
    medium_session_time_max = models.IntegerField(blank=True, null=True)
    short_session_time_min = models.IntegerField(blank=True, null=True)
    short_session_time_max = models.IntegerField(blank=True, null=True)
    # Delays
    short_time_min = models.IntegerField(blank=True, null=True)
    short_time_max = models.IntegerField(blank=True, null=True)
    medium_time_min = models.IntegerField(blank=True, null=True)
    medium_time_max = models.IntegerField(blank=True, null=True)
    long_time_min = models.IntegerField(blank=True, null=True)
    long_time_max = models.IntegerField(blank=True, null=True)
    # engagement levels
    use_engagement_levels = models.BooleanField(blank=True, null=True)
    strong_time_min = models.IntegerField(blank=True, null=True)
    strong_time_max = models.IntegerField(blank=True, null=True)
    moderate_time_min = models.IntegerField(blank=True, null=True)
    moderate_time_max = models.IntegerField(blank=True, null=True)
    weak_time_min = models.IntegerField(blank=True, null=True)
    weak_time_max = models.IntegerField(blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tools_account_actions'


class Logs(models.Model):
    bot_id = models.TextField(blank=True, null=True)
    log = models.TextField(blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'logs'


class Tracks(models.Model):
    bot_id = models.TextField(blank=True, null=True)
    track = ArrayField(models.TextField(blank=True, null=True))
    date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tracks'