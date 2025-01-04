import logging
from typing import Union
from datetime import datetime

from bson import ObjectId
from bson.errors import InvalidId

from fastapi import APIRouter, UploadFile, status
from fastapi.responses import JSONResponse

from app.utils import mock_data, utils
from app.config import schemas
from app.exceptions import NoContextError, InternalServerError, InvalidDocumentId
from app.db import crud, models

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/file")
async def files(
    documents: list[UploadFile],
):
    logger.debug("new request recived for file upload. file counts: %i", len(documents))
    file_paths = await utils.save_files(documents=list(documents))
    try:
        texts = await utils.extract_text(file_paths=file_paths)
        document_id = await utils.save_in_chroma(texts)
    except Exception as e:
        logger.error("Error in rag_endpoints.file route: %s", e)
        raise InternalServerError() from e
    logger.info("documents saved to chroma. document_id: %s", document_id)
    return {"document_id": document_id}


@router.post("/chat", response_model=schemas.ChatResponse)
async def chat(body: schemas.ChatRequest):
    # TODO validate query and document_id
    # TODO each user should only has access to his own documents

    request_time = datetime.now()
    logger.debug("new request recived for chat. data: %s", body)

    context = await utils.query_chroma(query=body.query, document_id=body.document_id)
    if not context:
        raise NoContextError()
    try:
        response = await utils.request_llm(context=context, question=body.query)

        response_time = datetime.now()

        request_data = models.RequestDataModel(
            query=body.query,
            context=(doc.page_content for doc, _score in context),
            response=response,
            document_id=body.document_id,
            request_time=str(request_time),
            response_time=str(response_time),
            duration=(response_time - request_time).total_seconds(),
        )
        crud.insert_document(request_data.model_dump())
    except Exception as e:
        logger.error("Error in rag_endpoints.chat route: %s", e)
        raise IndentationError() from e

    logger.info("request completed. request data: %s", request_data.model_dump())
    return JSONResponse(status_code=status.HTTP_200_OK, content={"response": response})


@router.post(
    "/logs", response_model=Union[schemas.LogResponse, list[schemas.LogResponse]]
)
async def get_logs(body: schemas.LogsRequest):
    try:
        # validate id (raise InvalidId exception if not valid)
        ObjectId(body.document_id)

        if body.document_id:
            data = crud.get_document(id=body.document_id)
        else:
            data = list(crud.get_all_documents())

        if not data:
            # no result
            data = {}
        return JSONResponse(status_code=status.HTTP_200_OK, content=data)

    except InvalidId as ii:
        logger.info("provided document id is not valid!")
        raise InvalidDocumentId() from ii
    except Exception as e:
        logger.error("Error in rag_endpoints.logs: %s", e)
        raise InternalServerError() from e
