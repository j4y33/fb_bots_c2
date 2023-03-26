import random
import time
from sqlalchemy import MetaData, Table, Column, String, Integer, Boolean, Date, ForeignKey, func, or_, not_, and_, Text
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import sqlalchemy as db
from datetime import date


class Tools:
    engine = db.create_engine('postgresql://bot:Dsirfbot294r2r@3.126.146.115:5432/dsirf')

    def __init__(self, launcher):
        self.launcher = launcher
        self.connection = self.engine.connect()
        print("DB Instance created")

    def time_in_range(self, start, end, x):
        """Return true if x is in the range [start, end]"""
        if start <= end:
            return start <= x <= end
        else:
            return start <= x or x <= end

    def tools(self):
        week = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']
        self.session = Session(bind=self.connection)
        scheduler = self.session.query(ToolsJoiner, ToolsDestinationLists, ToolsFindGroups) \
            .filter(ToolsJoiner.dst_id == ToolsDestinationLists.id, ).all()
        for settings in scheduler:
            # Joiner
            for day in settings[0].operate_on:
                # Check launch day
                if week[datetime.today().weekday()] == day:
                    # Check launch time
                    if self.time_in_range(settings[0].execute_between, settings[0].execute_between_and,
                                          datetime.now().strftime('%H:%M')):
                        # Start launch process
                        print('Process joiner id: {0}, name: {1}'.format(settings[1].id, settings[1].dst_name))

                        print('Process bots: {0}, from dst list: {1}'.format(settings[1].profiles,
                                                                             settings[1].dst_name))
                        # Check tools find groups status True/Flase

                        # Joiner start
                        print('Joiner')
                        # Check groups per day
                        actions = self.session.query(Action).filter(
                            and_(Action.groups_id == settings[0].dst_id, Action.action_id == 'join_group',
                                 Action.date == date.today())).all()
                        total_bots_actions = len(actions)
                        if settings[1].running is not None:
                            total_bots_actions = len(settings[1].running) + len(actions)
                        if settings[0].auto_stop_peer_day \
                                and total_bots_actions >= settings[0].reaching_groups_peer_day:
                            print('Reached maximum daily limit for joining groups')
                        else:
                            for bot in settings[1].profiles:
                                # And bot used status False
                                bot_status = self.session.query(Bots).filter(
                                    Bots.login == bot, ).scalar()

                                if bot not in settings[1].running and not bot_status.used_status:
                                    join_groups_per_day = random.randint(settings[0].join_between_peer_day,
                                                                         settings[0].join_between_and_peer_day)
                                    bot_actions = self.session.query(Action).filter(
                                        and_(Action.bot_id == bot, Action.action_id == 'join_group',
                                             Action.date == date.today())).all()
                                    if len(bot_actions) < join_groups_per_day:
                                        join_actions_for_bot = join_groups_per_day - len(bot_actions)
                                        groups_for_join = []
                                        extracted_groups = self.session.query(ToolsExtractedGroups) \
                                            .filter(ToolsExtractedGroups.dst_id == settings[0].dst_id, ) \
                                            .filter(and_(not_(ToolsExtractedGroups.joined.contains([bot])),
                                                         not_(ToolsExtractedGroups.bot_error.contains([bot])), )).all()
                                        for group in extracted_groups:
                                            if join_actions_for_bot == 0:
                                                break
                                            print(group.url)
                                            groups_for_join.append(group.url)
                                            join_actions_for_bot -= 1
                                        if groups_for_join:
                                            self.launcher.launch_instance(bot, 'join_group', groups_for_join)
                                            # Update running list for this post
                                            bot_status.used_status = True
                                            settings[1].running = settings[1].running + [bot]
                                            self.session.commit()
                                            print('Launch bot: {0}'.format(bot))
                                            time.sleep(10000)
                                            if settings[0].wait_between is not None and \
                                                    settings[0].wait_between_and is not None:
                                                time.sleep(random.randint(settings[0].wait_between,
                                                                          settings[0].wait_between_and))
                                        else:
                                            print('Nothing to join, bot: {0}'.format(bot))
                                else:
                                    print("Bot {0} running, skip!".format(bot))
                        if settings[2].status:
                            # Finder start
                            print('Finder')
                            if settings[1].extraction is None:
                                print("Start extraction")
                                # Add bot to dst extraction
                                print('Configuration ID: {0}'.format(settings[2].id))
                                # Remove bot from dst extraction
                                # Update tools find groups status True
                            else:
                                print('Wait...')

                        # if bot not in campaign[2].posted and bot not in campaign[2].running:


Base = declarative_base()


class Bots(Base):
    __tablename__ = 'bots'
    login = Column(Text, primary_key=True)
    total_errors = Column(Integer)
    used_status = Column(Boolean)


# Actions
class Action(Base):
    __tablename__ = "action"
    id = Column(Integer, primary_key=True)
    bot_id = Column(Text)
    groups_id = Column(Integer)
    dst_id = Column(Integer)
    action_priority = Column(Text)
    action_id = Column(Text)
    action_status = Column(Boolean)
    image = Column(Text)
    date = Column(Date)


# Tools
class ToolsDestinationLists(Base):
    __tablename__ = "tools_destination_lists"
    id = Column(Integer)
    dst_name = Column(Text, primary_key=True)
    profiles = Column(ARRAY(Text))
    running = Column(ARRAY(Text))
    extraction = Column(Text)
    configuration = Column(Integer)
    date = Column(Date)


class ToolsJoiner(Base):
    __tablename__ = "tools_joiner"
    id = Column(Integer, primary_key=True)
    dst_id = Column(Integer)
    wait_between = Column(Integer)
    wait_between_and = Column(Integer)
    execute_between = Column(Text)
    execute_between_and = Column(Text)
    random_sleep_time = Column(Boolean)
    join_between = Column(Integer)
    join_between_and = Column(Integer)
    auto_stop = Column(Boolean)
    reaching_groups = Column(Integer)
    join_between_peer_day = Column(Integer)
    join_between_and_peer_day = Column(Integer)
    auto_stop_peer_day = Column(Boolean)
    reaching_groups_peer_day = Column(Integer)
    operate_on = Column(ARRAY(Text))
    date = Column(Date)


class ToolsFindGroups(Base):
    __tablename__ = "tools_find_groups"
    id = Column(Integer, primary_key=True)
    dst_id = Column(Integer)
    keywords = Column(ARRAY(Text))
    exclude_keywords = Column(ARRAY(Text))
    groups_extra_urls = Column(ARRAY(Text))
    min_users = Column(Boolean)
    en_gr_groups = Column(Boolean)
    opened_groups = Column(Boolean)
    admin_post = Column(Boolean)
    min_users_count = Column(Integer)
    status = Column(Boolean)
    date = Column(Date)


class ToolsExtractedGroups(Base):
    __tablename__ = "tools_extracted_groups"
    id = Column(Integer, primary_key=True)
    dst_id = Column(Integer)
    url = Column(Text)
    members = Column(Integer)
    activity_today = Column(Integer)
    activity_last_30 = Column(Integer)
    created = Column(Text)
    author = Column(Text)
    joined = Column(ARRAY(Text))
    bot_error = Column(ARRAY(Text))
    required_answer = Column(Boolean)
    admins = Column(ARRAY(Text))
    access = Column(Boolean)
    keywords = Column(ARRAY(Text))
    exclude_keywords = Column(ARRAY(Text))
    date = Column(Date)


class CommentsResults(Base):
    __tablename__ = "comments_results"
    id = Column(Integer, primary_key=True)
    dst_id = Column(Integer)
    keywords = Column(ARRAY(Text))
    exclude_keywords = Column(ARRAY(Text))
    posted_link = Column(Text)
    action_type = Column(Text)
    story_text = Column(Text)
    action_screen = Column(Text)
    date = Column(Date)


class CommentsSources(Base):
    __tablename__ = "comments_sources"
    id = Column(Integer, primary_key=True)
    dst_id = Column(Integer)
    comment_like_in_pages = Column(Boolean)
    comment_like_in_walls = Column(Boolean)
    comment_like_in_searches = Column(Boolean)
    keywords = Column(ARRAY(Text))
    exclude_keywords = Column(ARRAY(Text))
    comment_like_in_groups = Column(Boolean)
    comment_like_in_permalinks = Column(Boolean)
    url_text_area = Column(Text)
    date = Column(Date)


class CommentsSettings(Base):
    __tablename__ = "comments_settings"
    id = Column(Integer, primary_key=True)
    dst_id = Column(Integer)
    on_off = Column(Boolean)
    wait_between_start = Column(Integer)
    wait_between_end = Column(Integer)
    execute_between_start = Column(Text)
    execute_between_end = Column(Text)
    random_sleep_time = Column(Boolean)
    rotate_weekends_randomly = Column(Boolean)
    operate_on = Column(ARRAY(Text))
    comments_maximum_start = Column(Integer)
    comments_maximum_end = Column(Integer)
    comments_increasing_start = Column(Integer)
    comments_increasing_end = Column(Integer)
    maximum_single_source_per_day = Column(Boolean)
    comments_single_source_maximum_start = Column(Integer)
    comments_single_source_maximum_end = Column(Integer)
    comments_post_maximum_age = Column(Boolean)
    comments_maximum_days = Column(Integer)
    keywords = Column(ARRAY(Text))
    exclude = Column(ARRAY(Text))
    comment = Column(Text)
    date = Column(Date)
