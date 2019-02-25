from tornado_gameshop.handler import BaseHandler
from apps.Game.model import GameTag, Game, Comment


class GameListHandler(BaseHandler):
    async def get(self, *args, **kwargs):
        re_data = {"games": [], "start": 0, "pagesize": 0, "total_count": 0}
        try:

            games_query = Game.extend()

            # 价格排序
            sort = self.get_argument("sort", None)
            if sort:
                if sort == "price_asc":
                    games_query = games_query.order_by(Game.price.asc())

                if sort == "price_desc":
                    games_query = games_query.order_by(Game.price.desc())

            # 分类
            tag = self.get_argument("tag", None)
            if tag:
                id = None
                game_tag = await self.application.objects.execute(GameTag.select().where(GameTag.name == tag))
                for item in game_tag:
                    id = item.id

                games_query = games_query.where(Game.tag == id)

            # 查询 起始 和 长度
            start = self.get_argument("start", None)
            count = self.get_argument("count", None)

            if start and count:
                games_query = games_query.paginate(int(start), int(count))
                re_data["start"] = start
                re_data["pagesize"] = count
            else:
                pass

            games = await self.application.objects.execute(games_query)

            for game in games:
                re_data["games"].append({
                    "id": game.id,
                    "name": game.name,
                    "cover_url": game.cover_url,
                    "price": game.price,
                })
            self.set_status(200)
            re_data["success"] = True
        except:
            self.set_status(404)
            re_data["success"] = False

        self.finish(re_data)


class GameDetailHandler(BaseHandler):
    """
    游戏详情
    """
    async def get(self, _id, *args, **kwargs):
        re_data = {}
        try:
            _game = await self.application.objects.execute(Game.select().where(Game.id == _id))

            if _game:
                for game in _game:
                    re_data["game"] = {
                        "name": game.name,
                        "desc": game.desc,
                        "os": game.os,
                        "game_scree_shot_1": game.game_scree_shot_1,
                        "game_scree_shot_2": game.game_scree_shot_2,
                        "game_scree_shot_3": game.game_scree_shot_3
                    }
                re_data["success"] = True
                self.set_status(200)
            else:
                self.set_status(404)
                re_data = {"success": False}
        except:
            self.set_status(404)
            re_data = {"success": False}

        self.finish(re_data)


class GameTagsHandler(BaseHandler):
    """
    返回所有游戏标签
    """
    async def get(self, *args, **kwargs):
        re_data = {"count": 0, "tags": []}

        try:
            count = await self.application.objects.count(GameTag.select())
            re_data["count"] = count

            tags = await self.application.objects.execute(GameTag.select())
            for tag in tags:
                re_data["tags"].append(tag.name)
            self.set_status(200)
            re_data["success"] = True
        except:
            self.set_status(404)
            re_data["success"] = False

        self.finish(re_data)


class GameCommentsHandler(BaseHandler):
    """
    获取游戏评论
    """
    async def get(self, _id, *args, **kwargs):
        re_data = {"comments": []}
        comment_query = Comment.extend()
        try:
            comment_query = comment_query.where(Comment.game.id == _id)

            comments = self.application.objects.execute(comment_query)

            for comment in comments:
                re_data["comments"].append(comment.comment)
            self.set_status(200)

        except:
            self.set_status(404)
            re_data["success"] = False

        self.finish(re_data)





