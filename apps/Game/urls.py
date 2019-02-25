from tornado.web import url
from apps.Game.handler import GameListHandler, GameTagsHandler, GameDetailHandler
url_pattern = (
    url("/v1/games/?", GameListHandler),
    url("/v1/game_tags/?", GameTagsHandler),
    url("/v1/game/(?P<_id>\d+)/?", GameDetailHandler),
    url("/v1/game/(?P<_id>\d+)/comments/?", GameDetailHandler)
)