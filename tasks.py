# Invoke
from invoke import task


@task(default=True)
def pre_commit(ctx):
    ctx.run("isort .")
    ctx.run("ruff format")
    ctx.run("ruff check --fix")
