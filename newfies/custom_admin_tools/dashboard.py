"""This file was generated with the customdashboard management command, it
contains the two classes for the main dashboard and app index dashboard.
You can customize these classes as you want.

To activate your index dashboard add the following to your settings.py::
    ADMIN_TOOLS_INDEX_DASHBOARD = 'dashboard.CustomIndexDashboard'

And to activate the app index dashboard::
    ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'dashboard.CustomAppIndexDashboard'"""
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from admin_tools.dashboard import modules, Dashboard, AppIndexDashboard
from admin_tools.utils import get_admin_site_name


class HistoryDashboardModule(modules.LinkList):
    title = 'History'

    def init_with_context(self, context):
        request = context['request']
        # we use sessions to store the visited pages stack
        history = request.session.get('history', [])
        for item in history:
            self.children.append(item)
        # add the current page to the history
        history.insert(0, {
            'title': context['title'],
            'url': request.META['PATH_INFO'],
        })
        if len(history) > 10:
            history = history[:10]
        request.session['history'] = history


class CustomIndexDashboard(Dashboard):
    """Custom index dashboard"""

    def init_with_context(self, context):

        request = context['request']

        # we want a 3 columns layout
        self.columns = 3

        site_name = get_admin_site_name(context)

        #self.children.append(
        #            HistoryDashboardModule()
        #)

        # append an app list module for "Administration"
        self.children.append(modules.AppList(
            _('Administration'),
            models=('django.contrib.*', 'user_profile.*', ),
        ))

        self.children.append(modules.AppList(
            _('Settings'),
            models=('dialer_settings.*', ),
        ))

        # append an app list module for "Dialer"
        self.children.append(modules.AppList(
            _('Task Manager'),
            models=('djcelery.*', ),
        ))

        # append an app list module for "Dialer"
        self.children.append(modules.AppList(
            _('Voip Dialer'),
            models=('dialer_cdr.*', 'dialer_gateway.*', 'dialer_campaign.*', ),
        ))

        # append an app list module for "Dialer"
        self.children.append(modules.AppList(
            _('Voip Server'),
            models=('voip_app.*', ),
        ))

        # append an app list module for "Country_prefix"
        self.children.append(modules.AppList(
            _('DialCode'),
            models=('prefix_country.*', ),
        ))

        # append a link list module for "quick links"
        self.children.append(modules.LinkList(
            _('Quick links'),
            layout='inline',
            draggable=True,
            deletable=True,
            collapsible=True,
            children=[
                [_('Go to Newfies'), 'http://www.newfies-dialer.org/'],
                [_('Go to FreedomFone'), 'http://www.freedomfone.org/'],
                [_('Change password'),
                 reverse('%s:password_change' % site_name)],
                [_('Log out'), reverse('%s:logout' % site_name)],
            ],
        ))

        # append a recent actions module
        self.children.append(modules.RecentActions(_('Recent Actions'), 5))


        # append a feed module
        #self.children.append(modules.Feed(
        #    _('Latest Django News'),
        #    feed_url='http://www.djangoproject.com/rss/weblog/',
        #    limit=5
        #))


class CustomAppIndexDashboard(AppIndexDashboard):
    """Custom app index dashboard for admin."""

    # we disable title because its redundant with the model list module
    title = ''

    def __init__(self, *args, **kwargs):
        AppIndexDashboard.__init__(self, *args, **kwargs)

        # append a model list module and a recent actions module
        self.children += [
            modules.ModelList(self.app_title, self.models),
            modules.RecentActions(
                _('Recent Actions'),
                include_list=self.get_app_content_types(),
                limit=5,
            ),
        ]

    def init_with_context(self, context):
        """Use this method if you need to access the request context."""
        return super(CustomAppIndexDashboard, self).init_with_context(context)
