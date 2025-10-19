from sqlalchemy import Column, String, Float, Integer
from .database import Base

class District(Base):
    __tablename__ = "districts"
    id = Column(Integer, primary_key=True, index=True)
    district_name = Column(String)
    state_code = Column(String)
    class_rooms = Column(Float)
    total_teachers = Column(Float)
    class_students = Column(Float)
    student_teacher_ratio = Column(Float)
    cluster = Column(Integer, default=-1)
    anomaly = Column(Integer, default=0)
    latitude = Column(Float)
    longitude = Column(Float)
