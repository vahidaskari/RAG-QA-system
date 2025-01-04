from typing import Annotated

from pydantic import BaseModel
from pydantic.functional_validators import BeforeValidator

PyObjectId = Annotated[str, BeforeValidator(str)]


class RequestDataModel(BaseModel):
    """defines schema model of document to insert into database"""

    query: str
    context: list
    response: str
    document_id: str
    request_time: str
    response_time: str
    duration: float
