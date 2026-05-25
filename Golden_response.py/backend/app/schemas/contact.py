from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import EmailStr
from pydantic import Field


class ContactSchema(BaseModel):
    full_name: str = Field(min_length=2, max_length=255)
    business_email: EmailStr
    phone_number: str = Field(min_length=7, max_length=20)
    company_name: str | None = None
    service_of_interest: str | None = None
    message: str = Field(min_length=10, max_length=5000)
    honeypot: str | None = None

    model_config = ConfigDict(str_strip_whitespace=True)
