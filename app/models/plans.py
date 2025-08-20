from sqlalchemy import Column, Integer, String, Float
from app.database import Base
from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import relationship
import datetime

class Plan(Base):
    __tablename__ = "plans"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    duration_days = Column(Integer, nullable=True)  # Opcional, si es suscripción

class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    plan_id = Column(Integer, ForeignKey("plans.id"), nullable=False)
    start_date = Column(DateTime, default=datetime.datetime.utcnow)
    end_date = Column(DateTime, nullable=True)

    plan = relationship("Plan")