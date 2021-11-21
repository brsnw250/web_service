import os
from time import sleep
from random import randint

from cassandra.cluster import Cluster, ExecutionProfile, EXEC_PROFILE_DEFAULT, NoHostAvailable
from cassandra.policies import (
    DowngradingConsistencyRetryPolicy,
    ConsistencyLevel
)


def init_session(cas_hostname=None, max_retr=10, sleep_sec=10):
    cas_hostname = "127.0.0.1" if cas_hostname is None else cas_hostname

    consist_map = ConsistencyLevel.name_to_value

    consist_level = consist_map[os.environ["CONSISTENCY_LEVEL"]]
    serial_consist_level = consist_map[os.environ["SERIAL_CONSISTENCY_LEVEL"]]

    profile = ExecutionProfile(
        consistency_level=consist_level,
        serial_consistency_level=serial_consist_level,
        request_timeout=15
    )

    t = 0
    while True:
        try:
            cluster = Cluster(
                [cas_hostname],
                execution_profiles={EXEC_PROFILE_DEFAULT: profile}
            )
            return cluster.connect()
        except NoHostAvailable as e:
            t += 1
            if t == max_retr:
                raise e
            print(f"No host avaliable @ {cas_hostname}! sleeping for {sleep_sec}s")
            sleep(sleep_sec)


SESSION = init_session(
    os.environ.get("CASSANDRA_HOST", "localhost")
)


def get_categories(session=None):
    if session is None:
        session = SESSION

    q_res = session.execute("SELECT * FROM image_store.categories")
    cat_names = [r.category_id for r in q_res]
    return cat_names


def get_random_category(session=None):
    if session is None:
        session = SESSION

    q_res = session.execute("SELECT min(token(category_id)) as a, max(token(category_id)) as b FROM image_store.categories")

    a, b = [(r.a, r.b) for r in q_res][0]

    rand_seed = randint(a, b)

    q_res = session.execute(f"SELECT * FROM image_store.categories WHERE token(category_id) >= {rand_seed} LIMIT 1")

    cat_name = q_res.current_rows[0].category_id

    return cat_name


def get_random_image(category_id, session=None):
    if session is None:
        session = SESSION

    q_res = session.execute(
        f"SELECT min(token(image_id)) as a, max(token(image_id)) as b FROM image_store.images where category_id = '{category_id}' ALLOW FILTERING"
    )

    a, b = [(r.a, r.b) for r in q_res][0]

    rand_seed = randint(a, b)

    q_res = session.execute(f"SELECT image_base64 FROM image_store.images where token(image_id) >= {rand_seed} and category_id = '{category_id}' limit 1 ALLOW FILTERING")
    image_b64 = q_res.current_rows[0].image_base64

    return image_b64
