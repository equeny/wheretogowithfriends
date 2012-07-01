from tornado.web import url

from apps.base.handlers import HomePageHandler


url_patterns = (
    url(r"/", HomePageHandler, name="home_page"),
)
