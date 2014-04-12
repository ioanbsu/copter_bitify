__author__ = 'ivanbahdanau'

import web



urls = (
    '/(.*)', 'hello'
)
app = web.application(urls, globals())

class hello:
    def GET(self, name):
        power=str(web.input()['power'])
        fl_val=float(web.input()['fl'])
        if not name:
            name = 'world'
        return 'Hello, ' + name + '!'

if __name__ == "__main__":
    app.run()