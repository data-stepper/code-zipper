# Invoke
from invoke import task


@task(default=True)
def pre_commit(ctx):
    ctx.run("isort .")
    ctx.run("ruff format")
    ctx.run("ruff check --fix")


@task
def clean(ctx):
    ctx.run("rm -rf build dist src.egg-info code_zipper-*")
    ctx.run("find . -name '*.pyc' -delete")
    ctx.run("find . -name '__pycache__' -delete")
