from datetime import datetime
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from app.database import Base


class Newsletter(Base):
    __tablename__ = "newsletter_subscribers"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    subscribed_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )
