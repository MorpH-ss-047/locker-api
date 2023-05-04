from googleapiclient.discovery import build
from google.oauth2 import service_account
from urllib.parse import urlencode
import requests
import json
import pyaes
import config


credentials = service_account.Credentials.from_service_account_file(
    config.SERVICE_ACCOUNT_FILE, scopes=config.SCOPES
)

androidmanagement = build("androidmanagement", "v1", credentials=credentials)


def create_policy(pk, policy_json):
    new_policy_name = config.BASE_POLICY_NAME + pk
    policy = (
        androidmanagement.enterprises()
        .policies()
        .patch(
            name=new_policy_name,
            body=json.loads(policy_json),
        )
        .execute()
    )

    return policy, new_policy_name


def get_policy(pk):
    policy_name = config.BASE_POLICY_NAME + pk
    try:
        policy = (
            androidmanagement.enterprises()
            .policies()
            .get(
                name=policy_name,
            )
            .execute()
        )
        return policy
    except Exception as e:
        return False


def get_enrollment_token(enterprise_name, policy_name):
    enrollment_token = (
        androidmanagement.enterprises()
        .enrollmentTokens()
        .create(parent=enterprise_name, body={"policyName": policy_name})
        .execute()
    )
    return enrollment_token


def get_qr_code(enrollment_token):
    image = {"cht": "qr", "chs": "500x500", "chl": enrollment_token["qrCode"]}
    qrcode_url = "https://chart.googleapis.com/chart?" + urlencode(image)
    return qrcode_url


def get_qr_url(pk):
    try:
        _, policy_name = create_policy(pk, config.POLICY_JSON)
    except Exception as e:
        return False
        # return f"Something went wrong during policy creation {e}", 403
    try:
        enrollment_token = get_enrollment_token(config.ENTERPRISE_NAME, policy_name)
    except Exception as e:
        return False
        # return f"Something went wrong during enrollment token creation {e}", 403
    try:
        qr_code_url = get_qr_code(enrollment_token)
        return qr_code_url
    except Exception as e:
        return False
        # return f"Something went wrong during qr code creation {e}", 403


def update_policy(pk, new_policy_json):
    policy_name = config.BASE_POLICY_NAME + pk

    policy = get_policy(pk)
    new_policy = new_policy_json
    
    if("lockdownDevice" in new_policy.keys()):
      
        for i, app2 in enumerate(policy["applications"]):
            if app2["packageName"] == "com.apptimates.apptimatelocker":
                policy["applications"][i]['installType'] = 'KIOSK' if new_policy['lockdownDevice'] else 'FORCE_INSTALLED'
                updated_policy_dict = policy
                break
        updated_policy_dict['screenCaptureDisabled'] = new_policy['lockdownDevice'] 
        updated_policy_dict["usbFileTransferDisabled"] = new_policy['lockdownDevice'] 
        updated_policy_dict["bluetoothConfigDisabled"] = new_policy['lockdownDevice'] 
        updated_policy_dict["outgoingBeamDisabled"] = new_policy['lockdownDevice'] 
        updated_policy_dict["cameraDisabled"] = new_policy['lockdownDevice'] 

            
    else:

        updated_policy_dict = {**policy, **new_policy}

    updated_policy = (
        androidmanagement.enterprises()
        .policies()
        .patch(
            name=policy_name,
            body=updated_policy_dict,
        )
        .execute()
    )

    return updated_policy


def release_device(pk):
    policy_name = config.BASE_POLICY_NAME + pk

    policy = get_policy(pk)
   
    for i, app2 in enumerate(policy["applications"]):
        if app2["packageName"] == "com.apptimates.apptimatelocker":
            policy["applications"][i]['installType'] = 'BLOCKED' 
            updated_policy_dict = policy
            break
    updated_policy_dict['factoryResetDisabled'] = False
    updated_policy_dict['screenCaptureDisabled'] = False
    updated_policy_dict["usbFileTransferDisabled"] = False
    updated_policy_dict["bluetoothConfigDisabled"] = False
    updated_policy_dict["outgoingBeamDisabled"] = False
    updated_policy_dict["cameraDisabled"] = False

    updated_policy = (
        androidmanagement.enterprises()
        .policies()
        .patch(
            name=policy_name,
            body=updated_policy_dict,
        )
        .execute()
    )
    print (updated_policy)

    #check if the policy was updated successfully
    keys = updated_policy.keys()
    return (
        # (if ("factoryResetDisabled") in keys updated_policy['factoryResetDisabled'] == False else False )and
        # updated_policy['screenCaptureDisabled'] == False and
        # updated_policy["usbFileTransferDisabled"] == False and
        # updated_policy["bluetoothConfigDisabled"] == False and
        # updated_policy["outgoingBeamDisabled"] == False and
        # updated_policy["cameraDisabled"] == False 
        all([policy["applications"][i]['installType'] == 'BLOCKED' for i, app2 in enumerate(policy["applications"]) if app2["packageName"] == "com.apptimates.apptimatelocker"])
            
    )
        
    # return updated_policy

def checkAuthentication(payload,encrypted):
    if encrypted:
        aes = pyaes.AESModeOfOperationCTR(key)

    # decrypted data is always binary, need to decode to plaintext
        decrypted = aes.decrypt(encrypted).decode('utf-8')
        return payload == decrypted
    else:
        return False


if __name__ == "__main__":
    # _, policy_name = create_policy("mypolicy", config.POLICY_JSON)
    # enrollment_token = get_enrollment_token(
    #     config.ENTERPRISE_NAME, policy_name
    # )
    # qr_code_url = get_qr_code(enrollment_token)
    # r = requests.get(qr_code_url)
    # with open("qr_code.png", "wb") as f:
    #     f.write(r.content)
    print(get_policy("mypolicy"))
