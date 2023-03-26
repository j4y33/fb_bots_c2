from sqlalchemy import MetaData, Table, Column, String, Integer, Boolean, Date, ForeignKey, func, or_, not_, and_, Text
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import sqlalchemy as db
from collections import defaultdict


# Print raw sql(remove al select from the end of the query)
# from sqlalchemy.dialects import postgresql
# print(str(posts.statement.compile(dialect=postgresql.dialect())))
#from scheduler.launcher import InstancesLauncher


class CampaignsScheduler:
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

    def campaigns(self):
        posts_for_launch = defaultdict(list)
        week = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']
        self.session = Session(bind=self.connection)
        scheduler = self.session.query(Scheduler, Campaigns, CampaignsPosts, CampaignsWhereToPublish, DstLists)\
            .filter(Scheduler.campaign_id == Campaigns.id, )\
            .filter(and_(CampaignsPosts.campaign_id == Campaigns.id, CampaignsPosts.status != 'done', ))\
            .filter(or_(func.array_length(CampaignsPosts.posted, 1) < CampaignsPosts.published_by,
                        func.array_length(CampaignsPosts.posted, 1) == None))\
            .filter(CampaignsWhereToPublish.campaign_id == Campaigns.id, )\
            .filter(CampaignsWhereToPublish.dst_lists == DstLists.dst_name).all()

        #from sqlalchemy.dialects import postgresql
        #print(str(scheduler.statement.compile(dialect=postgresql.dialect())))

        for campaign in scheduler:
            print('Start process campaign id: {0}'.format(campaign[0].campaign_id))
            # Check Campaign for errors
            if campaign[1].stop_after_single_error:
                print(len(campaign[1].errors))
                if len(campaign[1].errors) > 0:
                    print('Campaign id: {0}, name: {1} has more than 1 error, break'.format(campaign[1].id, campaign[1].campaign_name))
                    break

            if campaign[1].stop_campaign_after_errors:
                print(len(campaign[1].errors))
                if len(campaign[1].errors) > 5:
                    print('Campaign id: {0}, name: {1} has errors, break'.format(campaign[1].id, campaign[1].campaign_name))
                    break

            if campaign[1].do_not_publish_in_parallel:
                # Check running bots
                if len(campaign[2].running) > 0:
                    print('Campaign already running, '
                          'do_not_publish_in_parallel=True, '
                          'campaign id: {0}, name: {1}'.format(campaign[1].id, campaign[1].campaign_name))
                    break

            for day in campaign[0].operate_on:
                # Check launch day
                if week[datetime.today().weekday()] == day:
                    # Check launch time
                    if self.time_in_range(campaign[0].post_interval_start, campaign[0].post_interval_finish,
                                          datetime.now().strftime('%H:%M')):
                        # Start launch proccess
                        # Check for avalliable posts and posted status
                        # Check maximum posts per-day
                        print('Process campaign, campaign id: {0}, name: {1}'.format(campaign[1].id, campaign[1].campaign_name))

                        print('Process bots: {0}, from dst list: {1}'.format(campaign[4].profiles,
                                                                             campaign[4].dst_name))
                        for bot in campaign[4].profiles:
                            print(len(campaign[2].posted) + len(campaign[2].running))
                            if len(campaign[2].posted) + len(campaign[2].running) >= campaign[2].published_by:
                                print('Reached maximum bot numbers for this campaign:'
                                      ' {0}, {1}'.format(campaign[1].id,campaign[1].campaign_name))
                                break
                            if bot not in campaign[2].posted and bot not in campaign[2].running:
                                # Check bot used status, if true, skip
                                bot_status = self.session.query(Bots).filter(
                                    Bots.login == bot, ).scalar()
                                if bot_status.used_status:
                                    print('Bot: {0}, running, skip'.format(bot))
                                else:
                                    # Update running list for this post
                                    bot_status.used_status = True
                                    campaign[2].running = campaign[2].running + [bot]
                                    self.session.commit()
                                    posts_for_launch[bot].append(campaign[2].id)

        for bot in posts_for_launch:
            print('Launch bot: {0}, posts: {1}'.format(bot, posts_for_launch[bot]))
            self.launcher.launch_instance(bot, 'post', posts_for_launch[bot])
        print('Finish')


Base = declarative_base()


class Bots(Base):
    __tablename__ = 'bots'
    login = Column(Text, primary_key=True)
    total_errors = Column(Integer)
    used_status = Column(Boolean)


class Scheduler(Base):
    __tablename__ = 'campaigns_scheduler'
    campaign_id = Column(Integer)
    posts_per_day = Column(Integer)
    post_interval_start = Column(Text)
    post_interval_finish = Column(Text)
    randomise_interval_each_day = Column(Boolean)
    randomise_number_of_posts = Column(Boolean)
    maximum_randomise_posts = Column(Integer)
    wait = Column(Boolean)
    wait_before_publishing_with_same_account = Column(Integer)
    rotate_weekdays_randomly = Column(Boolean)
    operate_on = Column(ARRAY(Text))
    date = Column(Date)
    id = Column(Integer, primary_key=True)


#    def __repr__(self):
#        return "<Customer(name='%s', age='%s', email='%s', address='%s', zip code='%s')>" % (
#        self.campaign_id, self.age, self.email, self.address, self.zip_code)


class Campaigns(Base):
    __tablename__ = "campaigns"
    id = Column(Integer, ForeignKey("campaigns_scheduler.campaign_id"), primary_key=True)
    campaign_name = Column(Text)
    description = Column(Text)
    dst_lists = Column(ARRAY(Text))
    errors = Column(ARRAY(Text))
    stop_after_single_error = Column(Boolean)
    do_not_publish_in_parallel = Column(Boolean)
    stop_campaign_after_errors = Column(Boolean)
    date = Column(Date)


class DstLists(Base):
    __tablename__ = "destination_lists"
    id = Column(Integer, primary_key=True)
    dst_name = Column(String)
    profiles = Column(ARRAY(Text))
    campaigns = Column(ARRAY(Text))
    walls = Column(ARRAY(Text))
    date = Column(Date)


class CampaignsPosts(Base):
    __tablename__ = "campaigns_posts"
    id = Column(Integer, primary_key=True)
    campaign_id = Column(Integer)
    post_text = Column(Text)
    content = Column(Text)
    status = Column(Text)
    src = Column(Text)
    published_by = Column(Integer)
    date = Column(Date)
    running = Column(ARRAY(Text))
    posted = Column(ARRAY(Text))
    posted_groups = Column(ARRAY(Text))
    posted_walls = Column(ARRAY(Text))

class CampaignsWhereToPublish(Base):
    __tablename__ = "campaigns_where_to_publish"
    id = Column(Integer, primary_key=True)
    campaign_id = Column(Integer)
    dst_lists = Column(Text)
    date = Column(Date)


# Saved SQL
'''posts = self.session.query(CampaignsPosts).filter(
    CampaignsPosts.campaign_id == plan[0].campaign_id,
    CampaignsPosts.status != 'done'
).filter(or_(
    and_(
        func.array_length(CampaignsPosts.posted, 1) < CampaignsPosts.published_by,
        not_(CampaignsPosts.posted.contains([bot]))),
    func.array_length(CampaignsPosts.posted, 1) == None)).all()'''