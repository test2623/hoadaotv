from __future__ import annotations

import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from unittest.mock import patch
from zoneinfo import ZoneInfo

from sources import phaohoa

TZ = ZoneInfo("Asia/Ho_Chi_Minh")
MATCH_URL = "https://phaohoa1.live/truc-tiep/malisheva-vs-hibernian-23-07-2026-776573"
SIMPLE_URL = "https://phaohoa1.live/truc-tiep/tho-nhi-ki-w-vs-canada-w"


class StandaloneTests(unittest.TestCase):
    def test_home_domain(self) -> None:
        self.assertEqual(phaohoa.HOME_URLS[0], "https://phaohoa1.live/")

    def test_dated_url(self) -> None:
        name, time_value, _ = phaohoa.derive_match_info(MATCH_URL)
        self.assertEqual(name, "Malisheva vs Hibernian")
        self.assertEqual(time_value, "")
        self.assertEqual(phaohoa.extract_date(MATCH_URL), "23/07")

    def test_card_schedule(self) -> None:
        rows = [{
            "url": SIMPLE_URL,
            "raw_title": "Thổ Nhĩ Kì (W) VS Canada (W)",
            "raw_time": "15:00 - 23-07",
            "card_text": "15:00 - 23-07 Bóng chuyền Nations League Thổ Nhĩ Kì (W) VS Sắp diễn ra Canada (W) KaKa",
        }]
        kept, _ = phaohoa.filter_links_by_scan_window(rows, now=datetime(2026, 7, 23, 14, 0, tzinfo=TZ))
        self.assertEqual(len(kept), 1)
        self.assertEqual(kept[0]["time"], "15:00")
        self.assertEqual(kept[0]["date"], "23/07")

    def test_output_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with patch.object(phaohoa, "OUTPUT_M3U", root / "phaohoa_live.m3u"), \
                 patch.object(phaohoa, "OUTPUT_PIPE_M3U", root / "phaohoa_live_pipe.m3u"), \
                 patch.object(phaohoa, "OUTPUT_VLC_M3U", root / "phaohoa_live_vlc.m3u"), \
                 patch.object(phaohoa, "OUTPUT_DEBUG", root / "phaohoa_debug.json"):
                phaohoa.write_outputs([])
            for name in ("phaohoa_live.m3u", "phaohoa_live_pipe.m3u", "phaohoa_live_vlc.m3u"):
                self.assertEqual((root / name).read_text(encoding="utf-8"), "#EXTM3U\n")


if __name__ == "__main__":
    unittest.main()
