import numpy as np
import base64
from locust import HttpUser, task, between

URL = "/api"


class User(HttpUser):
    categories = ['bird', 'horse', 'truck', 'airplane', 'cat', 'automobile', 'dog', 'ship', 'deer', 'frog']
    wait_time = between(0.1, 1)

    @staticmethod
    def _render_image(resp):
        category, base_str = resp["result"]

        bimg = base64.decodebytes(base_str.encode('utf-8'))
        img = np.frombuffer(bimg, dtype=np.uint8)
        img.resize((32, 32, 3))

        return category

    @task(5)
    def image_load_random(self):
        payload = {
            "method": "download",
            "jsonrpc": "2.0",
            "id": 0,
        }
        with self.client.post(URL, json=payload, catch_response=True) as resp:
            try:
                self._render_image(resp.json())

            except KeyError:
                resp.failure("failed to get image result!")

            except Exception:
                resp.failure("failed to convert to image!")

    @task(5)
    def image_load_selected(self):
        c = np.random.choice(self.categories)
        payload = {
            "method": "download",
            "params": {"category_id": c},
            "jsonrpc": "2.0",
            "id": 0,
        }
        with self.client.post(URL, json=payload, catch_response=True) as resp:
            category = None
            try:
                category = self._render_image(resp.json())

            except KeyError:
                resp.failure("failed to get image result!")

            except Exception as e:
                print(repr(e))
                resp.failure(f"failed to convert to image! {repr(e)}")

            if category != c:
                resp.failure(f"invalid category! got {category} expected {c}")

    @task
    def list_categories(self):
        payload = {
            "method": "listCategories",
            "jsonrpc": "2.0",
            "id": 0,
        }
        with self.client.post(URL, json=payload, catch_response=True) as resp:
            try:
                if set(resp.json()["result"]) != set(self.categories):
                    resp.failure("invalid category list!")

            except KeyError:
                resp.failure("failed to get categories result!")
