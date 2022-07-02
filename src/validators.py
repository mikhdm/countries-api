from pydantic import BaseModel


class _CountriesResponseSchema(BaseModel):
    country: str


class CountriesResponseSchema(BaseModel):
    data: _CountriesResponseSchema


class _ErrorSchema(BaseModel):
    message: str
    code: int
    
    
class ErrorSchema(BaseModel):
    error: _ErrorSchema
