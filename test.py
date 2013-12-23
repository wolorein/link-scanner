import tornado.ioloop
import tornado.web
import tornado.escape
import tornado.httpserver
import os.path
from mods import downloadurl

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("home.html")
		
class CheckHandler(tornado.web.RequestHandler):
	def post(self):
		resp = self.get_argument("resp")
		if not resp:
			self.redirect("/")
		self.render("check.html", resp = downloadurl("download", resp))	
	def get(self):
		self.redirect("/")
		
class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
        (r"/", MainHandler),
		(r"/check", CheckHandler),
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
			download_path=os.path.join(os.path.dirname(__file__), "download"),
            debug=True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)

def main():
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen("5000")
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
