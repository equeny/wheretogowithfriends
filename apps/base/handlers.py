from tornado.web import RequestHandler
from jinja2 import Environment, ChoiceLoader


class BaseHandler(RequestHandler):

    def initialize(self):
        self.db = self.application.db
        self.jinja_env = Environment(loader=ChoiceLoader(self.settings['template_dirs']))

    def jinja_render(self, template_name, **kwargs):

        # Args from original render
        args = dict(
            handler=self,
            request=self.request,
            current_user=self.current_user,
            locale=self.locale,
            _=self.locale.translate,
            static_url=self.static_url,
            xsrf_form_html=self.xsrf_form_html,
            reverse_url=self.reverse_url
        )
        args.update(self.ui)

        args.update(kwargs)
        template = self.jinja_env.get_template(template_name)

        self.finish(template.render(**args))


class HomePageHandler(BaseHandler):
    def get(self):
        self.jinja_render("home_page.html")
