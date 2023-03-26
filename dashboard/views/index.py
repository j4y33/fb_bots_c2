from django.db.models import Count
from django.db.models.functions import TruncDay
from django.views.generic import TemplateView
from dashboard.forms.index_from import IndexForm
from dashboard.models import Bots, Action


class IndexView(TemplateView):
    form_class = IndexForm
    template_name = "components/index.html"

    def get_context_data(self, **kwargs):
        model = Bots
        total_blocked = model.objects.filter(total_errors__gte=3).count()
        total_active = model.objects.filter(total_errors__lte=2).count()
        total_paused = 0
        total = model.objects.count()
        actions = Action
        # total_actions = actions.objects.all()
        total_actions = actions.objects.annotate(day=TruncDay('date')) \
            .values('day').annotate(total_act=Count('id')).filter(action_id='like')

        context = super(IndexView, self).get_context_data(**kwargs)
        context.update({'title': "Dashboard"})

        bots_status_data = ({"label": "BLOCKED", "total": total_blocked},
                            {"label": "ACTIVE", "total": total_active},
                            {"label": "INACTIVE/PAUSED", "total": total_paused})
        context.update({'bots_status': bots_status_data})
        context.update({'total_actions': total_actions})
        context.update({'select_campaign': self.form_class})
        return context
