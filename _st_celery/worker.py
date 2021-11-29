import os
import pathlib
import pickle
import time
import datetime

import celery


ARTIFACT_PATH = pathlib.Path('data/artifacts')
if not ARTIFACT_PATH.exists():
    ARTIFACT_PATH.mkdir(parents=True)


app = celery.Celery('celery')
if 'REDIS_URL' in os.environ:
    app.conf.update(
        BROKER_URL=os.environ['REDIS_URL'],
        CELERY_RESULT_BACKEND=os.environ['REDIS_URL']
    )

@app.task(name='add', bind=True)
def add(self: celery.Task, x, y):
    start = datetime.datetime.now()
    result = x + y
    time.sleep(20)
    end = datetime.datetime.now()
    if self.request.id is not None:
        filepath = ARTIFACT_PATH.joinpath(f'{self.request.id}.pkl')
        with open(filepath, 'wb') as o_:
            pickle.dump({
                    'id': self.request.id,
                    'task': self.name,
                    'start': start,
                    'end': end,
                    'result': result
                },
                o_
            )
    return result