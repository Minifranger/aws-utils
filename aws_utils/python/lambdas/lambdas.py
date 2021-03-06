import json
import logging
import re
from functools import wraps

from utils import DecimalEncoder

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Lambdas(object):

    class Decorators(object):
        @classmethod
        def output(cls, f):
            @wraps(f)
            def wrapper(*args, **kwargs):
                result = f(*args, **kwargs)
                return {'statusCode': result.get('ResponseMetadata').get('HTTPStatusCode'),
                        'headers': kwargs.get('headers'), 'body': json.dumps(result, cls=DecimalEncoder)}
            return wrapper

        @classmethod
        def payload(cls, id='id', load=True):
            def decorator(f):
                @wraps(f)
                def wrapper(self, event, *args, **kwargs):
                    logger.info('Received payload : {payload}'.format(payload=event))

                    body = event.get('body')
                    if load:
                        body = json.loads(body) if body else dict()
                    if body and id and not body.get(id):
                        raise ValueError('You should provide a {id} key to your body'.format(id=id))
                    if event.get('pathParameters') and id and not event.get('pathParameters').get(id):
                        raise ValueError('You should provide a {id} key to your pathParameters'.format(id=id))
                    kwargs.update({'body': body, 'path': event.get('pathParameters'),
                                   'query': event.get('queryStringParameters')})

                    logger.info('Payload have been loaded into kwargs : {kwargs}'.format(kwargs=kwargs))
                    return f(self, event, *args, **kwargs)
                return wrapper
            return decorator

        @classmethod
        def cors(cls, ips=None):
            if ips is None:
                ips = []

            def decorator(f):
                @wraps(f)
                def wrapper(self, event, *args, **kwargs):
                    logger.info('Incoming event : {event}'.format(event=event))
                    if any(re.compile(ip).match(event.get('headers').get('origin')) for ip in ips):
                        kwargs.update({'headers': {'Access-Control-Allow-Origin': event.get('headers').get('origin')}})

                    else:
                        raise ValueError('{origin} is not cors authorised'.format(origin=event.get('headers').get('origin')))
                    return f(self, event, *args, **kwargs)
                return wrapper
            return decorator

        @classmethod
        def limit(cls, length=10):
            def decorator(f):
                @wraps(f)
                def wrapper(event, *args, **kwargs):
                    result = f(event, *args, **kwargs)
                    return result[:length]
                return wrapper
            return decorator
