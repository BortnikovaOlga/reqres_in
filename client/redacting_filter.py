import logging
from dataclasses import dataclass


@dataclass
class Config:
    # api_key: str
    # url: str
    password: str


config = Config(
    # api_key='super_secret_api_key',
    # url='https://swapi.dev/api/films'
    password="cityslicka"
)

for_masking = [
    # config.api_key,
    # config.url

    config.password
]


class RedactingFilter(logging.Filter):
    def __init__(self, patterns: list):
        super().__init__()
        self._patterns = patterns

    def filter(self, record):
        record.msg = self.redact(record.msg)
        # if isinstance(record.args, dict):
        #     for key in record.args.keys():
        #         record.args[key] = self.redact(record.args[key])
        # else:
        #     record.args = tuple(self.redact(arg) for arg in record.args)
        record.args = tuple(self.redact(arg) for arg in record.args)
        return True

    def redact(self, msg: str):
        msg = isinstance(msg, str) and msg or str(msg)
        for pattern in self._patterns:
            msg = msg.replace(pattern, '******')
        return msg


def produce_logger(name):
    logger = logging.getLogger(name)
    filter = RedactingFilter(for_masking)
    logger.addFilter(filter)
    return logger
