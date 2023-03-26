class DestinationAddView(TemplateView):
    template_name = "components/destination_lists_add.html"

def get_context_data(self, **kwargs):
    model = Bots
    all_bots = model.objects.raw('''SELECT * FROM bots LEFT OUTER JOIN groups ON bots.login = groups.bot_id;''')
    # all_bots = model.objects.values_list('login')
    # print(all_bots.query)
    bots_db_view = {}
    for i in all_bots:
        if i.login not in bots_db_view:
            bots_db_view[i.login] = []
        if i.link is not None:
            bots_db_view[i.login].append(i.link)
    # for i in bots_db_view:
    #    print(bots_db_view[i])
    # bots_db_view = json.dumps(bots_db_view)
    # print(bots_db_view)
    context = super(DestinationAddView, self).get_context_data(**kwargs)
    context.update({'title': "Destination Lists Add"})
    context.update({"all_bots": bots_db_view})
    # context.update({'all_groups': bots_db_view})

    return context