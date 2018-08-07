import datetime
import itertools
import metadata_parser
from celery import Celery
from bson import ObjectId

from models import connection

app = Celery('tasks', broker='amqp://guest@rabbit//')
convert_to_list = lambda l: l if isinstance(l, list) else [l]

@app.task
def scrape(url_id):
    d = connection.OpenGraphTag.one({"_id": ObjectId(url_id)})
    try:
        og = metadata_parser.MetadataParser(d['url'])
        d['url'] = og.get_metadata('url', 'og')
        d['type'] = og.get_metadata('type', 'og')
        d['title'] = og.get_metadata('title', 'og')
        im_url = convert_to_list(og.get_metadata('image', 'og'))
        im_type = convert_to_list(og.get_metadata('image:type', 'og'))
        im_width = convert_to_list(og.get_metadata('image:width', 'og'))
        im_height = convert_to_list(og.get_metadata('image:height', 'og'))
        im_alt = convert_to_list(og.get_metadata('image:alt', 'og'))
        for url, ty, width, height, alt in itertools.izip_longest(im_url, im_type, im_width, im_height, im_alt):
            d['image'].append({
                'url': url,
                'type': ty,
                'width': int(width),
                'height': int(height),
                'alt': alt
            })

        d['scrape_status'] = 'done'
    except:
        d['scrape_status'] = 'error'
    finally:
        d['updated_time'] = datetime.datetime.utcnow()
        d.save()
