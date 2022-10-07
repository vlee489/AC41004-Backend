from pydantic import BaseModel, Field


class AddExceptionResponse(BaseModel):
    inserted_id: str = Field(description="status of exception addition attempt")


class EditExceptionResponse(BaseModel):
    status: bool
