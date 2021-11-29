import pathlib
import subprocess
from typing import Optional

import fastapi
import uvicorn
import pydantic


app = fastapi.FastAPI()
apps_dir = pathlib.Path(__file__).parent.parent.joinpath('apps')


class App(pydantic.BaseModel):
    name: str
    repo: str
    description: Optional[str] = None


def clone_repo(repo: str, dest: str=''):
    cmd = f'git clone {repo} {dest}'
    result = subprocess.run(cmd, shell=True, check=True)
    return result.check_returncode() == 0

def new_func():
    return """ Call git and clone repository """


@app.post('/apps')
def register(app: App):
    app_dir = apps_dir.joinpath(app.name)
    if app_dir.exists:
        raise fastapi.HTTPException(
            status_code=409,
            detail='App already exists.'
        )
    app_dir.mkdir(parents=True)
    if not clone_repo(app.repo, app_dir.joinpath('repo').as_posix()):
        raise fastapi.HTTPException(
            status_code=409,
            detail='Failed to clone repository.'
        )        


if __name__ == '__main__':
    uvicorn.run(app)