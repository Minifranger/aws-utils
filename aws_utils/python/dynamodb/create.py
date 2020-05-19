import json
import logging
import boto3
from utils import DecimalEncoder, success, failure, validate_params

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

client = boto3.resource('dynamodb')


def create(event, context, **kwargs):
    # logger.info('event : {event}'.format(event=event))
    # body, = validate_params(body=event.get('body'))
    #
    # body = json.loads(body) if isinstance(body, str) else body
    # if not body.get('id'):
    #     return failure(code=400, body='You should provide a reminder id to your payload')

    # params = {
    #     'TableName': table,
    #     'Item': body
    # }
    key, params = kwargs.get('key'), kwargs.get('params')

    logger.info('Creating item {key}'.format(key=key))

    try:
        client.Table(params.get('TableName')).put_item(**params)
    except Exception as e:
        return failure(body=e)

    logger.info('Created item {key}'.format(key=key))
    return success(body=json.dumps(params['Item'], cls=DecimalEncoder))
