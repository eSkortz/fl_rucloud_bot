from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func, Sequence, UniqueConstraint, ForeignKeyConstraint

from database.orm._base_class import Base
from database.orm._annotations import (
    IntegerPrimaryKey,
    IntegerColumn,
    BoolColumn,
    TimestampWTColumn,
)


class M2M_UsersFolders(Base):
    __tablename__ = "m2m_users_folders"
    __table_args__ = (
        UniqueConstraint("user_id", "folder_id", "is_active"),
        ForeignKeyConstraint(["user_id"], ["users.id"]),
        ForeignKeyConstraint(["folder_id"], ["folders.id"]),
    )
    id: Mapped[IntegerPrimaryKey] = mapped_column(Sequence("m2m_users_folders_id_seq"))
    user_id: Mapped[IntegerColumn] = mapped_column(index=True, nullable=False)
    folder_id: Mapped[IntegerColumn] = mapped_column(index=True, nullable=False)
    is_active: Mapped[BoolColumn] = mapped_column(
        index=True, nullable=False, default=True
    )
    expired_at: Mapped[TimestampWTColumn] = mapped_column(index=True, nullable=False)
    created_at: Mapped[TimestampWTColumn] = mapped_column(
        nullable=False, default=func.now()
    )
    updated_at: Mapped[TimestampWTColumn] = mapped_column(
        nullable=False, default=func.now(), onupdate=func.now()
    )
