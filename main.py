from __future__ import annotations

import asyncio

from sources.phaohoa import main as scan_phaohoa


if __name__ == "__main__":
    asyncio.run(scan_phaohoa())
