from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import make_turn, add_new_game, get_turns

urlpatterns = {
    url(r'^newgame/$', add_new_game),
    url(r'^maketurn/$', make_turn),
    url(r'^getturns/(?P<game_id>\d+)/$', get_turns),
}

urlpatterns = format_suffix_patterns(urlpatterns)
