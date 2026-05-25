from datetime import datetime
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from app.database import Base


class Contact(Base):
    __tablename__ = "contacts"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(255))
    business_email: Mapped[str] = mapped_column(String(255))
    phone_number: Mapped[str] = mapped_column(String(100))
    company_name: Mapped[str | None] = mapped_column(String(255))
    service_of_interest: Mapped[str | None] = mapped_column(String(255))
    message: Mapped[str] = mapped_column(String(5000))
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )
