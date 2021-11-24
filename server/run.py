from argparse import ArgumentParser

from typing import List, Optional

from flask import Flask
from flask_jsonrpc import JSONRPC

from cas_ops import get_categories, get_random_category, get_random_image


app = Flask("image-server")

jrpc = JSONRPC(app, "/api", enable_web_browsable_api=True)


@jrpc.method("listCategories")
def list_categories() -> List[str]:
    return get_categories()


# @jrpc.method("upload")
# def upload(category, image_bs64):
#     raise NotImplementedError()


@jrpc.method("download")
def download(category_id: Optional[str] = None) -> List[str]:
    if category_id is None:
        category_id = get_random_category()

    return [category_id, get_random_image(category_id)]


if __name__ == '__main__':
    parser = ArgumentParser()

    parser.add_argument("--host", help="Server host address.")
    parser.add_argument("--port", help="Server run port.")

    args = parser.parse_args()

    app.run(args.host, int(args.port), debug=True)
