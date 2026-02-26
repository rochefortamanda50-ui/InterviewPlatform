# render_app.py - SIMPLE VERSION THAT WILL WORK ON RENDER
from flask import Flask, render_template_string, request, jsonify
import json
import time
from datetime import datetime
import secrets
import os
import base64

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Store interviews
interviews = {}

# Business Analyst Questions
QUESTIONS = [
    "Describe your sales process from lead generation to closing deals also describe the metrics used to measure business development success?",
    "Describe how do you conduct market research to identify new business opportunities?",
    "Describe a time when you had to manage conflicting requirements.",
    "How do you use data analytics in your business development process also state the usage of CRM Data to identify sales opportunity and how do you improve it?",
    "How do you create a dashboard to track and forecast sales pipeline?",
    "How would you analyze the current market position and recommend growth strategies using data analytics tool.",
    "How will you use VLOOKUP,XLOOKUP and INDEX-MATCH. Explain briefly",
    "How do you create a dynamic dashboard in EXCEL that updates automatically?",
    "What are the different types of Schemas used in data modeling?",
    "State the core components of Power BI and explain in short the difference between Power BI desktop and Power BI.",
    "Imagine you are provided a table with sales data and a separate table with Date/Calendar, so why having a separate date table is considered as a best practice?",
    "Write in short the difference between Primary key and foreign key , View and a Table in SQL databases , Dimension and measure in Tableau?",
    "Describe a process of publishing a report from desktop to the service and setting up a scheduled refresh with an On premises data source.",
    "How do you document business requirements?",
    "You need to show Year-over-Year growth. Walk me through the DAX measures you would create?"
]


# SIMPLE HTML TEMPLATE - Camera works directly in browser
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Business Analyst Interview - Amul Industries</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 1000px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }
        h1 { color: #333; text-align: center; margin-bottom: 10px; }
        h2 { color: #667eea; margin: 20px 0; }
        
        /* Branding */
        .branding {
            text-align: center;
            margin-bottom: 20px;
            padding-bottom: 20px;
            border-bottom: 2px solid #f0f0f0;
        }
        .branding h3 {
            color: #ff6b6b;
            font-size: 18px;
            font-weight: normal;
            letter-spacing: 2px;
        }
        .branding .company-name {
            color: #4a5568;
            font-size: 24px;
            font-weight: bold;
            margin-top: 5px;
        }
        
        /* Camera Section - SIMPLE */
        .camera-section {
            background: #1a202c;
            border-radius: 10px;
            padding: 15px;
            margin: 20px 0;
            color: white;
        }
        .camera-container {
            position: relative;
            width: 100%;
            height: 250px;
            background: #2d3748;
            border-radius: 8px;
            overflow: hidden;
            border: 2px solid #4a5568;
        }
        #videoFeed {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
        .camera-controls {
            display: flex;
            justify-content: center;
            gap: 10px;
            margin-top: 10px;
        }
        .camera-btn {
            background: #4a5568;
            color: white;
            border: none;
            padding: 8px 20px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 14px;
        }
        .camera-btn:hover { background: #2d3748; }
        .camera-btn.active { background: #48bb78; }
        .recording-badge {
            position: absolute;
            top: 10px;
            right: 10px;
            background: rgba(0,0,0,0.7);
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 14px;
            display: flex;
            align-items: center;
            gap: 5px;
        }
        .recording-dot {
            width: 10px;
            height: 10px;
            background: #f56565;
            border-radius: 50%;
            animation: pulse 1.5s infinite;
        }
        @keyframes pulse {
            0% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.5; transform: scale(1.2); }
            100% { opacity: 1; transform: scale(1); }
        }
        
        /* Forms */
        .form-group { margin-bottom: 20px; }
        label {
            display: block;
            margin-bottom: 8px;
            color: #555;
            font-weight: 500;
        }
        input {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 16px;
        }
        input:focus { outline: none; border-color: #667eea; }
        
        /* Buttons */
        .btn {
            background: #667eea;
            color: white;
            border: none;
            padding: 12px 30px;
            border-radius: 8px;
            font-size: 16px;
            cursor: pointer;
            margin: 10px 5px;
        }
        .btn:hover { background: #5a67d8; }
        .btn-success { background: #48bb78; }
        .btn-success:hover { background: #38a169; }
        .btn-danger { background: #f56565; }
        .btn-danger:hover { background: #e53e3e; }
        
        /* Cards */
        .interview-card {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            margin: 15px 0;
            border-left: 5px solid #667eea;
        }
        
        /* Timer */
        .timer {
            font-size: 32px;
            font-weight: bold;
            color: #667eea;
            text-align: center;
            margin: 20px 0;
        }
        
        /* Warning Box */
        .warning-box {
            background: #fed7d7;
            color: #c53030;
            padding: 15px;
            border-radius: 8px;
            margin: 15px 0;
            text-align: center;
            font-weight: bold;
            animation: pulse 1s infinite;
        }
        .terminated-box {
            background: #742a2a;
            color: white;
            padding: 30px;
            border-radius: 10px;
            text-align: center;
            font-size: 20px;
            margin: 30px 0;
        }
        
        /* Status Panel */
        .status-panel {
            display: flex;
            justify-content: space-around;
            background: #f7fafc;
            padding: 15px;
            border-radius: 8px;
            margin: 20px 0;
        }
        .status-item { text-align: center; }
        .status-label { color: #718096; font-size: 14px; }
        .status-value { font-size: 24px; font-weight: bold; color: #2d3748; }
        .warning-count { color: #f56565; }
        
        /* Question Box */
        .question-box {
            background: #f7fafc;
            padding: 25px;
            border-radius: 10px;
            margin: 20px 0;
        }
        .question-text {
            font-size: 18px;
            color: #2d3748;
            margin-bottom: 20px;
            line-height: 1.6;
        }
        textarea {
            width: 100%;
            height: 150px;
            padding: 15px;
            border: 2px solid #e2e8f0;
            border-radius: 8px;
            font-size: 16px;
            resize: vertical;
            font-family: inherit;
        }
        textarea:focus { outline: none; border-color: #667eea; }
        
        /* Navigation */
        .nav-buttons {
            display: flex;
            justify-content: center;
            gap: 10px;
            margin: 20px 0;
        }
        
        /* Word Count */
        .word-count {
            text-align: right;
            color: #718096;
            font-size: 14px;
            margin-top: 5px;
        }
        
        /* Log */
        .log-container {
            background: #1a202c;
            border-radius: 8px;
            padding: 15px;
            margin-top: 20px;
        }
        .log-title { color: white; font-weight: bold; margin-bottom: 10px; }
        .log-content {
            height: 150px;
            overflow-y: auto;
            font-family: monospace;
            font-size: 12px;
            color: #48bb78;
            padding: 10px;
            background: #2d3748;
            border-radius: 5px;
        }
        
        /* Link Box */
        .link-box {
            background: #ebf4ff;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
            word-break: break-all;
            font-family: monospace;
            font-size: 14px;
        }
        
        /* Footer */
        .footer {
            text-align: center;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 2px solid #f0f0f0;
            color: #718096;
            font-size: 14px;
        }
        .footer .powered-by {
            color: #ff6b6b;
            font-weight: bold;
        }
        
        /* Layout */
        .main-layout {
            display: flex;
            gap: 20px;
        }
        .left-panel { flex: 2; }
        .right-panel { flex: 1; }
        
        /* Utility */
        .hidden { display: none; }
        .text-center { text-align: center; }
        .mt-20 { margin-top: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <!-- Branding -->
        <div class="branding">
            <h3>POWERED BY</h3>
            <div class="company-name">AMUL INDUSTRIES - INDIA, FRANCE, ITALY</div>
        </div>
        
        <!-- Simple URL Display -->
        <div style="background: #f0f9ff; padding: 15px; border-radius: 10px; margin: 20px 0; text-align: center; border: 2px dashed #667eea;">
            <p>🌍 Your interview platform is live worldwide!</p>
            <p id="currentUrl" style="font-size: 18px; font-weight: bold; color: #667eea;"></p>
        </div>
        
        <!-- Link Creation Page -->
        <div id="linkPage">
            <h1>📊 Business Analyst Interview</h1>
            <div class="interview-card">
                <h2>Create Interview Link</h2>
                <div class="form-group">
                    <label>Interview Title</label>
                    <input type="text" id="interviewTitle" value="BA Interview">
                </div>
                <div class="form-group">
                    <label>Duration (minutes)</label>
                    <input type="number" id="interviewDuration" value="45">
                </div>
                <div class="form-group">
                    <label>Max Warnings (Auto-terminate after)</label>
                    <input type="number" id="maxWarnings" value="3">
                </div>
                <button class="btn btn-success" onclick="createLink()">Generate Link</button>
            </div>
            
            <div id="linkResult" class="hidden">
                <h2>✅ Interview Created</h2>
                <div class="link-box" id="generatedLink"></div>
                <button class="btn" onclick="copyLink()">Copy Link</button>
                <button class="btn" onclick="resetPage()">Create Another</button>
            </div>
            
            <div class="footer">
                <span class="powered-by">Powered by Amul Industries - India, France, Italy</span> | © 2025
            </div>
        </div>
        
        <!-- Login Page -->
        <div id="loginPage" class="hidden">
            <h1>Business Analyst Interview</h1>
            <div class="interview-card">
                <h2>Candidate Login</h2>
                <div class="form-group">
                    <label>Full Name</label>
                    <input type="text" id="candidateName" placeholder="Enter your name">
                </div>
                <div class="form-group">
                    <label>Email</label>
                    <input type="email" id="candidateEmail" placeholder="Enter your email">
                </div>
                <button class="btn btn-success" onclick="startInterview()">Start Interview</button>
                <div id="loginError" class="text-center mt-20" style="color: red;"></div>
            </div>
        </div>
        
        <!-- Interview Page -->
        <div id="interviewPage" class="hidden">
            <h1 id="interviewTitleDisplay">Interview</h1>
            <div class="timer" id="timer">45:00</div>
            
            <div class="main-layout">
                <!-- Left Panel - Questions -->
                <div class="left-panel">
                    <div id="warningBox" class="warning-box hidden">
                        ⚠ FINAL WARNING: One more violation will terminate the interview!
                    </div>
                    
                    <div id="terminatedBox" class="terminated-box hidden">
                        ❌ INTERVIEW TERMINATED<br>Maximum warnings (3) exceeded.
                    </div>
                    
                    <div class="status-panel">
                        <div class="status-item">
                            <div class="status-label">Tab Switches</div>
                            <div class="status-value" id="tabCount">0</div>
                        </div>
                        <div class="status-item">
                            <div class="status-label">Warnings</div>
                            <div class="status-value warning-count" id="warningCount">0</div>
                        </div>
                        <div class="status-item">
                            <div class="status-label">Max Warnings</div>
                            <div class="status-value" id="maxWarningCount">3</div>
                        </div>
                    </div>
                    
                    <div class="question-box">
                        <div class="question-text" id="questionText">Loading...</div>
                        <textarea id="answerInput" placeholder="Type your answer here..." disabled></textarea>
                        <div class="word-count" id="wordCount">Words: 0</div>
                    </div>
                    
                    <div class="nav-buttons">
                        <button class="btn" onclick="prevQuestion()" id="prevBtn" disabled>Previous</button>
                        <button class="btn" onclick="nextQuestion()" id="nextBtn" disabled>Next</button>
                        <button class="btn btn-success" onclick="submitInterview()" id="submitBtn" disabled>Submit</button>
                    </div>
                </div>
                
                <!-- Right Panel - Camera -->
                <div class="right-panel">
                    <div class="camera-section">
                        <h3 style="color: white; margin-bottom: 10px;">📹 Live Recording</h3>
                        <div class="camera-container">
                            <video id="videoFeed" autoplay playsinline></video>
                            <div class="recording-badge" id="recordingBadge">
                                <span class="recording-dot"></span>
                                <span id="recordingStatus">READY</span>
                            </div>
                        </div>
                        <div class="camera-controls">
                            <button class="camera-btn" id="startCameraBtn" onclick="startCamera()">Start Camera</button>
                            <button class="camera-btn" id="stopCameraBtn" onclick="stopCamera()" disabled>Stop Camera</button>
                        </div>
                        <p id="cameraStatus" style="color: #a0aec0; font-size: 12px; margin-top: 5px;">Click Start Camera to begin</p>
                    </div>
                    
                    <div class="log-container">
                        <div class="log-title">Activity Log</div>
                        <div class="log-content" id="activityLog">[System] Ready<br></div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Thank You Page -->
        <div id="thankYouPage" class="hidden text-center">
            <h1>✅ Interview Complete!</h1>
            <p style="margin: 30px 0;">Thank you for completing the interview.</p>
            <button class="btn" onclick="window.location.href='/'">Close</button>
        </div>
    </div>
    
    <script>
        // Display current URL
        document.getElementById('currentUrl').innerHTML = window.location.href;
        
        // Global variables
        let currentQuestion = 0;
        let questions = [];
        let answers = [];
        let tabSwitches = 0;
        let warnings = 0;
        let maxWarnings = 3;
        let timeLeft = 2700;
        let timerInterval;
        let interviewActive = false;
        let interviewTerminated = false;
        let interviewId = null;
        let candidateName = '';
        
        // Camera variables
        let videoStream = null;
        let mediaRecorder = null;
        let recordedChunks = [];
        let cameraActive = false;
        
        function getInterviewId() {
            let urlParams = new URLSearchParams(window.location.search);
            return urlParams.get('id');
        }
        
        window.onload = function() {
            let id = getInterviewId();
            if (id) {
                checkInterview(id);
            }
        };
        
        function checkInterview(id) {
            fetch('/check_interview/' + id)
                .then(res => res.json())
                .then(data => {
                    if (data.exists) {
                        interviewId = id;
                        maxWarnings = data.max_warnings;
                        document.getElementById('linkPage').classList.add('hidden');
                        document.getElementById('loginPage').classList.remove('hidden');
                        document.getElementById('maxWarningCount').innerHTML = maxWarnings;
                    } else {
                        alert('Invalid interview link');
                    }
                });
        }
        
        function createLink() {
            let title = document.getElementById('interviewTitle').value;
            let duration = document.getElementById('interviewDuration').value;
            let maxWarns = document.getElementById('maxWarnings').value;
            
            fetch('/create_interview', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    title: title,
                    duration: parseInt(duration),
                    max_warnings: parseInt(maxWarns)
                })
            })
            .then(res => res.json())
            .then(data => {
                let link = window.location.origin + '/?id=' + data.id;
                document.getElementById('generatedLink').innerHTML = link;
                document.getElementById('linkResult').classList.remove('hidden');
            });
        }
        
        function copyLink() {
            let link = document.getElementById('generatedLink').innerHTML;
            navigator.clipboard.writeText(link);
            alert('Link copied!');
        }
        
        function resetPage() {
            window.location.href = '/';
        }
        
        // SIMPLE Camera functions - NO SOCKET.IO NEEDED
        function startCamera() {
            if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
                navigator.mediaDevices.getUserMedia({ 
                    video: true,
                    audio: true 
                })
                .then(function(stream) {
                    videoStream = stream;
                    let video = document.getElementById('videoFeed');
                    video.srcObject = stream;
                    
                    cameraActive = true;
                    document.getElementById('startCameraBtn').disabled = true;
                    document.getElementById('stopCameraBtn').disabled = false;
                    document.getElementById('cameraStatus').innerHTML = '✅ Camera active';
                    document.getElementById('recordingStatus').innerHTML = 'REC';
                    
                    // Simple recording
                    recordedChunks = [];
                    mediaRecorder = new MediaRecorder(stream);
                    
                    mediaRecorder.ondataavailable = function(event) {
                        if (event.data.size > 0) {
                            recordedChunks.push(event.data);
                        }
                    };
                    
                    mediaRecorder.onstop = function() {
                        const blob = new Blob(recordedChunks, { type: 'video/webm' });
                        // Save locally
                        const url = URL.createObjectURL(blob);
                        const a = document.createElement('a');
                        a.href = url;
                        a.download = `interview_${candidateName}_${new Date().getTime()}.webm`;
                        a.click();
                        
                        document.getElementById('recordingStatus').innerHTML = 'SAVED';
                    };
                    
                    mediaRecorder.start();
                    logActivity('Camera and recording started');
                })
                .catch(function(error) {
                    alert('Camera access denied: ' + error.message);
                    logActivity('Camera error: ' + error.message);
                });
            } else {
                alert('Camera not supported in this browser');
            }
        }
        
        function stopCamera() {
            if (videoStream) {
                videoStream.getTracks().forEach(track => track.stop());
                videoStream = null;
            }
            
            if (mediaRecorder && mediaRecorder.state !== 'inactive') {
                mediaRecorder.stop();
            }
            
            cameraActive = false;
            document.getElementById('startCameraBtn').disabled = false;
            document.getElementById('stopCameraBtn').disabled = true;
            document.getElementById('cameraStatus').innerHTML = '❌ Camera stopped';
            document.getElementById('recordingStatus').innerHTML = 'STOPPED';
            logActivity('Camera stopped');
        }
        
        function startInterview() {
            candidateName = document.getElementById('candidateName').value;
            let email = document.getElementById('candidateEmail').value;
            
            if (!candidateName || !email) {
                document.getElementById('loginError').innerHTML = 'Please enter name and email';
                return;
            }
            
            fetch('/start_interview', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    interview_id: interviewId,
                    name: candidateName,
                    email: email
                })
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    questions = data.questions;
                    answers = new Array(questions.length).fill('');
                    timeLeft = data.duration * 60;
                    maxWarnings = data.max_warnings;
                    
                    document.getElementById('loginPage').classList.add('hidden');
                    document.getElementById('interviewPage').classList.remove('hidden');
                    document.getElementById('interviewTitleDisplay').innerHTML = 'Interview: ' + candidateName;
                    document.getElementById('maxWarningCount').innerHTML = maxWarnings;
                    
                    document.getElementById('prevBtn').disabled = false;
                    document.getElementById('nextBtn').disabled = false;
                    document.getElementById('submitBtn').disabled = false;
                    document.getElementById('answerInput').disabled = false;
                    
                    interviewActive = true;
                    interviewTerminated = false;
                    
                    startTimer();
                    showQuestion();
                    logActivity('Interview started');
                    
                    document.addEventListener('visibilitychange', function() {
                        if (document.hidden && interviewActive && !interviewTerminated) {
                            tabSwitches++;
                            warnings++;
                            
                            document.getElementById('tabCount').innerHTML = tabSwitches;
                            document.getElementById('warningCount').innerHTML = warnings;
                            
                            logActivity('Warning ' + warnings + '/' + maxWarnings);
                            
                            if (warnings >= maxWarnings) {
                                terminateInterview();
                            } else if (warnings >= maxWarnings - 1) {
                                document.getElementById('warningBox').classList.remove('hidden');
                            }
                        }
                    });
                }
            });
        }
        
        function startTimer() {
            timerInterval = setInterval(function() {
                if (timeLeft > 0 && interviewActive && !interviewTerminated) {
                    timeLeft--;
                    let mins = Math.floor(timeLeft / 60);
                    let secs = timeLeft % 60;
                    document.getElementById('timer').innerHTML = 
                        (mins < 10 ? '0' + mins : mins) + ':' + 
                        (secs < 10 ? '0' + secs : secs);
                    
                    if (timeLeft <= 0) {
                        submitInterview();
                    }
                }
            }, 1000);
        }
        
        function showQuestion() {
            if (interviewTerminated) return;
            document.getElementById('questionText').innerHTML = 
                '<strong>Question ' + (currentQuestion + 1) + '/' + questions.length + ':</strong><br><br>' + 
                questions[currentQuestion];
            document.getElementById('answerInput').value = answers[currentQuestion] || '';
            updateWordCount();
        }
        
        function updateWordCount() {
            let text = document.getElementById('answerInput').value;
            let words = text.trim() ? text.trim().split(/\s+/).length : 0;
            document.getElementById('wordCount').innerHTML = 'Words: ' + words;
        }
        
        document.getElementById('answerInput').addEventListener('keyup', updateWordCount);
        
        function prevQuestion() {
            if (interviewTerminated) return;
            saveAnswer();
            if (currentQuestion > 0) {
                currentQuestion--;
                showQuestion();
            }
        }
        
        function nextQuestion() {
            if (interviewTerminated) return;
            saveAnswer();
            if (currentQuestion < questions.length - 1) {
                currentQuestion++;
                showQuestion();
            }
        }
        
        function saveAnswer() {
            if (interviewTerminated) return;
            answers[currentQuestion] = document.getElementById('answerInput').value;
        }
        
        function terminateInterview() {
            interviewActive = false;
            interviewTerminated = true;
            clearInterval(timerInterval);
            stopCamera();
            
            document.getElementById('interviewPage').classList.add('hidden');
            document.getElementById('terminatedBox').classList.remove('hidden');
            
            logActivity('Interview terminated - 3 warnings');
            
            fetch('/terminate_interview', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    interview_id: interviewId,
                    name: candidateName,
                    warnings: warnings
                })
            });
        }
        
        function submitInterview() {
            if (!interviewActive || interviewTerminated) return;
            
            saveAnswer();
            interviewActive = false;
            clearInterval(timerInterval);
            stopCamera();
            
            fetch('/submit_interview', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    interview_id: interviewId,
                    name: candidateName,
                    answers: answers,
                    tab_switches: tabSwitches,
                    warnings: warnings
                })
            })
            .then(res => res.json())
            .then(data => {
                document.getElementById('interviewPage').classList.add('hidden');
                document.getElementById('thankYouPage').classList.remove('hidden');
                logActivity('Interview submitted');
            });
        }
        
        function logActivity(message) {
            let log = document.getElementById('activityLog');
            let time = new Date().toLocaleTimeString();
            log.innerHTML += '[' + time + '] ' + message + '<br>';
            log.scrollTop = log.scrollHeight;
        }
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/create_interview', methods=['POST'])
def create_interview():
    data = request.json
    interview_id = secrets.token_hex(8)
    
    interviews[interview_id] = {
        'id': interview_id,
        'title': data['title'],
        'duration': data['duration'],
        'max_warnings': data['max_warnings'],
        'questions': QUESTIONS,
        'created': datetime.now().strftime('%Y-%m-%d %H:%M'),
        'status': 'waiting'
    }
    
    return jsonify({'id': interview_id})

@app.route('/check_interview/<interview_id>')
def check_interview(interview_id):
    exists = interview_id in interviews
    max_warnings = interviews[interview_id]['max_warnings'] if exists else 0
    return jsonify({'exists': exists, 'max_warnings': max_warnings})

@app.route('/start_interview', methods=['POST'])
def start_interview():
    data = request.json
    interview_id = data['interview_id']
    
    if interview_id not in interviews:
        return jsonify({'success': False})
    
    interview = interviews[interview_id]
    interview['status'] = 'active'
    interview['candidate'] = data['name']
    interview['candidate_email'] = data['email']
    interview['start_time'] = time.time()
    
    return jsonify({
        'success': True,
        'questions': interview['questions'],
        'duration': interview['duration'],
        'max_warnings': interview['max_warnings']
    })

@app.route('/terminate_interview', methods=['POST'])
def terminate_interview():
    data = request.json
    interview_id = data['interview_id']
    
    if interview_id in interviews:
        interviews[interview_id]['status'] = 'terminated'
        interviews[interview_id]['warnings'] = data['warnings']
    
    return jsonify({'success': True})

@app.route('/submit_interview', methods=['POST'])
def submit_interview():
    data = request.json
    interview_id = data['interview_id']
    
    if interview_id in interviews:
        interview = interviews[interview_id]
        interview['status'] = 'completed'
        
        if interview.get('start_time'):
            duration = int(time.time() - interview['start_time'])
        else:
            duration = 0
        
        # Save report
        report = {
            'candidate': data['name'],
            'timestamp': datetime.now().isoformat(),
            'duration': duration,
            'answers': data['answers'],
            'tab_switches': data['tab_switches'],
            'warnings': data['warnings'],
            'questions': interview['questions']
        }
        
        filename = 'interview_' + datetime.now().strftime('%Y%m%d_%H%M%S') + '.json'
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
    
    return jsonify({'success': True})

if __name__ == '__main__':
    print('\n' + '='*60)
    print('🌍 BUSINESS ANALYST INTERVIEW PLATFORM')
    print('='*60)
    print('\n✅ Server starting...')
    print('\n📌 This version WILL WORK on Render!')
    print('\n📌 Features:')
    print('   - Powered by Amul Industries')
    print('   - Camera works in browser')
    print('   - No complex Socket.IO needed')
    print('   - Auto-terminates after 3 warnings')
    print('\n' + '='*60 + '\n')
    
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
