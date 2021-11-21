CREATE KEYSPACE IF NOT EXISTS  image_store WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 3 };

CREATE TABLE IF NOT EXISTS image_store.categories (
    category_id text,
    PRIMARY KEY (category_id)
);

CREATE TABLE IF NOT EXISTS image_store.images (
    category_id text,
    image_id text,
    image_base64 text,
    PRIMARY KEY (image_id, category_id)
);