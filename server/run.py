import os
import time
from argparse import ArgumentParser

from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple
from werkzeug.exceptions import NotFound

from jsonrpc import JSONRPCResponseManager, dispatcher

from cas_ops import get_categories, get_random_category, get_random_image


@dispatcher.add_method
def listCategories():
    return get_categories()


@dispatcher.add_method
def upload(category, image_bs64):
    raise NotFound()


@dispatcher.add_method
def download(category_id=None):
    if category_id is None:
        category_id = get_random_category()
    return category_id, get_random_image(category_id)


@Request.application
def application(request):
    response = JSONRPCResponseManager.handle(
        request.data, dispatcher)
    return Response(response.json, mimetype='application/json')


if __name__ == '__main__':
    parser = ArgumentParser()

    parser.add_argument("--host", help="Server host address.")
    parser.add_argument("--port", help="Server run port.")

    args = parser.parse_args()

    run_simple(args.host, int(args.port), application)
