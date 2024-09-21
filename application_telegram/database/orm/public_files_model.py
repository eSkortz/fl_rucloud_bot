from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func, Sequence

from database.orm._base_class import Base
from database.orm._annotations import (
    IntegerPrimaryKey,
    TextColumn,
    TimestampWTColumn,
)


class Files(Base):
    __tablename__ = "files"
    id: Mapped[IntegerPrimaryKey] = mapped_column(Sequence("files_id_seq"))
    name: Mapped[TextColumn] = mapped_column(nullable=False)
    file_link: Mapped[TextColumn] = mapped_column(nullable=False)
    created_at: Mapped[TimestampWTColumn] = mapped_column(
        nullable=True, default=func.now()
    )
    updated_at: Mapped[TimestampWTColumn] = mapped_column(
        nullable=True, default=func.now(), onupdate=func.now()
    )
