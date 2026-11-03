import logging


class OishiiLogger:
    def __init__(self, name: str, level: int = logging.INFO):
        logging.basicConfig(
            level=level,
            force=True)
        self.level = level
        self.logger = logging.getLogger(name)