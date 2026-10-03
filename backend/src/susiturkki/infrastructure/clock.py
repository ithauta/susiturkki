from datetime import datetime

from susiturkki.domain.time import HELSINKI


class SystemClock:
    def now(self) -> datetime:
        return datetime.now(HELSINKI)
