from flask import Flask, request, jsonify
import json
import asyncio
from collections import OrderedDict
from .core import load_user_tokens, enc, make_request, send_multiple_requests

def create_api_server(valid_keys, daily_limit=20):
    app = Flask(__name__)
    used_count = {"count": 0}

    @app.route('/like', methods=['GET'])
    def handle_requests():
        api_key = request.args.get("key")
        if api_key not in valid_keys:
            return jsonify({"error": "Invalid API key", "status": 3}), 401

        uid = request.args.get("uid")
        region = request.args.get("region", "").upper()
        
        if not uid or not region:
            return jsonify({"error": "UID and region are required"}), 400

        try:
            tokens = load_user_tokens(region)
            token = tokens[0]['token']
            encrypted_uid = enc(uid)
            
            before = make_request(encrypted_uid, region, token)
            before_like = before.AccountInfo.Likes

            url_map = {
                "IND": "https://client.ind.freefiremobile.com/LikeProfile",
                "US": "https://client.us.freefiremobile.com/LikeProfile",
                "BR": "https://client.us.freefiremobile.com/LikeProfile",
            }
            url = url_map.get(region, "https://clientbp.ggpolarbear.com/LikeProfile")

            asyncio.run(send_multiple_requests(uid, region, url))

            after = make_request(encrypted_uid, region, token)
            after_like = after.AccountInfo.Likes
            like_given = after_like - before_like
            status = 1 if like_given > 0 else 2

            if status == 1:
                used_count["count"] += 1

            remaining = max(daily_limit - used_count["count"], 0)

            result = OrderedDict([
                ("LikesGivenByAPI", like_given),
                ("LikesafterCommand", after_like),
                ("LikesbeforeCommand", before_like),
                ("PlayerNickname", after.AccountInfo.PlayerNickname),
                ("UID", after.AccountInfo.UID),
                ("status", status),
                ("daily_limit", daily_limit),
                ("used", used_count["count"]),
                ("remaining", remaining)
            ])
            return jsonify(result)

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/remain', methods=['GET'])
    def remain_info():
        remaining = max(daily_limit - used_count["count"], 0)
        return jsonify({
            "daily_limit": daily_limit,
            "remaining": remaining,
            "used": used_count["count"]
        })

    return app

# CLI entry point
def start_server():
    import argparse
    parser = argparse.ArgumentParser(description="Free Fire Like API")
    parser.add_argument("--port", type=int, default=5000)
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--key", required=True, help="API key")
    args = parser.parse_args()
    
    app = create_api_server([args.key], daily_limit=args.limit)
    app.run(host="0.0.0.0", port=args.port)