from flask import jsonify
from flask import Flask, request
import UrlAnalyzer

app = Flask(__name__)

@app.route('/analyze', methods=['Get'])
def analyze():
    url = request.args.get('url')
    response = UrlAnalyzer.AnalyzeUrl(url)
    return response

@app.route('/analyzer', methods=['Get'])
def analyzer():
    url="https://www.imdb.com/ap/signin?clientContext=134-8641719-9196331&openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.imdb.com%2Fap-signin-handler&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=imdb_us&openid.mode=checkid_setup&siteState=eyJvcGVuaWQuYXNzb2NfaGFuZGxlIjoiaW1kYl91cyIsInJlZGlyZWN0VG8iOiJodHRwczovL3d3dy5pbWRiLmNvbS8_cmVmXz1sb2dpbiJ9&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&&tag=imdbtag_reg-20"
    response = UrlAnalyzer.AnalyzeUrl(url)
    return response

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run()
#app.run("localhost", 4200)


