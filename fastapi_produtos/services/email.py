def send_reset_password_email(email: str, token: str):
    reset_link = f"http://localhost:8000/auth/reset-password?token={token}"
    print(f"[DEBUG] Enviar e-mail para {email}")
    print(f"Link de redefinição: {reset_link}")
