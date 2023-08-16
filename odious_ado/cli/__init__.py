# # -*- coding: utf-8 -*-
# """
# Command Line Interface
# """
import asyncio
from multiprocessing import freeze_support
import platform
import sys

from odious_ado.cli.commands import main


operating_system = platform.system()
if operating_system.lower() == "linux":
    import uvloop

    if __name__ == "__main__":
        freeze_support()
        if sys.version_info >= (3, 11):
            with asyncio.Runner(loop_factory=uvloop.new_event_loop) as runner:
                runner.run(main())
        else:
            uvloop.install()
            asyncio.run(main())
else:
    main()
