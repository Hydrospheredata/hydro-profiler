import  yoyo

backend = yoyo.get_backend('sqlite:///profiler.db')
migrations = yoyo.read_migrations('./migrations')

def create_db_file():
    database_name = 'profiler.db'
    try:
        open(database_name, 'r').close()
    except:
        open(database_name, 'w').close()


if __name__ == "__main__":
    create_db_file()

    with backend.lock():
        backend.apply_migrations(backend.to_apply(migrations))
