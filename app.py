# app.py
from flask import Flask, render_template, request, jsonify
import threading
import automation  # automation.py file ko import karega
import os

app = Flask(__name__)

active_sessions = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start-automation', methods=['POST'])
def start_automation():
    data = request.json

    number = int(data.get('number', 1))
    meeting_code = data.get('meeting_code')
    passcode = data.get('passcode')
    end_time = data.get('end_time')

    if not meeting_code or not passcode:
        return jsonify({'error': 'Meeting code and passcode required'}), 400

    session_id = f"session_{len(active_sessions) + 1}"
    
    # State initialize karo backend thread start hone se pehle
    active_sessions[session_id] = {
        'status': 'running',
        'details': data
    }

    def run_automation():
        try:
            automation.run_zoom_automation(
                number,
                meeting_code,
                passcode,
                end_time
            )
            active_sessions[session_id]['status'] = 'completed'
        except Exception as e:
            active_sessions[session_id]['status'] = 'error'
            active_sessions[session_id]['error'] = str(e)

    # Thread separate run hoga taki API request hang na ho
    thread = threading.Thread(target=run_automation, daemon=True)
    thread.start()

    return jsonify({
        'success': True,
        'session_id': session_id,
        'message': f'{number} bots started successfully!'
    })

@app.route('/status/<session_id>')
def get_status(session_id):
    session = active_sessions.get(session_id)
    if session:
        return jsonify(session)
    return jsonify({'error': 'Session not found'}), 404

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 7860))
    app.run(host='0.0.0.0', port=port)