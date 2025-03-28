import hashlib
import random
import smtplib
from email.message import EmailMessage
from database.db_config import get_db_connection

# Password Hashing
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Email Verification Code Generator
def generate_verification_code():
    return str(random.randint(100000, 999999))

# Email Sending Logic
def send_verification_email(email, code):
    sender_email = "1realmakaveli@proton.me"  # Corrected email
    sender_password = "430AMclub!"  # Corrected password

    msg = EmailMessage()
    msg['Subject'] = 'Wildlife Conservation System - Email Verification Code'
    msg['From'] = sender_email
    msg['To'] = email
    msg.set_content(f'Your verification code is: {code}')

    try:
        with smtplib.SMTP('smtp.protonmail.com', 465) as server:
            server.starttls()  # Ensures encrypted connection
            server.login(sender_email, sender_password)
            server.send_message(msg)
        print("✅ Verification email sent successfully.")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

# Save New User
def create_user(username, email, password, verification_code):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO Users (username, email, password, verified, verification_code)
        VALUES (%s, %s, %s, %s, %s)
    ''', (username, email, hash_password(password), 0, verification_code))

    conn.commit()
    conn.close()

# Verify Email Code
def verify_email_code(email, code):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT verification_code FROM Users WHERE email = %s', (email,))
    result = cursor.fetchone()

    if result and result[0] == code:
        cursor.execute('UPDATE Users SET verified = 1 WHERE email = %s', (email,))
        conn.commit()
        conn.close()
        return True

    conn.close()
    return False
