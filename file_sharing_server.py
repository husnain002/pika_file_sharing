import http.server
import socketserver
import os
import socket
from urllib.parse import unquote

# Configuration
PORT = 8080
DIRECTORY = os.getcwd()  # Use the current working directory
BOUNDARY = b"----WebKitFormBoundary"  # Common boundary for multipart forms

class FileSharingHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            
            # Generate HTML page with Japanese-inspired CSS
            html = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title> ⚡ Pikachu FileSync</title>
                <style>
                    body {{
                        font-family: 'Helvetica Neue', Arial, sans-serif;
                        background-color: #f8f1e9;
                        margin: 0;
                        padding: 20px;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        min-height: 100vh;
                        color: #2c3e50;
                    }}
                    .container {{
                        max-width: 900px;
                        width: 100%;
                    }}
                    .header {{
                        text-align: center;
                        margin-bottom: 2rem;
                        padding: 1rem;
                        background: linear-gradient(180deg, #d4a5a5, #f8f1e9);
                        border-radius: 8px;
                    }}
                    .header h1 {{
                        font-size: 2.5rem;
                        margin: 0;
                        color: #2c3e50;
                        font-weight: 300;
                        letter-spacing: 2px;
                    }}
                    .header p {{
                        color: #5c6b73;
                        font-size: 1rem;
                        margin-top: 0.5rem;
                    }}
                    .card {{
                        background-color: #ffffff;
                        border-radius: 12px;
                        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
                        padding: 2rem;
                        margin-bottom: 2rem;
                        border: 1px solid #e2d9c8;
                    }}
                    .card h2 {{
                        font-size: 1.5rem;
                        color: #2c3e50;
                        margin-bottom: 1.5rem;
                        font-weight: 400;
                    }}
                    .file-input-container {{
                        position: relative;
                        display: flex;
                        align-items: center;
                        gap: 1rem;
                    }}
                    .file-input {{
                        display: none;
                    }}
                    .browse-button {{
                        padding: 0.75rem 1.5rem;
                        background-color: #6b7280;
                        color: #ffffff;
                        border-radius: 8px;
                        cursor: pointer;
                        transition: background-color 0.3s ease;
                        font-size: 1rem;
                    }}
                    .browse-button:hover {{
                        background-color: #4b5563;
                    }}
                    .file-name {{
                        flex: 1;
                        padding: 0.75rem;
                        border: 1px solid #e2d9c8;
                        border-radius: 8px;
                        background-color: #f8fafc;
                        color: #2c3e50;
                        font-size: 0.9rem;
                    }}
                    .upload-button {{
                        width: 100%;
                        padding: 0.75rem;
                        background-color: #2a9d8f;
                        color: #ffffff;
                        border: none;
                        border-radius: 8px;
                        cursor: pointer;
                        font-size: 1rem;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        transition: background-color 0.3s ease;
                    }}
                    .upload-button:disabled {{
                        background-color: #a0aec0;
                        cursor: not-allowed;
                    }}
                    .upload-button:hover:not(:disabled) {{
                        background-color: #21867a;
                    }}
                    .progress-container {{
                        display: none;
                        margin-top: 1rem;
                    }}
                    .progress-bar {{
                        width: 100%;
                        background-color: #e2e8f0;
                        border-radius: 8px;
                        height: 0.5rem;
                        overflow: hidden;
                    }}
                    .progress-fill {{
                        height: 100%;
                        background-color: #2a9d8f;
                        width: 0%;
                        transition: width 0.3s ease;
                    }}
                    .progress-text {{
                        font-size: 0.875rem;
                        color: #5c6b73;
                        margin-top: 0.5rem;
                    }}
                    .message {{
                        display: none;
                        margin-top: 0.5rem;
                        font-size: 0.875rem;
                    }}
                    .success {{
                        color: #2a9d8f;
                    }}
                    .error {{
                        color: #e63946;
                    }}
                    .file-list ul {{
                        list-style: none;
                        padding: 0;
                        margin: 0;
                    }}
                    .file-list li {{
                        display: flex;
                        align-items: center;
                        justify-content: space-between;
                        padding: 0.75rem;
                        border-bottom: 1px solid #e2d9c8;
                        transition: background-color 0.2s;
                    }}
                    .file-list li:last-child {{
                        border-bottom: none;
                    }}
                    .file-list li:hover {{
                        background-color: #f1e9db;
                    }}
                    .file-list a {{
                        color: #2a9d8f;
                        text-decoration: none;
                        flex: 1;
                    }}
                    .file-list a:hover {{
                        text-decoration: underline;
                    }}
                    .file-icon {{
                        margin-right: 0.75rem;
                        font-size: 1.25rem;
                    }}
                    .file-size {{
                        color: #5c6b73;
                        font-size: 0.875rem;
                        margin-right: 1rem;
                    }}
                    .download-button {{
                        padding: 0.5rem 1rem;
                        background-color: #264653;
                        color: #ffffff;
                        border-radius: 6px;
                        text-decoration: none;
                        font-size: 0.875rem;
                        transition: background-color 0.3s ease;
                    }}
                    .download-button:hover {{
                        background-color: #1d3c48;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>⚡Pikachu FileSync</h1>
                        <p>Pika-pika! Share files with Pokémon power!</p>
                    </div>
                    
                    <div class="card">
                        <h2>⚡ Upload File</h2>
                        <form id="uploadForm" enctype="multipart/form-data" method="post">
                            <div class="file-input-container">
                                <label for="fileInput" class="browse-button">📂 Browse</label>
                                <input type="file" name="file" id="fileInput" class="file-input"/>
                                <span id="fileName" class="file-name">No file selected</span>
                            </div><br>
                            <button type="submit" id="uploadButton" class="upload-button" disabled>⬆ Upload File</button>
                        </form>
                        <div id="progressContainer" class="progress-container">
                            <div class="progress-bar">
                                <div id="progressBar" class="progress-fill"></div>
                            </div>
                            <div id="progressText" class="progress-text">Uploading: 0%</div>
                        </div>
                        <div id="uploadMessage" class="message success">✅ Pika! File uploaded!</div>
                        <div id="errorMessage" class="message error">❌ Pika... Upload failed:<span></span></div>
                    </div>
                    
                    <div class="card file-list">
                        <h2>📂 Available Files</h2>
                        <ul>
            """
            
            # List all files in the directory with Unicode icons and download buttons
            for filename in os.listdir(DIRECTORY):
                # Determine file icon based on extension
                ext = os.path.splitext(filename)[1].lower()
                icon = "📄"  # Default file icon
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
                    const fileInput = document.getElementById('fileInput');
                    const uploadButton = document.getElementById('uploadButton');
                    const progressContainer = document.getElementById('progressContainer');
                    const progressBar = document.getElementById('progressBar');
                    const progressText = document.getElementById('progressText');
                    const uploadMessage = document.getElementById('uploadMessage');
                    const errorMessage = document.getElementById('errorMessage');
                    const fileNameDisplay = document.getElementById('fileName');
                    
                    // Update file name display and enable upload button
                    fileInput.addEventListener('change', () => {
                        fileNameDisplay.textContent = fileInput.files.length ? fileInput.files[0].name : 'No file selected';
                        uploadButton.disabled = !fileInput.files.length;
                    });
                    
                    // Handle form submission
                    document.getElementById('uploadForm').addEventListener('submit', async (e) => {
                        e.preventDefault();
                        if (!fileInput.files.length) return;
                        
                        const file = fileInput.files[0];
                        const formData = new FormData();
                        formData.append('file', file);
                        
                        // Reset UI
                        uploadMessage.style.display = 'none';
                        errorMessage.style.display = 'none';
                        progressContainer.style.display = 'block';
                        uploadButton.disabled = true;
                        
                        try {
                            const xhr = new XMLHttpRequest();
                            xhr.open('POST', '/', true);
                            
                            // Update progress
                            xhr.upload.onprogress = (event) => {
                                if (event.lengthComputable) {
                                    const percent = Math.round((event.loaded / event.total) * 100);
                                    progressBar.style.width = percent + '%';
                                    progressText.textContent = `Uploading: ${percent}%`;
                                }
                            };
                            
                            // Handle completion
                            xhr.onload = () => {
                                if (xhr.status === 200) {
                                    uploadMessage.style.display = 'block';
                                    progressContainer.style.display = 'none';
                                    fileInput.value = ''; // Reset file input
                                    fileNameDisplay.textContent = 'No file selected';
                                    // Reload file list after a short delay
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
                </script>
            </body>
            </html>
            """
            
            self.wfile.write(html.encode())
        else:
            # Serve the requested file
            super().do_GET()
    
    def do_POST(self):
        # Get content length
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length == 0:
            self.send_error(400, "No file was uploaded")
            return

        # Read the raw POST data
        raw_data = self.rfile.read(content_length)
        
        # Find the file content in the multipart form data
        try:
            # Split by boundary
            parts = raw_data.split(BOUNDARY)
            for part in parts:
                if b'filename="' in part:
                    # Extract filename
                    filename_start = part.find(b'filename="') + len(b'filename="')
                    filename_end = part.find(b'"', filename_start)
                    filename = part[filename_start:filename_end].decode('utf-8')
                    filename = os.path.basename(unquote(filename))
                    
                    # Extract file content
                    content_start = part.find(b'\r\n\r\n') + 4
                    content_end = part.rfind(b'\r\n--')
                    file_content = part[content_start:content_end]
                    
                    # Save the file
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

def get_local_ip():
    # Get the local IP address
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Doesn't need to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def main():
    # Set up and start the server
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