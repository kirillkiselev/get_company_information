# -*- coding: utf-8 -*-
import json
import requests
import zmq
from error import ParseError


API_KEY = 'YOUR_API_KEY'  # How to get API key see on https://dadata.ru/api/suggest/#request
BASE_URL = 'https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/%s'


def get_party(query):
    """Send POST request on dadata.ru use suggest API.
    See more information in https://dadata.ru/api/suggest/.

    Parameters
    ----------
    :query: str
        Criteria of search : inn or ogrn

    :return: json object
    """

    url = BASE_URL % 'party'
    headers = {
        'Authorization': 'Token %s' % API_KEY,
        'Content-Type': 'application/json',
    }
    data = {
        'query': query
    }
    r = requests.post(url, data=json.dumps(data), headers=headers)
    return r.json()


def run_server():
    """Run server for receive and send messages
    More information about ZeroMQ in http://zguide.zeromq.org/"""
    context = zmq.Context()
    socket = context.socket(zmq.REP)  # Socket to talk to client
    socket.bind('tcp://127.0.0.1:43000')
    while True:
        try:
            message = socket.recv_string()
            if message:
                print('Recieved message %s' % message)

                type, query = message.split()
                if type == 'GET' and query:  # Check message format, it should look: 'GET query'

                    if not query.isdigit():
                        raise TypeError('{0} is not a number'.format(query))

                    data = get_party(query)
                    socket.send_json(data['suggestions'][0]['data'], ensure_ascii=False)
                else:
                    raise ParseError('wrong format message(%s), it should look \'GET query\'' % message)
        except zmq.ZMQError as err:
            socket.send_string('ZMQError: {0}'.format(err.errno))
            raise
        except TypeError as err:
            socket.send_string('TypeError: {0}'.format(err))
            print(err)
        except ParseError as err:
            socket.send_string('ParseError: {0}'.format(err.message))
            print(err)
        except Exception as err:
            socket.send_string('Error: {0}'.format(err))
            print(err)
        else:
            print('Send JSON in client is successful')
