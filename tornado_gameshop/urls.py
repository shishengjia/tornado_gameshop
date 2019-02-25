from apps.users import urls as user_urls
from apps.Game import urls as game_urls


url_pattern = []

url_pattern += user_urls.url_pattern
url_pattern += game_urls.url_pattern
