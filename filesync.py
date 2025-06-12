import http.server
import socketserver
import os
import socket
from urllib.parse import unquote
import json
from datetime import datetime

PORT = 8080
DIRECTORY = os.getcwd() 
BOUNDARY = b"----WebKitFormBoundary" 
TEXT_FILE = os.path.join(DIRECTORY, ".shared_text.json")

class FileSharingHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            
            # Load text history if exists
            text_history = []
            if os.path.exists(TEXT_FILE):
                with open(TEXT_FILE, 'r') as f:
                    try:
                        text_history = json.load(f)
                    except:
                        text_history = []
            
            html = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>⚡ Pikachu FileSync</title>
                <style>
                    body {{
                        font-family: 'Helvetica Neue', Arial, sans-serif;
                        background-color: #f8f1e9;
                        margin: 0;
                        padding: 15px;
                        display: flex;
                        justify-content: center;
                        min-height: 100vh;
                        color: #2c3e50;
                    }}
                    .container {{
                        max-width: 1200px;
                        width: 100%;
                        box-sizing: border-box;
                    }}
                    .header {{
                        text-align: center;
                        margin-bottom: 1.5rem;
                        padding: 1rem;
                        background: linear-gradient(180deg, #d4a5a5, #f8f1e9);
                        border-radius: 8px;
                    }}
                    .header h1 {{
                        font-size: clamp(1.8rem, 5vw, 2.2rem);
                        margin: 0;
                        color: #2c3e50;
                        font-weight: 300;
                        letter-spacing: 1px;
                    }}
                    .header p {{
                        color: #5c6b73;
                        font-size: clamp(0.9rem, 3vw, 1rem);
                        margin-top: 0.5rem;
                    }}
                    .signature {{
                        color: #5c6b73;
                        font-size: clamp(0.75rem, 2vw, 0.8rem);
                        margin-top: 0.5rem;
                    }}
                    .signature a {{
                        color: #2a9d8f;
                        text-decoration: none;
                        margin: 0 0.5rem;
                    }}
                    .signature a:hover {{
                        text-decoration: underline;
                    }}
                    .card {{
                        background-color: #ffffff;
                        border-radius: 8px;
                        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                        padding: 1.5rem;
                        margin-bottom: 1.5rem;
                        border: 1px solid #e2d9c8;
                        box-sizing: border-box;
                    }}
                    .card h2 {{
                        font-size: clamp(1.2rem, 4vw, 1.4rem);
                        color: #2c3e50;
                        margin-bottom: 1rem;
                        font-weight: 400;
                    }}
                    .file-input-container {{
                        display: flex;
                        flex-wrap: wrap;
                        align-items: center;
                        gap: 0.5rem;
                        margin-bottom: 0.5rem;
                    }}
                    .file-input {{
                        display: none;
                    }}
                    .browse-button {{
                        padding: 0.5rem 1rem;
                        background-color: #6b7280;
                        color: #ffffff;
                        border-radius: 6px;
                        cursor: pointer;
                        transition: background-color 0.3s ease;
                        font-size: clamp(0.85rem, 2.5vw, 0.9rem);
                        flex: 0 0 auto;
                    }}
                    .browse-button:hover {{
                        background-color: #4b5563;
                    }}
                    .file-name {{
                        flex: 1;
                        padding: 0.5rem;
                        border: 1px solid #e2d9c8;
                        border-radius: 6px;
                        background-color: #f8fafc;
                        color: #2c3e50;
                        font-size: clamp(0.8rem, 2.5vw, 0.85rem);
                        overflow: hidden;
                        text-overflow: ellipsis;
                        white-space: nowrap;
                        min-width: 0;
                    }}
                    .upload-button {{
                        padding: 0.5rem 1rem;
                        background-color: #2a9d8f;
                        color: #ffffff;
                        border: none;
                        border-radius: 6px;
                        cursor: pointer;
                        font-size: clamp(0.85rem, 2.5vw, 0.9rem);
                        transition: background-color 0.3s ease;
                        flex: 0 0 auto;
                    }}
                    .upload-button:disabled {{
                        background-color: #a0aec0;
                        cursor: not-allowed;
                    }}
                    .upload-button:hover:not(:disabled) {{
                        background-color: #21867a;
                    }}
                    .text-button, .clear-button {{
                        padding: 0.5rem 1rem;
                        background-color: #2a9d8f;
                        color: #ffffff;
                        border: none;
                        border-radius: 6px;
                        cursor: pointer;
                        font-size: clamp(0.85rem, 2.5vw, 0.9rem);
                        transition: background-color 0.3s ease;
                        flex: 1;
                    }}
                    .text-button:disabled, .clear-button:disabled {{
                        background-color: #a0aec0;
                        cursor: not-allowed;
                    }}
                    .text-button:hover:not(:disabled), .clear-button:hover:not(:disabled) {{
                        background-color: #21867a;
                    }}
                    .text-actions {{
                        display: flex;
                        gap: 0.5rem;
                        justify-content: center;
                        flex-wrap: wrap;
                        margin-top: 0.5rem;
                    }}
                    .progress-container {{
                        display: none;
                        margin-top: 0.5rem;
                    }}
                    .progress-bar {{
                        width: 100%;
                        background-color: #e2e8f0;
                        border-radius: 6px;
                        height: 0.4rem;
                        overflow: hidden;
                    }}
                    .progress-fill {{
                        height: 100%;
                        background-color: #2a9d8f;
                        width: 0%;
                        transition: width 0.3s ease;
                    }}
                    .progress-text {{
                        font-size: clamp(0.75rem, 2vw, 0.8rem);
                        color: #5c6b73;
                        margin-top: 0.3rem;
                    }}
                    .message {{
                        display: none;
                        margin-top: 0.5rem;
                        font-size: clamp(0.75rem, 2vw, 0.8rem);
                    }}
                    .success {{
                        color: #2a9d8f;
                    }}
                    .error {{
                        color: #e63946;
                    }}
                    .file-list ul, .text-history ul {{
                        list-style: none;
                        padding: 0;
                        margin: 0;
                    }}
                    .file-list li, .text-history li {{
                        display: flex;
                        flex-wrap: wrap;
                        align-items: center;
                        padding: 0.5rem;
                        border-bottom: 1px solid #e2d9c8;
                        transition: background-color 0.2s;
                        gap: 0.5rem;
                    }}
                    .file-list li:last-child, .text-history li:last-child {{
                        border-bottom: none;
                    }}
                    .file-list li:hover, .text-history li:hover {{
                        background-color: #f1e9db;
                    }}
                    .file-list a {{
                        color: #2a9d8f;
                        text-decoration: none;
                        flex: 1;
                        min-width: 0;
                        overflow: hidden;
                        text-overflow: ellipsis;
                        white-space: nowrap;
                    }}
                    .file-list a:hover {{
                        text-decoration: underline;
                    }}
                    .file-icon, .text-icon {{
                        margin-right: 0.5rem;
                        font-size: clamp(1rem, 3vw, 1.1rem);
                        flex: 0 0 auto;
                    }}
                    .file-size, .text-timestamp {{
                        color: #5c6b73;
                        font-size: clamp(0.75rem, 2vw, 0.8rem);
                        flex: 0 0 auto;
                        margin-right: 0.5rem;
                    }}
                    .download-button, .copy-button {{
                        padding: 0.4rem 0.8rem;
                        background-color: #264653;
                        color: #ffffff;
                        border-radius: 6px;
                        text-decoration: none;
                        font-size: clamp(0.75rem, 2vw, 0.8rem);
                        transition: background-color 0.3s ease;
                        border: none;
                        cursor: pointer;
                        flex: 0 0 auto;
                    }}
                    .download-button:hover, .copy-button:hover {{
                        background-color: #1d3c48;
                    }}
                    .textarea {{
                        width: 100%;
                        height: 40px;
                        padding: 0.5rem;
                        border: 1px solid #e2d9c8;
                        border-radius: 6px;
                        background-color: #f8fafc;
                        color: #2c3e50;
                        font-size: clamp(0.8rem, 2.5vw, 0.85rem);
                        resize: vertical;
                        margin-bottom: 0.5rem;
                        box-sizing: border-box;
                    }}
                    .text-content {{
                        flex: 1;
                        min-width: 0;
                        word-wrap: break-word;
                        white-space: pre-wrap;
                        font-size: clamp(0.8rem, 2.5vw, 0.85rem);
                        color: #2c3e50;
                        line-height: 1.4;
                        max-height: 80px;
                        overflow-y: auto;
                        padding: 0.5rem;
                        border: 1px solid #e2d9c8;
                        border-radius: 6px;
                        background-color: #f8fafc;
                    }}
                    @media (min-width: 601px) {{
                        .text-button, .clear-button {{
                            flex: 1;
                            min-width: 0;
                            max-width: none;
                        }}
                        .text-actions {{
                            justify-content: space-between;
                        }}
                    }}
                    @media (max-width: 600px) {{
                        body {{
                            padding: 10px;
                        }}
                        .container {{
                            max-width: 100%;
                        }}
                        .card {{
                            padding: 1rem;
                        }}
                        .file-input-container {{
                            flex-direction: column;
                            align-items: stretch;
                        }}
                        .browse-button, .file-name, .upload-button {{
                            width: 100%;
                            box-sizing: border-box;
                        }}
                        .file-list li, .text-history li {{
                            flex-direction: column;
                            align-items: flex-start;
                        }}
                        .file-size, .text-timestamp {{
                            margin-right: 0;
                            margin-bottom: 0.5rem;
                        }}
                        .download-button, .copy-button {{
                            width: 100%;
                            text-align: center;
                            max-width: 150px;
                        }}
                        .text-content {{
                            width: 100%;
                            max-width: 100%;
                            overflow-wrap: break-word;
                            word-break: break-all;
                        }}
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>⚡Pikachu FileSync</h1>
                        <p>Pika-pika! Share files and text with Pokémon power!</p>
                    
                        <div class="signature">
                            Created by Husnain Shahid | 
                            <a href="https://www.linkedin.com/in/husnain-shahid-5b6b471b8" target="_blank">LinkedIn</a> | 
                            <a href="https://github.com/husnain002" target="_blank">GitHub</a>
                        </div>
                    </div>
                    <div class="card">
                        <h2>📋 Share Text</h2>
                        <form id="textForm">
                            <textarea id="textInput" class="textarea" placeholder="Paste your text here..."></textarea>
                            <div class="text-actions">
                                <button type="submit" id="textButton" class="text-button">📤 Share Text</button>
                                <button type="button" id="clearHistoryButton" class="clear-button">🗑️ Clear History</button>
                            </div>
                        </form>
                        <div id="textMessage" class="message success">✅ Pika! Text shared!</div>
                        <div id="textErrorMessage" class="message error">❌ Pika... Text sharing failed: <span></span></div>
                        <div id="copyMessage" class="message success">✅ Pika! Text copied!</div>
                    </div>
            """
            # Only show text history if there are entries
            if text_history:
                html += """
                    <div class="card text-history">
                        <h2>📜 Text History</h2>
                        <ul>
                """
                for entry in reversed(text_history[-5:]):
                    html += f"""
                            <li>
                                <span class="text-icon">📋</span>
                                <span class="text-content">{entry['text'].replace('<', '<').replace('>', '>').replace("'", "'")}</span>
                                <span class="text-timestamp">{entry['timestamp']}</span>
                                <button class="copy-button" data-text="{entry['text'].replace('"', '"').replace('\\', '\\\\')}">📋 Copy</button>
                            </li>
                    """
                html += """
                        </ul>
                    </div>
                """
            
            html += """
                    <div class="card">
                        <h2>⚡ Upload File</h2>
                        <form id="uploadForm" enctype="multipart/form-data" method="post">
                            <div class="file-input-container">
                                <label for="fileInput" class="browse-button">📂 Browse</label>
                                <input type="file" name="file" id="fileInput" class="file-input"/>
                                <span id="fileName" class="file-name">No file selected</span>
                                <button type="submit" id="uploadButton" class="upload-button" disabled>⬆ Upload File</button>
                            </div>
                        </form>
                        <div id="progressContainer" class="progress-container">
                            <div class="progress-bar">
                                <div id="progressBar" class="progress-fill"></div>
                            </div>
                            <div id="progressText" class="progress-text">Uploading: 0%</div>
                        </div>
                        <div id="uploadMessage" class="message success">✅ Pika! File uploaded!</div>
                        <div id="errorMessage" class="message error">❌ Pika... Upload failed: <span></span></div>
                    </div>
                    
                    <div class="card file-list">
                        <h2>📂 Available Files</h2>
                        <ul>
            """
            for filename in os.listdir(DIRECTORY):
                if filename != '.shared_text.json':
                    ext = os.path.splitext(filename)[1].lower()
                    icon = "📄"
                    if ext in ['.pdf']:
                        icon = "📕"
                    elif ext in ['.jpg', '.jpeg', '.png', '.gif']:
                        icon = "🖼️"
                    elif ext in ['.doc', '.docx']:
                        icon = "📝"
                    elif ext in ['.xls', '.xlsx']:
                        icon = "📊"
                    elif ext in ['.zip', '.rar']:
                        icon = "🗜️"
                    
                    html += f"""
                                <li>
                                    <span class="file-icon">{icon}</span>
                                    <a href="/{filename}">{filename}</a>
                                    <span class="file-size">{os.path.getsize(os.path.join(DIRECTORY, filename))} bytes</span>
                                    <a href="/{filename}" download class="download-button">⚡Download</a>
                                </li>
                    """
            html += """
                        </ul>
                    </div>
                </div>
                
                <script>
                    // File upload handling
                    const fileInput = document.getElementById('fileInput');
                    const uploadButton = document.getElementById('uploadButton');
                    const progressContainer = document.getElementById('progressContainer');
                    const progressBar = document.getElementById('progressBar');
                    const progressText = document.getElementById('progressText');
                    const uploadMessage = document.getElementById('uploadMessage');
                    const errorMessage = document.getElementById('errorMessage');
                    const fileNameDisplay = document.getElementById('fileName');
                    
                    fileInput.addEventListener('change', () => {
                        fileNameDisplay.textContent = fileInput.files.length ? fileInput.files[0].name : 'No file selected';
                        uploadButton.disabled = !fileInput.files.length;
                    });
                    
                    document.getElementById('uploadForm').addEventListener('submit', async (e) => {
                        e.preventDefault();
                        if (!fileInput.files.length) return;
                        
                        const file = fileInput.files[0];
                        const formData = new FormData();
                        formData.append('file', file);
                        
                        uploadMessage.style.display = 'none';
                        errorMessage.style.display = 'none';
                        progressContainer.style.display = 'block';
                        uploadButton.disabled = true;
                        
                        try {
                            const xhr = new XMLHttpRequest();
                            xhr.open('POST', '/', true);
                            
                            xhr.upload.onprogress = (event) => {
                                if (event.lengthComputable) {
                                    const percent = Math.round((event.loaded / event.total) * 100);
                                    progressBar.style.width = percent + '%';
                                    progressText.textContent = `Uploading: ${percent}%`;
                                }
                            };
                            
                            xhr.onload = () => {
                                if (xhr.status === 200) {
                                    uploadMessage.style.display = 'block';
                                    progressContainer.style.display = 'none';
                                    fileInput.value = '';
                                    fileNameDisplay.textContent = 'No file selected';
                                    setTimeout(() => location.reload(), 1000);
                                } else {
                                    errorMessage.querySelector('span').textContent = `Upload failed: ${xhr.statusText}`;
                                    errorMessage.style.display = 'block';
                                    progressContainer.style.display = 'none';
                                }
                                uploadButton.disabled = false;
                            };
                            
                            xhr.onerror = () => {
                                errorMessage.querySelector('span').textContent = 'Upload failed: Network error';
                                errorMessage.style.display = 'block';
                                progressContainer.style.display = 'none';
                                uploadButton.disabled = false;
                            };
                            
                            xhr.send(formData);
                        } catch (error) {
                            errorMessage.querySelector('span').textContent = `Upload failed: ${error.message}`;
                            errorMessage.style.display = 'block';
                            progressContainer.style.display = 'none';
                            uploadButton.disabled = false;
                        }
                    });
                    
                    // Text sharing handling
                    const textInput = document.getElementById('textInput');
                    const textButton = document.getElementById('textButton');
                    const textMessage = document.getElementById('textMessage');
                    const textErrorMessage = document.getElementById('textErrorMessage');
                    const clearHistoryButton = document.getElementById('clearHistoryButton');
                    const copyMessage = document.getElementById('copyMessage');
                    
                    document.getElementById('textForm').addEventListener('submit', async (e) => {
                        e.preventDefault();
                        if (!textInput.value.trim()) return;
                        
                        textMessage.style.display = 'none';
                        textErrorMessage.style.display = 'none';
                        copyMessage.style.display = 'none';
                        textButton.disabled = true;
                        
                        try {
                            const response = await fetch('/text', {
                                method: 'POST',
                                headers: {
                                    'Content-Type': 'application/json'
                                },
                                body: JSON.stringify({ text: textInput.value })
                            });
                            
                            if (response.ok) {
                                textMessage.style.display = 'block';
                                textInput.value = '';
                                setTimeout(() => location.reload(), 1000);
                            } else {
                                textErrorMessage.querySelector('span').textContent = 'Failed to share text';
                                textErrorMessage.style.display = 'block';
                            }
                        } catch (error) {
                            textErrorMessage.querySelector('span').textContent = error.message;
                            textErrorMessage.style.display = 'block';
                        }
                        textButton.disabled = false;
                    });
                    
                    clearHistoryButton.addEventListener('click', async () => {
                        try {
                            const response = await fetch('/text', {
                                method: 'DELETE'
                            });
                            if (response.ok) {
                                textMessage.style.display = 'block';
                                textMessage.textContent = '✅ Pika! Text history cleared!';
                                setTimeout(() => location.reload(), 1000);
                            } else {
                                textErrorMessage.querySelector('span').textContent = 'Failed to clear history';
                                textErrorMessage.style.display = 'block';
                            }
                        } catch (error) {
                            textErrorMessage.querySelector('span').textContent = error.message;
                            textErrorMessage.style.display = 'block';
                        }
                    });
                    
                    // Copy text functionality
                    document.querySelectorAll('.copy-button').forEach(button => {
                        button.addEventListener('click', () => {
                            const text = button.getAttribute('data-text');
                            try {
                                const textarea = document.createElement('textarea');
                                textarea.value = text;
                                textarea.style.position = 'fixed';
                                textarea.style.opacity = '0';
                                document.body.appendChild(textarea);
                                textarea.select();
                                document.execCommand('copy');
                                document.body.removeChild(textarea);
                                copyMessage.style.display = 'block';
                                setTimeout(() => {
                                    copyMessage.style.display = 'none';
                                }, 2000);
                            } catch (error) {
                                textErrorMessage.querySelector('span').textContent = 'Failed to copy text: ' + error.message;
                                textErrorMessage.style.display = 'block';
                                setTimeout(() => {
                                    textErrorMessage.style.display = 'none';
                                }, 2000);
                            }
                        });
                    });
                </script>
            </body>
            </html>
            """
            
            self.wfile.write(html.encode())
        else:
            super().do_GET()
    
    def do_POST(self):
        if self.path == '/text':
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length == 0:
                self.send_error(400, "No text provided")
                return
                
            raw_data = self.rfile.read(content_length)
            try:
                data = json.loads(raw_data.decode('utf-8'))
                text = data.get('text', '').strip()
                if not text:
                    self.send_error(400, "Empty text")
                    return
                    
                # Load existing history or create new
                text_history = []
                if os.path.exists(TEXT_FILE):
                    with open(TEXT_FILE, 'r') as f:
                        try:
                            text_history = json.load(f)
                        except:
                            text_history = []
                
                # Add new entry with timestamp
                text_history.append({
                    'text': text,
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                })
                
                # Save updated history
                with open(TEXT_FILE, 'w') as f:
                    json.dump(text_history, f)
                
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(b'{"status": "success"}')
            except Exception as e:
                self.send_error(500, f"Error processing text: {str(e)}")
        else:
            # File upload handling
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length == 0:
                self.send_error(400, "No file was uploaded")
                return

            raw_data = self.rfile.read(content_length)
            
            try:
                parts = raw_data.split(BOUNDARY)
                for part in parts:
                    if b'filename="' in part:
                        filename_start = part.find(b'filename="') + len(b'filename="')
                        filename_end = part.find(b'"', filename_start)
                        filename = part[filename_start:filename_end].decode('utf-8')
                        filename = os.path.basename(unquote(filename))
                        
                        content_start = part.find(b'\r\n\r\n') + 4
                        content_end = part.rfind(b'\r\n--')
                        file_content = part[content_start:content_end]
                        
                        if filename and file_content:
                            file_path = os.path.join(DIRECTORY, filename)
                            with open(file_path, 'wb') as f:
                                f.write(file_content)
                            
                            self.send_response(200)
                            self.send_header("Content-type", "text/html")
                            self.end_headers()
                            self.wfile.write(b"File uploaded successfully!")
                            return
                self.send_error(400, "No file was uploaded")
            except Exception as e:
                self.send_error(500, f"Error processing upload: {str(e)}")
    
    def do_DELETE(self):
        if self.path == '/text':
            try:
                if os.path.exists(TEXT_FILE):
                    os.remove(TEXT_FILE)
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(b'{"status": "success"}')
            except Exception as e:
                self.send_error(500, f"Error clearing text history: {str(e)}")
        else:
            self.send_error(404, "Not found")

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def main():
    with socketserver.TCPServer(("", PORT), FileSharingHandler) as httpd:
        print(f"Server running at http://{get_local_ip()}:{PORT}")
        print(f"Sharing files from: {os.path.abspath(DIRECTORY)}")
        print("Press Ctrl+C to stop the server")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped")
            httpd.server_close()

if __name__ == "__main__":
    main()
