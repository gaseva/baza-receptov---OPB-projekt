from presentation.bottleext import get, post, run, request, template, redirect, static_file, url, response, template_user
import os

# privzete nastavitve
SERVER_PORT = os.environ.get('BOTTLE_PORT', 8080)
RELOADER = os.environ.get('BOTTLE_RELOADER', True)

@get('/')
def test():
    return template("test1.html")

run(host='localhost', port=SERVER_PORT, reloader=RELOADER, debug=True)