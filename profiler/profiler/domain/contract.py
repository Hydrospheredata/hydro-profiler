from typing import List

from pydantic import BaseModel

from profiler.domain.table_requirement import TableRequirement


class Contract(BaseModel):
    __root__: List[TableRequirement]
