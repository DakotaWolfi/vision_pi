from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Optional


@dataclass
class CollarStatus:
    connected: bool
    state: str
    battery_percent: Optional[int]
    detail: str = ""


class CollarClient:
    """Interface/client boundary to the external CollarPet application.

    This class intentionally avoids embedding CollarPet runtime behavior.
    When no protocol endpoint is configured, all methods remain safe no-ops.
    """

    def __init__(self, endpoint: str = "") -> None:
        self.endpoint = endpoint.strip()
        self._last_poll_s = 0.0
        self._cached = CollarStatus(connected=False, state="disconnected", battery_percent=None)

    def _refresh(self) -> None:
        now = time.time()
        if now - self._last_poll_s < 1.0:
            return
        self._last_poll_s = now

        if not self.endpoint:
            self._cached = CollarStatus(
                connected=False,
                state="disconnected",
                battery_percent=None,
                detail="endpoint not configured",
            )
            return

        # Protocol intentionally not invented here. Endpoint presence only marks
        # integration intent until CollarPet protocol is finalized.
        self._cached = CollarStatus(
            connected=False,
            state="unimplemented",
            battery_percent=None,
            detail="protocol pending",
        )

    def get_status(self) -> CollarStatus:
        self._refresh()
        return self._cached

    def set_led_mode(self, mode: str) -> str:
        _ = mode
        status = self.get_status()
        if not status.connected:
            return "offline"
        return "unsupported"

    def set_expression(self, expression: str) -> str:
        _ = expression
        status = self.get_status()
        if not status.connected:
            return "offline"
        return "unsupported"

    def vibrate(self, pattern: str = "default") -> str:
        _ = pattern
        status = self.get_status()
        if not status.connected:
            return "offline"
        return "unsupported"

    def trigger_nfc(self) -> str:
        status = self.get_status()
        if not status.connected:
            return "offline"
        return "unsupported"

    def music_recognition(self) -> str:
        status = self.get_status()
        if not status.connected:
            return "offline"
        return "unsupported"

    def petmind(self) -> str:
        status = self.get_status()
        if not status.connected:
            return "offline"
        return "unsupported"
