from dotenv import load_dotenv
import os
import psycopg2

from faker import Faker
import random

fake = Faker()

SCHEMA_NAME = "video_games"

load_dotenv('./.env', override=True)

def_vars = [
    'DATABASE_USER', 'DATABASE_PASS',
    'DATABASE_HOST', 'DATABASE_PORT',
    'DATABASE_NAME',
]


def get_env_object():
    return {x: os.environ[x] for x in def_vars}


env_object: str = get_env_object()

conn = psycopg2.connect(
        host=env_object['DATABASE_HOST'],
        user=env_object['DATABASE_USER'],
        password=env_object['DATABASE_PASS'],
        dbname=env_object['DATABASE_NAME']
    )

cur = conn.cursor()

meta_tables: dict = {
    "region_sales": {
        "header": "region_id,game_platform_id, num_sales",
        "num": ""
    },
    "region": {
        "header": "region_name",
        "num": "4"
    },
    "genre": {
        "header": "genre_name",
        "num": "12"
    },
    "game": {
        "header": "genre_id, game_name",
        "num": ""
    },
    "publisher": {
        "header": "publisher_name",
        "num": "577"
    },
    "game_publisher": {
        "header": "game_id, publisher_id",
        "num": ""
    },
    "platform": {
        "header": "platform_name",
        "num": "31"
    },
    "game_platform": {
        "header": "game_publisher_id, platform_id, release_year",
        "num": ""
    }
}


def load_to_db(key: str, data):
    headers = meta_tables[key]["header"]
    vals = ','.join(['%s' for _ in range(headers.count(',') + 1)])

    SQL_query = f"""
    INSERT INTO {SCHEMA_NAME}.{key} ({headers})
    VALUES ({vals});
    """

    cur.executemany(SQL_query, data)
    conn.commit()


def get_max_id(table_name):
    SQL_query = f"""
        SELECT MAX(id) FROM {SCHEMA_NAME}.{table_name};
        """
    cur.execute(SQL_query)

    max_id = cur.fetchone()[0]

    return max_id


def create_regions():
    return [tuple(x) for x in [
        'North America', 'Europe',
        'Japan', 'Other'
    ]]


def create_genres():
    return [tuple(x) for x in [
        'Action', 'Adventure',
        'Fighting', 'Misc', 'Platform',
        'Puzzle', 'Racing', 'Role-Playing',
        'Shooter', 'Simulation', 'Sports',
        'Strategy'
    ]]


def create_publisher():
    num = meta_tables["publisher"]["num"] - 1
    # нужно, чтобы быть устойчивыми на случай перегенерации синтетики
    data = [tuple(['3DO'])]
    data.extend([tuple([fake.company()]) for _ in range(num)])
    return data


def create_game():
    num_g = meta_tables["genre"]["num"]
    data = []
    for _ in range(random.randint(1000, 12000)):
        record = [
            random.randint(1, num_g),
            fake.company()
        ]
        data.append(tuple(record))
    return data


def create_game_publisher():
    num_p = meta_tables["publisher"]["num"]
    game_id = get_max_id("game")
    data = []
    for _ in range(random.randint(1000, 15000)):
        record = [
            random.randint(1, game_id),  # game_id
            random.randint(1, num_p)  # publisher_id
        ]
        data.append(tuple(record))
    return data


# Функция для создания записей в таблице platform
def create_platform():
    num = meta_tables["platform"]["num"] - 1
    # нужно, чтобы быть устойчивыми на случай перегенерации синтетики
    data = [tuple(['PS'])]
    data.extend([tuple([fake.company()]) for _ in range(num)])
    return data


def create_game_platform():
    num_pl = meta_tables["platform"]["num"]
    game_p = get_max_id("game_publisher")
    data = []
    for _ in range(random.randint(1000, 20000)):
        record = [
            random.randint(1, game_p),  # game_publisher_id
            random.randint(1, num_pl),  # platform_id
            random.randint(1980, 2025)  # release_year
        ]
        data.append(tuple(record))
    return data


def create_region_sales(num_records):
    game_pl = get_max_id("game_platform")
    num_reg = meta_tables["region"]["num"]

    data = []
    for _ in range(num_records):
        record = [
            random.randint(1, num_reg),  # region_id
            random.randint(1, game_pl),  # game_platform_id (1-10)
            random.randint(1, 4000)  # num_sales
        ]
        data.append(tuple(record))
    return data


load_to_db("region", create_regions())
load_to_db("genre", create_genres())
load_to_db("publisher", create_publisher())
load_to_db("game", create_game())
load_to_db("game_publisher", create_game_publisher())
load_to_db("platform", create_platform())
load_to_db("game_platform", create_game_platform())
load_to_db("region_sales", create_region_sales())
