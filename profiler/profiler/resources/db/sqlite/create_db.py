import yoyo
import os


if __name__ == "__main__":
    path = os.path.dirname(os.path.realpath(__file__)) + '/profiler.db'

    open(path, 'w').close()
    backend = yoyo.get_backend('sqlite:///' + path)

    migrations = yoyo.read_migrations('./migrations')

    with backend.lock():
        backend.apply_migrations(backend.to_apply(migrations))
