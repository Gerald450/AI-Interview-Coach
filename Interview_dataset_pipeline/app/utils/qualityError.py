class QualityError(Exception):
    def __init__(self, reason: str, score: int) -> None:
        self.reason = reason
        self.score = score
        super().__init__(reason)