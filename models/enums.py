import enum

class JobType(str, enum.Enum):
    WORD_STATS = "WORD_STATS"
    WORD_STATS_COMPARE = "WORD_STATS_COMPARE"

class JobStatus(str, enum.Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"
    FAILED = "FAILED"
