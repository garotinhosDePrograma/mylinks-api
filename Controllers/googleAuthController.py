from flask import Blueprint, request, jsonify, redirect
from flask_cors import cross_origin
from extensions import limiter
import requests
import jwt
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from Workers.userWorker import UserWorker
from Repositories.userRepository import UserRepository
import secrets

load_dotenv()

google_auth_bp = Blueprint("google_auth", __name__)
user_worker = UserWorker()
user_repo = UserRepository()

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI", "https://pygre.onrender.com/auth/google/callback")
SECRET_KEY = os.getenv("SECRET_KEY")

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"


@google_auth_bp.route("/auth/google", methods=["GET"])
@cross_origin()
def google_login():
    state = secrets.token_urlsafe(32)
    
    params = {
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "state": state,
        "access_type": "offline",
        "prompt": "select_account"
    }
    
    auth_url = f"{GOOGLE_AUTH_URL}?{'&'.join([f'{k}={v}' for k, v in params.items()])}"
    
    return jsonify({
        "auth_url": auth_url,
        "state": state
    }), 200


@google_auth_bp.route("/auth/google/callback", methods=["GET"])
@cross_origin()
@limiter.limit("10 per minute")
def google_callback():
    code = request.args.get("code")
    error = request.args.get("error")
    
    if error:
        return redirect(f"https://mylinks-352x.onrender.com/login.html?error={error}")
    
    if not code:
        return redirect("https://mylinks-352x.onrender.com/login.html?error=no_code")
    
    try:
        token_data = {
            "code": code,
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "redirect_uri": GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code"
        }
        
        token_response = requests.post(GOOGLE_TOKEN_URL, data=token_data)
        token_response.raise_for_status()
        tokens = token_response.json()
        
        access_token = tokens.get("access_token")
        
        headers = {"Authorization": f"Bearer {access_token}"}
        userinfo_response = requests.get(GOOGLE_USERINFO_URL, headers=headers)
        userinfo_response.raise_for_status()
        user_info = userinfo_response.json()
        
        google_id = user_info.get("id")
        email = user_info.get("email")
        name = user_info.get("name", "")
        picture = user_info.get("picture", "")
        
        if not email:
            return redirect("https://mylinks-352x.onrender.com/login.html?error=no_email")
        
        user = user_repo.find_by_email(email)
        
        if not user:
            base_username = name.lower().replace(" ", "_") if name else email.split("@")[0]
            username = base_username
            counter = 1
            
            while user_repo.find_by_username(username):
                username = f"{base_username}{counter}"
                counter += 1
            
            random_password = secrets.token_urlsafe(32)
            
            user = user_repo.create(username, email, random_password)
            
            if picture:
                user_repo.update_foto(user.id, picture)
        
        access_token_jwt = jwt.encode(
            {
                "id": user.id,
                "exp": datetime.utcnow() + timedelta(minutes=15),
                "type": "access"
            },
            SECRET_KEY,
            algorithm="HS256"
        )
        
        refresh_token_jwt = jwt.encode(
            {
                "id": user.id,
                "exp": datetime.utcnow() + timedelta(days=7),
                "type": "refresh"
            },
            SECRET_KEY,
            algorithm="HS256"
        )
        
        redirect_url = (
            f"https://mylinks-352x.onrender.com/login.html?"
            f"access_token={access_token_jwt}&"
            f"refresh_token={refresh_token_jwt}&"
            f"user_id={user.id}&"
            f"username={user.username}&"
            f"email={user.email}&"
            f"foto_perfil={user.foto_perfil or ''}"
        )
        
        return redirect(redirect_url)
        
    except requests.exceptions.RequestException as e:
        print(f"Erro ao comunicar com Google: {e}")
        return redirect("https://mylinks-352x.onrender.com/login.html?error=google_error")
    
    except Exception as e:
        print(f"Erro no callback do Google: {e}")
        return redirect("https://mylinks-352x.onrender.com/login.html?error=server_error")


@google_auth_bp.route("/auth/google/mobile", methods=["POST"])
@cross_origin()
@limiter.limit("10 per minute")
def google_login_mobile():
    data = request.get_json()
    
    if not data or "id_token" not in data:
        return jsonify({"error": "Token não fornecido"}), 400
    
    id_token = data["id_token"]
    
    try:
        response = requests.get(
            f"https://oauth2.googleapis.com/tokeninfo?id_token={id_token}"
        )
        response.raise_for_status()
        token_info = response.json()
        
        if token_info.get("aud") != GOOGLE_CLIENT_ID:
            return jsonify({"error": "Token inválido"}), 401
        
        google_id = token_info.get("sub")
        email = token_info.get("email")
        name = token_info.get("name", "")
        picture = token_info.get("picture", "")
        
        if not email:
            return jsonify({"error": "Email não encontrado no token"}), 400
        
        user = user_repo.find_by_email(email)
        
        if not user:
            base_username = name.lower().replace(" ", "_") if name else email.split("@")[0]
            username = base_username
            counter = 1
            
            while user_repo.find_by_username(username):
                username = f"{base_username}{counter}"
                counter += 1
            
            random_password = secrets.token_urlsafe(32)
            user = user_repo.create(username, email, random_password)
            
            if picture:
                user_repo.update_foto(user.id, picture)
        
        access_token_jwt = jwt.encode(
            {
                "id": user.id,
                "exp": datetime.utcnow() + timedelta(minutes=15),
                "type": "access"
            },
            SECRET_KEY,
            algorithm="HS256"
        )
        
        refresh_token_jwt = jwt.encode(
            {
                "id": user.id,
                "exp": datetime.utcnow() + timedelta(days=7),
                "type": "refresh"
            },
            SECRET_KEY,
            algorithm="HS256"
        )
        
        return jsonify({
            "access_token": access_token_jwt,
            "refresh_token": refresh_token_jwt,
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "foto_perfil": user.foto_perfil
            }
        }), 200
        
    except requests.exceptions.RequestException as e:
        print(f"Erro ao validar token do Google: {e}")
        return jsonify({"error": "Erro ao validar token"}), 500
    
    except Exception as e:
        print(f"Erro no login mobile do Google: {e}")
        return jsonify({"error": "Erro no servidor"}), 500
