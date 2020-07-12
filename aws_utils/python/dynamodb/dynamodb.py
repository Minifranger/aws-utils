import logging
import os
import boto3


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class DynamoDB(object):
    __CLIENT__ = boto3.resource('dynamodb')

    def __init__(self, **kwargs):
        if not kwargs.get('__DYNAMODB_TABLE__'):
            kwargs.update({'__DYNAMODB_TABLE__': os.environ['__DYNAMODB_TABLE__']})
        self.__TABLE__ = self.__CLIENT__.Table(kwargs.get('__DYNAMODB_TABLE__'))

    def scan(self, **kwargs):
        logger.info('Getting all items')

        result = self.__TABLE__.scan(**kwargs)

        logger.info('Retrieved all items')
        return result

    def put(self, **kwargs):
        logger.info('Creating item {item}'.format(item=kwargs.get('Item')))

        result = self.__TABLE__.put_item(**kwargs)

        logger.info('Created item {item}'.format(item=kwargs.get('Item')))
        return result

    def get(self, **kwargs):
        logger.info('Getting item {key}'.format(key=kwargs.get('Key')))

        result = self.__TABLE__.get_item(**kwargs)

        logger.info('Retrieved item {key}'.format(key=kwargs.get('Key')))
        return result
