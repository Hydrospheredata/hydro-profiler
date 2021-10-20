from pydantic import BaseModel


class Overall(BaseModel):
    failed: int = 0
    suspicious: int = 0
    succeed: int = 0
    count: int = 0

    def add_fail(self):
        self.failed = self.failed + 1
        self.count = self.count + 1

    def add_succeed(self):
        self.succeed = self.succeed + 1
        self.count = self.count + 1

    def add_suspicious(self):
        self.suspicious = self.suspicious + 1
        self.count = self.count + 1


def merge_overall(o1: Overall, o2: Overall) -> Overall:
    return Overall(
        failed=o1.failed + o2.failed,
        suspicious=o1.suspicious + o2.suspicious,
        succeed=o1.succeed + o2.succeed,
        count=o1.count + o2.count,
    )
