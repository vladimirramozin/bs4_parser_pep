from pathlib import Path

LOG_FORMAT = '"%(asctime)s - [%(levelname)s] - %(message)s"'
DT_FORMAT = '%d.%m.%Y %H:%M:%S'
MAIN_DOC_URL = 'https://docs.python.org/3/'
BASE_DIR = Path(__file__).parent
DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'
PEP_DOC_URL = 'https://peps.python.org/'
STATUS = (
    'Active', 'Accepted', 'Deferred', 'Final',
    'Provisional', 'Rejected', 'Superseded',
    'Withdrawn', 'Draft'
)
EXPECTED_STATUS = {
    'A': ('Active', 'Accepted'),
    'D': ('Deferred'),
    'F': ('Final'),
    'P': ('Provisional'),
    'R': ('Rejected'),
    'S': ('Superseded'),
    'W': ('Withdrawn'),
    '': ('Draft', 'Active'),
}

