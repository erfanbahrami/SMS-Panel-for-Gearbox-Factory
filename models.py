from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, SmallInteger, BigInteger
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP, DateTime
from sqlalchemy import Text
from sqlalchemy.sql import func

from database import Base
# Base = declarative_base()
metadata = Base.metadata


# ============================================================
# 0) EMPLOYEE / USER TABLE (FOR LOGIN & TRACKING)
# ============================================================
class Employees(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)



# ============================================================
# 1) GEARBOX INFORMATION  (MAIN PRODUCT TABLE)
# ============================================================
class GearboxInformation(Base):
    __tablename__ = "gearbox_information"
    serial = Column(BigInteger, primary_key=True, index=True)
    type = Column(String(9), nullable=False)
    size = Column(String(7), nullable=False)
    ratio = Column(SmallInteger, nullable=False)
    productionDate = Column(TIMESTAMP(timezone=True),nullable=False,server_default=func.now())
    province = Column(String(30), nullable=False)
    customer = Column(String(30), nullable=False)
    comments = Column(String(200))
    # One-to-One relationship with GuaranteeInformation
    guarantee = relationship("GuaranteeInformation", back_populates="gearbox",uselist=False)



# ============================================================
# 2) GUARANTEE INFORMATION  (ONE GUARANTEE PER GEARBOX)
# ============================================================
class GuaranteeInformation(Base):
    __tablename__ = "guarantee_information"

    id = Column(BigInteger, primary_key=True, index=True)
    serial = Column(BigInteger, ForeignKey("gearbox_information.serial"), unique=True, nullable=False)
    activeDateTime = Column(TIMESTAMP(timezone=True), nullable=False)
    expireDateTime = Column(TIMESTAMP(timezone=True), nullable=False)
    # Relationship back to gearbox
    gearbox = relationship("GearboxInformation", back_populates="guarantee")


# ============================================================
# 3) SMS INBOX (RECEIVED SMS)
# ============================================================
class SMSInbox(Base):
    __tablename__ = "sms_inbox"
    id = Column(BigInteger, primary_key=True, index=True)
    flag = Column(String(12), nullable=False)        # "true", "false", "duplicate"
    message_body = Column(String(1000), nullable=False)
    sender_mobile_number = Column(String(11), nullable=False)
    received_date_and_time = Column(TIMESTAMP(timezone=True), nullable=False)


# ============================================================
# 4) SMS OUTBOX (SENT SMS)
#    flag = sent / failed / duplicate
# ============================================================
class SMSOutbox(Base):
    __tablename__ = "sms_outbox"
    id = Column(BigInteger, primary_key=True, index=True)
    flag = Column(String(12), nullable=False)        # "sent", "failed", "duplicate"
    message_body = Column(String(1000), nullable=False)
    receiptor_mobile_number = Column(String(11), nullable=False)
    sent_date_and_time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())




