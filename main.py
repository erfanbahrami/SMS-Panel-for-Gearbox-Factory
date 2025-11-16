from fastapi import FastAPI
from sqlalchemy.orm import Session
from database import get_db, SessionLocal, engine
import models

from datetime import datetime
import ghasedak_sms
import threading
import time
import re

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# ---------------------------
#  MAIN SMS PROCESSOR
# ---------------------------
@app.on_event("startup")
@repeat_every(seconds=180)        
def check_sms_inbox() -> None:
    db_gen = get_db()
    db = next(iter(db))

    try:
        # line number is wrong it is a special number that assigned for you annd can see in panel
        response = sms_api.get_received_smses(ghasedak_sms.GetReceivedSmsInput(line_number='30005088', is_read=False))

        for sms in response.items:
            receivedNumber = extract_serial(sms.message)
            if receivedNumber:
                # if below query not be null, serial is fake?
                # validity_check = db.query(models.GearboxInformation).filter(models.GearboxInformation.serial == receivedNumber).first()
                # if validity_check :
                if  ### to database check kone in to gerabox_information hast ya na:
                    if ### age to jadvale gerabox_information bood, bere tu guarantee_information check kone hast ya na ya na
                        if    ### age nabood
                                ### bechepon to database jadvale sms_inbox ba flag true
                                ### send sms kone vase karbar ke guarantee active shod
                                ### sms ersali ro ezafe kone be jadvale sms_outbox ba flag true

                        else  ### age bod (yani tekrarie)
                                ### bechepon to database jadvale sms_inbox ba flag duplicate
                                ### send sms kone be karbar bege tekrarie
                                ### sms ersali ro ezafe kone be jadvale sms_outbox ba flag duplicate

                    else ### age to jadvale gerabox_information nabood
                           ### bechepon to database jadvale sms_inbox ba flag false
                           ### send sms kone be karbar bege seriale vared shode eshtebahe
                           ### sms ro ezafe kone be jadvale sms_outbox ba flag false    
            else:
                # Invalid SMS
                # sample add to db by related objecy
                # db.add(models.SMSInbox(flag= "kososher", message_body= "", mobile_number=""))
                # below command required for commit and better to be inside a try catch
                # db.commit()
                ### bechepon to database jadvale sms_inbox ba flag kossher
                ### send sms kone be karbar bege kossher vared nakon haroooooom zade
                ### sms ro ezafe kone be jadvale sms_outbox ba flag kossher

    except Exception as e:
        print("🔥 ERROR in check_sms_inbox:", e)

    finally:
        # close the DB session safely
        try:
            db_gen.close()
        except:
            pass




def extract_serial(message: str):
    pattern = r"^\d{15}$"
    match = re.match(pattern, message.strip())
    return match.group(0) if match else None



@app.get("/")
def home():
    return {"message": "SMS receiver service is running."}








