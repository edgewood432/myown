from sqlalchemy import Column, Integer, Boolean, String
from database import Base


class Scripts(Base):
    __tablename__ = "scripts"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    script_name = Column(String)
    is_active = Column(Boolean, default=True)
