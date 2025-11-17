import ghasedak_sms
from datetime import datetime

sms_api = ghasedak_sms.Ghasedak(api_key="2ac92e310b07b033a2f49a15037420332367ecfb8463c88644726d03b6955f5buoNsGTcfHK9a4RNJ")

############################################# 1 #############################################
def send_sms_guarantee_activated(type_value, size_value, ratio_value, activeDateTime_value, expireDateTime_value, mobileNumber_value):
    guarantee_Success_Activated_Command = ghasedak_sms.SendOtpInput(
        send_date=None,
        receptors=[
            ghasedak_sms.SendOtpReceptorDto(
                mobile=mobileNumber_value,
                # client_reference_id='client_ref_id'
            )
        ],
        template_name='guaranteeSuccessActivated',
        inputs=[
            ghasedak_sms.SendOtpInput.OtpInput(param='param1', value=type_value),
            ghasedak_sms.SendOtpInput.OtpInput(param='param2', value=size_value),
            ghasedak_sms.SendOtpInput.OtpInput(param='param3', value=ratio_value),
            ghasedak_sms.SendOtpInput.OtpInput(param='param4', value=activeDateTime_value),
            ghasedak_sms.SendOtpInput.OtpInput(param='param5', value=expireDateTime_value)
        ],
        udh=False
    )

    response = sms_api.send_otp_sms(guarantee_Success_Activated_Command)

# ############################################# 2 #############################################
def send_sms_invalid_serial(receivedNumber_value, mobileNumber_value):
    invalid_Serial_Command = ghasedak_sms.SendOtpInput(
        send_date=None,
        receptors=[
            ghasedak_sms.SendOtpReceptorDto(
                mobile=mobileNumber_value,
                # client_reference_id='client_ref_id'
            )
        ],
        template_name='invalidSerial',
        inputs=[
            ghasedak_sms.SendOtpInput.OtpInput(param='param1', value=receivedNumber_value)
        ],
        udh=False
    )

    response = sms_api.send_otp_sms(invalid_Serial_Command)

# ############################################# 3 #############################################
def send_sms_duplicate_serial(serial_value, activeDateTime_value, expireDateTime_value, mobileNumber_value):
    duplicate_Serial_Command = ghasedak_sms.SendOtpInput(
        send_date=None,
        receptors=[
            ghasedak_sms.SendOtpReceptorDto(
                mobile=mobileNumber_value,
                # client_reference_id='client_ref_id'
            )
        ],
        template_name='duplicateSerial',
        inputs=[
            ghasedak_sms.SendOtpInput.OtpInput(param='param1', value=serial_value),
            ghasedak_sms.SendOtpInput.OtpInput(param='param2', value=activeDateTime_value),
            ghasedak_sms.SendOtpInput.OtpInput(param='param3', value=expireDateTime_value)
        ],
        udh=False
    )

    response = sms_api.send_otp_sms(duplicate_Serial_Command)

    print(response)