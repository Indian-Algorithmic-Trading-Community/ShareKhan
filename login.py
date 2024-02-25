import pyotp, requests
from urllib.parse import urlparse, parse_qs

AUTH_URL = "https://api.sharekhan.com/skapi/auth/login"
TWOFA_URL = "https://api.sharekhan.com/skapi/auth/verifyOTP"
USERID = "YOUR_USERID"
PASSWORD = "YOUR_PASSWORD"
TWOFA_SECRET = "YOUR_TOTP_SECRET_KEY"
API_KEY = "YOUR_API_KEY"
STATE = "YOUR_STATE"


def totp(qrcode: str) -> str:
    return pyotp.TOTP(qrcode).now().zfill(6)


session = requests.session()
auth_data = {
    "loginId": USERID,
    "membershipPwd": PASSWORD,
    "apiKey": API_KEY,
    "vendorKey": "",
    "userId": "",
    "versionId": "",
    "state": STATE,
    "isLoginAfterActivation": "0",
}
response = session.post(AUTH_URL, json=auth_data)
print(response.status_code)
if response.status_code == 200:
    data = response.json()
    print(data)
    if data["statusCode"] == 100:
        requestSessionId = data["requestSessionId"]

        twofa_data = {
            "loginId": USERID,
            "apiKey": API_KEY,
            "vendorKey": "",
            "userId": "",
            "versionId": "",
            "state": STATE,
            "otp": "",
            "totp": totp(TWOFA_SECRET),
            "validateBy": "TOTP",
            "requestSessionId": requestSessionId,
        }

        response = session.post(TWOFA_URL, json=twofa_data)
        print(response.status_code)
        if response.status_code == 200:
            data = response.json()
            print(data)
            if (
                data["statusCode"] == 200
                and data["msg"] == "TOTP validated Successfully"
            ):
                responseUrl = data["responseUrl"]
                print(f"\nResponseUrl:  {responseUrl}\n")
                response_url_schema = urlparse(responseUrl)
                response_url_dict = parse_qs(response_url_schema.query)
                request_token = response_url_dict["request_token"][0]
                print(f"RequestToken:  {request_token}\n")
        else:
            print(response.text)
else:
    print(response.text)
