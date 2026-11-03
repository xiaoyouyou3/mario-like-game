# /// script
# dependencies = [
#     "pygame-ce",
# ]
# ///
"""pygbag（Web 版）用の入り口。開発機では `python -m src.main` で起動する。"""

import asyncio

from src.main import main

asyncio.run(main())
