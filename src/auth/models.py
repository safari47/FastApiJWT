import uuid

from sqlalchemy import Boolean, Date, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database.database import Base


class User(Base):
    id: Mapped[uuid.UUID] = mapped_column(
        String, primary_key=True, default=lambda: str(uuid.uuid4())
    )
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)

    # Связь один-к-одному с Profile
    profile: Mapped["Profile"] = relationship(
        "Profile",
        back_populates="user",
        uselist=False,  # Обеспечивает связь один-к-одному
        lazy="selectin",  # Автоматически загружает связанные данные из Profile при запросе User
        cascade="all, delete-orphan",  # Позволяет удалять связанные Profile при удалении User
    )


class Profile(Base):
    id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), primary_key=True)
    username: Mapped[str] = mapped_column(String, nullable=True, unique=True)
    bio: Mapped[str] = mapped_column(String, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    birthday: Mapped[Date] = mapped_column(Date, nullable=True)
    phone_number: Mapped[str] = mapped_column(String, nullable=True)

    # Обратная связь один-к-одному с User
    user: Mapped["User"] = relationship("User", back_populates="profile", uselist=False)
