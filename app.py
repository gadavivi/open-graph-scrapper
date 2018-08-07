import datetime
from flask import Flask, redirect, url_for, request, jsonify, abort
import json
from bson import ObjectId
import metadata_parser

from tasks import scrape
from models import connection

app = Flask(__name__)


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime.datetime):
            return str(o)
        return json.JSONEncoder.default(self, o)


@app.route('/stories', methods=['POST'])
def new_ob():
    try:
        url = metadata_parser.MetadataParser(request.args.get('url')).get_discrete_url()
    except:
        return abort(400)

    d = connection.OpenGraphTag.one({'url': url})
    if not d:
        d = connection.OpenGraphTag()
        d['url'] = url
        d.save()
    if d['scrape_status'] != 'done':
        scrape.delay(str((d['_id'])))

    return JSONEncoder().encode(d['_id'])


@app.route('/stories/<url_id>', methods=['GET'])
def get_og(url_id):
    d = connection.OpenGraphTag.one({"_id": ObjectId(url_id)})
    if d:
        return JSONEncoder().encode(d)

    return abort(404)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
