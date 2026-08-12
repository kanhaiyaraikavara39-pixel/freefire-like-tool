import os
import json
import asyncio
import aiohttp
import requests
import binascii
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from google.protobuf.message import DecodeError

# तुम्हारे Protobuf इम्पोर्ट्स
from . import like_pb2
from . import uid_generator_pb2
from . import visit_count_pb2

# --- USER के फोल्डर से टोकन लोड करने का फंक्शन ---
def load_user_tokens(region):
    cwd = os.getcwd()  # यह यूजर का करेंट फोल्डर निकालेगा
    try:
        if region == "IND":
            file_path = os.path.join(cwd, "token_ind.json")
        elif region in {"BR", "US", "SAC", "NA"}:
            file_path = os.path.join(cwd, "token_br.json")
        else:
            file_path = os.path.join(cwd, "token_bd.json")
            
        with open(file_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        raise Exception(f"Token file '{os.path.basename(file_path)}' not found in your folder. Please provide it.")
    except Exception as e:
        raise Exception(f"Error loading tokens: {e}")

# --- एन्क्रिप्शन लॉजिक ---
def encrypt_message(plaintext):
    try:
        key = b'Yg&tc%DEuh6%Zc^8'
        iv = b'6oyZDr22E3ychjM%'
        cipher = AES.new(key, AES.MODE_CBC, iv)
        padded_message = pad(plaintext, AES.block_size)
        encrypted_message = cipher.encrypt(padded_message)
        return binascii.hexlify(encrypted_message).decode('utf-8')
    except Exception as e:
        return None

def create_protobuf_message(user_id, region):
    message = like_pb2.like()
    message.uid = int(user_id)
    message.region = region
    return message.SerializeToString()

def create_protobuf(uid):
    message = uid_generator_pb2.uid_generator()
    message.saturn_ = int(uid)
    message.garena = 1
    return message.SerializeToString()

def enc(uid):
    protobuf_data = create_protobuf(uid)
    if protobuf_data is None: return None
    return encrypt_message(protobuf_data)

# --- रिक्वेस्ट लॉजिक ---
async def send_request(encrypted_uid, token, url):
    try:
        edata = bytes.fromhex(encrypted_uid)
        headers = {
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; ASUS_Z01QD Build/PI)",
            "Connection": "Keep-Alive",
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/x-www-form-urlencoded",
            "X-Unity-Version": "2018.4.11f1",
            "X-GA": "v1 1",
            "ReleaseVersion": "OB54"
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=edata, headers=headers) as response:
                return await response.text()
    except Exception:
        return None

async def send_multiple_requests(uid, region, url):
    protobuf_message = create_protobuf_message(uid, region)
    encrypted_uid = encrypt_message(protobuf_message)
    tokens = load_user_tokens(region)  # यूजर के टोकन इस्तेमाल होंगे
    
    tasks = []
    for i in range(100):
        token = tokens[i % len(tokens)]["token"]
        tasks.append(send_request(encrypted_uid, token, url))
    return await asyncio.gather(*tasks, return_exceptions=True)

def make_request(encrypt, region, token):
    try:
        url_map = {
            "IND": "https://client.ind.freefiremobile.com/GetPlayerPersonalShow",
            "US": "https://client.us.freefiremobile.com/GetPlayerPersonalShow",
            "BR": "https://client.us.freefiremobile.com/GetPlayerPersonalShow",
        }
        url = url_map.get(region, "https://clientbp.ggpolarbear.com/GetPlayerPersonalShow")
        
        edata = bytes.fromhex(encrypt)
        headers = {
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; ASUS_Z01QD Build/PI)",
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/x-www-form-urlencoded",
            "ReleaseVersion": "OB54"
        }
        response = requests.post(url, data=edata, headers=headers, verify=False)
        decoded = visit_count_pb2.Info()
        decoded.ParseFromString(response.content)
        return decoded
    except Exception:
        return None
