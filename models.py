from mongokit import Document, Connection
import datetime

connection = Connection('db')


@connection.register
class OpenGraphTag(Document):
    __collection__ = 'tags'
    __database__ = 'og'
    structure = {
        'url': basestring,
        'type': basestring,
        'title': basestring,
        "image": [
            {
                "url": basestring,
                "type": basestring,
                "width": int,
                "height": int,
                "alt": basestring
            },
        ],
        'updated_time': datetime.datetime,
        'scrape_status': basestring,
    }
    default_values = {
        'type': None,
        'title': None,
        'image': [],
        'scrape_status': "pending",
        'updated_time': datetime.datetime.utcnow
    }