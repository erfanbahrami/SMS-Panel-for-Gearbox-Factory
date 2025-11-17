from fastapi import FastAPI, BackgroundTasks
from sqlalchemy.orm import Session
from database import get_db, SessionLocal, engine
import models
import ghasedak_sms
from datetime import datetime
from dateutil.relativedelta import relativedelta
import ghasedak_sms
import threading
import time
import re
import mehrdad

models.Base.metadata.create_all(bind=engine)

sms_api = ghasedak_sms.Ghasedak(api_key="2ac92e310b07b033a2f49a15037420332367ecfb8463c88644726d03b6955f5buoNsGTcfHK9a4RNJ")

app = FastAPI()

BackgroundTasks.add_task()


def extract_received_number_from_customer(message: str):
    pattern = r"^\d{15}$"
    match = re.match(pattern, message.strip())
    return match.group(0) if match else None


# ---------------------------
#  MAIN SMS PROCESSOR
# ---------------------------
def check_sms_inbox() -> None:
    db_gen = get_db()
    db = next(iter(db_gen))
    try:
        responses = sms_api.get_received_smses(ghasedak_sms.GetReceivedSmsInput(line_number='????????', is_read=False))

        for response in responses.items:
            received_number_from_customer = extract_received_number_from_customer(response.message)
            if received_number_from_customer:
                gearbox_check = db.query(models.GearboxInformation).filter(models.GearboxInformation.serial==received_number_from_customer).first()
                if gearbox_check:
                    if gearbox_check.guarantee is None:
                        db.add(models.GuaranteeInformation(serial=gearbox_check.serial, activeDateTime=response.receiveDate, expireDateTime=response.receiveDate + relativedelta(months=12)))
                        db.commit()
                        db.refresh(gearbox_check)
                        
                        db.add(models.SMSInbox(flag='true', message_body=response.message, sender_mobile_number=response.sender, received_time_and_date=response.receiveDate))
                        
                        type_value=gearbox_check.type
                        size_value=gearbox_check.size
                        ratio_value=gearbox_check.ratio
                        activeDateTime_value=gearbox_check.guarantee.activeDateTime
                        expireDateTime_value=gearbox_check.guarantee.expireDateTime
                        mobileNumber_value=response.sender
                        sent_sms = mehrdad.send_sms_guarantee_activated(type_value, size_value, ratio_value, activeDateTime_value, expireDateTime_value, mobileNumber_value)

                        db.add(models.SMSOutbox(flag='true', message_body=sent_sms.messageBody , receiptor_mobile_number=sent_sms.receptor, sent_date_and_time=sent_sms.sendDate))
                        db.commit()


                    else: #if gearbox_check.guarantee
                        db.add(models.SMSInbox(flag='duplicate', message_body=response.message, sender_mobile_number=response.sender, received_time_and_date=response.receiveDate))
                        
                        serial_value=gearbox_check.guarantee.serial
                        activeDateTime_value=gearbox_check.guarantee.activeDateTime
                        expireDateTime_value=gearbox_check.guarantee.expireDateTime
                        mobileNumber_value=response.sender
                        sent_sms = mehrdad.send_sms_duplicate_serial(serial_value, activeDateTime_value, expireDateTime_value, mobileNumber_value)

                        db.add(models.SMSOutbox(flag='duplicate', message_body=sent_sms.messageBody , receiptor_mobile_number=sent_sms.receptor, sent_date_and_time=sent_sms.sendDate))
                        db.commit()


                else:
                    db.add(models.SMSInbox(flag='false', message_body=response.message, sender_mobile_number=response.sender, received_time_and_date=response.receiveDate))
                    
                    receivedNumber_value=received_number_from_customer
                    mobileNumber_value=response.sender
                    sent_sms = mehrdad.send_sms_invalid_serial(receivedNumber_value, mobileNumber_value)

                    db.add(models.SMSOutbox(flag='false', message_body=sent_sms.messageBody , receiptor_mobile_number=sent_sms.receptor, sent_date_and_time=sent_sms.sendDate))
                    db.commit()


            else:
                db.add(models.SMSInbox(flag='wrong-format', message_body=response.message, sender_mobile_number=response.sender, received_time_and_date=response.receiveDate))
                    
                receivedNumber_value=response.message
                mobileNumber_value=response.sender
                sent_sms = mehrdad.send_sms_invalid_serial(receivedNumber_value, mobileNumber_value)

                db.add(models.SMSOutbox(flag='wrong-format', message_body=sent_sms.messageBody , receiptor_mobile_number=sent_sms.receptor, sent_date_and_time=sent_sms.sendDate))
                db.commit()
  

    except Exception as e:
        print("🔥 ERROR in check_sms_inbox:", e)

    finally:
        # close the DB session safely
        try:
            db_gen.close()
        except:
            pass



@app.get("/")
def home():
    return {"message": "SMS receiver service is running."}








