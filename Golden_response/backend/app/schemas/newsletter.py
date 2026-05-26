from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import EmailStr


class NewsletterSchema(BaseModel):
    email: EmailStr

    model_config = ConfigDict(str_strip_whitespace=True)
