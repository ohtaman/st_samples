import datetime
from multiprocessing import Queue
from multiprocessing.managers import BaseManager
import pathlib
import pickle


ARTIFACT_PATH = pathlib.Path('./artifacts')
QUEUE_HOST = '' # localhost
QUEUE_PORT = 6666
AUTH_KEY = b'1234'


class QueueManager(BaseManager):
    pass

def _get_queue():
    return queue

queue = Queue()
QueueManager.register(
    'get_queue',
    callable=_get_queue
)


def get_job_id():
    return datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S')


def get_jobs():
    if not ARTIFACT_PATH.exists():
        return []

    jobs = [
        path.stem
        for path in ARTIFACT_PATH.iterdir()
        if path.is_dir()
    ]
    jobs.sort()
    jobs.reverse()
    return jobs


def put_job(*args):
    manager = QueueManager(address=(QUEUE_HOST, QUEUE_PORT), authkey=b'1234')
    manager.connect()
    queue = manager.get_queue()
    job_id = get_job_id()
    queue.put((job_id, args))
    return job_id


def get_job():
    manager = QueueManager(address=(QUEUE_HOST, QUEUE_PORT), authkey=b'1234')
    manager.connect()
    queue = manager.get_queue()
    return queue.get()


def save_artifact(name, data, job_id):
    artifact_dir = ARTIFACT_PATH.joinpath(job_id)
    if not artifact_dir.exists():
        artifact_dir.mkdir(parents=True)
    filepath = artifact_dir.joinpath(f'{name}.pkl')
    with open(filepath, 'wb') as o_:
        pickle.dump(data, o_)


def load_artifact(name, job_id):
    artifact_dir = ARTIFACT_PATH.joinpath(job_id)
    if not artifact_dir.exists():
        raise ValueError(f'Artifact directory {artifact_dir} does not exist')

    filepath = artifact_dir.joinpath(f'{name}.pkl')
    with open(filepath,'rb') as i_:
        return pickle.load(i_)


def serve():
    manager = QueueManager(address=(QUEUE_HOST, QUEUE_PORT), authkey=AUTH_KEY)
    server = manager.get_server()
    server.serve_forever()


if __name__ == '__main__':
    serve()