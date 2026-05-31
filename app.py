import time
import threading
import requests
import urllib3
import Beta_pb2 as _7P
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from flask import Flask, request, jsonify

urllib3.disable_warnings()

_1U = "4205159811"
_2P = "31895616B873AD9846006BF07EE903271FB52D8948AA1A9A56C381C13CB4D267"
_3K = b'Yg&tc%DEuh6%Zc^8'
_4V = b'6oyZDr22E3ychjM%'
_5B = "https://clientbp.ggpolarbear.com"
_6T = 15
_7H = {"Content-Type": "application/x-www-form-urlencoded"}
_8A = "Dalvik/2.1.0 (Linux; U; Android 11)"
_9R = "v1 1"
_10L = "OB53"

# ---------- Exact original functions ----------
def YoUr_MoM(d):
    return AES.new(_3K, AES.MODE_CBC, _4V).encrypt(pad(d, 16))

def UNknown(d):
    try:
        return unpad(AES.new(_3K, AES.MODE_CBC, _4V).decrypt(d), 16)
    except:
        return d

def ReSPeCt_GiRLs(n):
    res = bytearray()
    while n >= 0x80:
        res.append((n & 0x7f) | 0x80)
        n >>= 7
    res.append(n)
    return bytes(res)

def YOuR_FaThER(uid):
    return YoUr_MoM(b"\x08" + ReSPeCt_GiRLs(int(uid)))

def LOvE_HaTe():
    url = f"https://ff-jwt-gen-api.lovable.app/api/public/token?uid={_1U}&password={_2P}"
    try:
        r = requests.get(url, timeout=_6T)
        if r.status_code == 200:
            return r.json().get("token")
    except:
        return None
    return None

def TiMe_TRaVeL(ts):
    try:
        return time.strftime('%B %d, %Y at %I:%M %p', time.localtime(ts))
    except:
        return "Invalid Timestamp"

def No_NAMe(d):
    try:
        resp = _7P.SpecialFriendResponse()
        resp.ParseFromString(d)
        if not resp.HasField("duo_info"):
            return None, "No Dynamic Duo info found"
        duo = resp.duo_info
        score = duo.score
        if score < 101: lvl = 1
        elif score < 301: lvl = 2
        elif score < 501: lvl = 3
        elif score < 801: lvl = 4
        elif score < 1201: lvl = 5
        else: lvl = 6
        status = "Active" if duo.status == 2 else "Inactive"
        return {
            "Dost/Beta": str(duo.partner_uid),
            "DuoLevel": lvl,
            "DuoScore": score,
            "Active_form_days": duo.days_active,
            "Creation_Timr": TiMe_TRaVeL(duo.creation_timestamp),
            "creation_timestamp": duo.creation_timestamp,
            "status": status
        }, "Success"
    except Exception as e:
        return None, str(e)

def SiLeNt_KiLL(uid):
    res = {"jwt": None, "resp": None, "err": None}
    def InSiDe():
        try:
            jwt = LOvE_HaTe()
            res["jwt"] = jwt
            if jwt:
                headers = {
                    "Authorization": f"Bearer {jwt}",
                    "Content-Type": _7H["Content-Type"],
                    "User-Agent": _8A,
                    "X-GA": _9R,
                    "ReleaseVersion": _10L,
                    "Connection": "Keep-Alive"
                }
                payload = YOuR_FaThER(uid)
                res["resp"] = requests.post(f"{_5B}/GetSpecialFriendList", headers=headers, data=payload, timeout=_6T, verify=False)
        except Exception as e:
            res["err"] = e
    t = threading.Thread(target=InSiDe)
    t.start()
    t.join()
    return res

# ---------- Flask API ----------
app = Flask(__name__)

@app.route('/duo', methods=['GET'])
def get_duo():
    uid = request.args.get('uid')
    if not uid or not uid.isdigit():
        return jsonify({"success": False, "error": "Invalid UID"}), 400

    data = SiLeNt_KiLL(uid)
    if data["err"] or not data["jwt"]:
        return jsonify({"success": False, "error": "Token/Network Error"}), 500

    if data["resp"] and data["resp"].status_code == 200:
        dec_data = UNknown(data["resp"].content)
        parsed, msg = No_NAMe(dec_data)
        if parsed:
            return jsonify({
                "success": True,
                "data": {
                    "uid": uid,
                    "partner_uid": parsed['Dost/Beta'],
                    "duo_score": parsed['DuoScore'],
                    "duo_level": parsed['DuoLevel'],
                    "active_days": parsed['Active_form_days'],
                    "created_at": parsed['Creation_Timr'],
                    "status": parsed['status']
                }
            })
        else:
            return jsonify({
                "success": False,
                "error": "No duo found",
                "message": "This user has no partner"
            }), 200
    elif data["resp"] and data["resp"].status_code == 500:
        return jsonify({"success": False, "error": "Server Error - Invalid UID or Private Profile"}), 404
    else:
        code = data["resp"].status_code if data["resp"] else "Unknown"
        return jsonify({"success": False, "error": f"HTTP {code}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)