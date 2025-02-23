import sys

import anyio
import dagger
from dagger import dag
from shlex import split


async def main(args: list[str]):
    print(args)
    config = dagger.Config(log_output=sys.stderr)
    async with dagger.connection(config):
        # build container with cowsay entrypoint
        ctr = dag.container().from_("python:alpine").with_exec(split("pip install cowsay"))

        # run cowsay with requested message
        result = await ctr.with_exec(["cowsay", "-t", *args]).stdout()

    print(result)


anyio.run(main, ["test1"])
# anyio.run(main, sys.argv[1:])
