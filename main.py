import sys
import os.path
import tornado.ioloop
import tornado.web
import tornado.options
from tornado.options import define, options
from pymongo import Connection
from jinja2 import FileSystemLoader, PackageLoader
from utils.importlib import import_module

define("port", default=8000, help="run on the given port", type=int)
define("db_host", default="127.0.0.1", help="database host")
define("db_port", default=27017, help="database port", type=int)
define("db_name", default="wheretogowithfriends", help="database name")

PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))
sys.path.append(os.path.join(PROJECT_PATH, 'apps'))

INSTALLED_APPS = (
    'base',
)

TEMPLATE_DIRS = [
    FileSystemLoader(os.path.join(PROJECT_PATH, 'templates')),
]
TEMPLATE_DIRS.extend([PackageLoader(app_name) for app_name in INSTALLED_APPS])


class Application(tornado.web.Application):

    def __init__(self):

        handlers = []

        for app_name in INSTALLED_APPS:
            app_urls = import_module("%s.urls" % app_name)
            handlers += app_urls.url_patterns

        settings = dict(
            cookie_secret="43oETzKXQAGajopaeJJFuYh7EQnptrololo2XdTP1o/Vo=",
            static_path=os.path.join(PROJECT_PATH, 'static'),
            xsrf_cookies=True,
            template_dirs=TEMPLATE_DIRS,
        )

        tornado.web.Application.__init__(self, handlers, **settings)

        # Have one global connection to the DB across all handlers
        self.db_connection = Connection(
            host=options.db_host,
            port=options.db_port,
            max_pool_size=5
        )

        self.db = self.db_connection[options.db_name]


if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
