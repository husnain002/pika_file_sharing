# ⚡ Pikachu FileSync

![Pikachu FileSync Banner](https://img.shields.io/badge/Pikachu%20FileSync%202.0-Pika%20Power!-yellow?style=for-the-badge&logo=python)

**Pikachu FileSync** is a lightning-fast, Pokémon-inspired file and text-sharing server built with Python. Share files and text snippets from your computer or phone to any device on the same network with a vibrant, Japanese-themed UI. Version 2.0 introduces text sharing with history, powered up by Pikachu’s Thunderbolt! Pika-pika! ⚡

## 🌟 Features

### Pikachu FileSync 2.0 (Latest)
- **📋 Text Sharing**: Share text snippets instantly and view the last 5 entries in a history log.
- **🗑️ Text History Management**: Clear text history with a single click.
- **⚡ Cross-Device Sharing**: Share files and text from phones, tablets, or computers on the same Wi-Fi network.
- **📂 Responsive Interface**: Mobile-optimized, Japanese-inspired UI with Pokémon flair.
- **⬆ Easy Uploads**: Drag-and-drop or tap-to-upload files with real-time progress tracking.
- **📄 File Previews**: Displays file icons based on type (PDF, images, docs, etc.).
- **💾 Download Support**: One-click file downloads with a Pokémon-powered button.
- **🌐 Local Network Access**: Auto-detects your local IP for seamless access.
- **💻 Standalone EXE**: Download a pre-built executable for Windows, no Python required.
- **🔒 Safe & Simple**: Uses Python’s standard library for minimal dependencies.

### Pikachu FileSync 1.0 (Legacy)
- File sharing with the same mobile-friendly UI and cross-device support.
- Lacked text-sharing and history features introduced in 2.0.
- Available in the [Releases](https://github.com/husnain002/pikachu-filesync/releases) for reference.

## 🚀 Getting Started

### Prerequisites
- **For Source Version**: Python 3.6+ (on the host computer).
- **For EXE Version**: Windows OS (no Python needed).
- Devices (phone, tablet, or computer) on the same Wi-Fi network.
- A love for Pokémon! ⚡

### Installation
#### Option 1: Run with Python (Source Version)
1. Clone the repository:
   ```bash
   git clone https://github.com/husnain002/pikachu-filesync.git
   cd pikachu-filesync
   ```

2. Run the server:
   ```bash
   python filesync.py
   ```

#### Option 2: Use the EXE (Windows Only)
1. Visit the [Releases](https://github.com/husnain002/pikachu-filesync/releases) page.
2. Download the latest `PikachuFileSync.exe` (version 2.0 recommended).
3. Double-click the EXE to start the server (no Python installation needed).
4. Allow firewall access if prompted to enable network sharing.

3. Note the server address (e.g., `http://192.168.1.100:8080`) displayed in the terminal or EXE console.

### Usage
- **From a Phone**:
  1. Connect to the same Wi-Fi network as the server.
  2. Open a browser (e.g., Chrome, Safari) and enter the server address.
  3. **File Sharing**: Tap "Browse" to select a file, then "Upload" to share.
  4. **Text Sharing**: Paste text in the textarea and click "Share Text". Copy or view recent texts in the history.
  5. Download files by tapping the "⚡ Download" button or copy text with the "📋 Copy" button.

- **From a Computer**:
  1. Visit the server address in a browser.
  2. Drag-and-drop or select files to upload.
  3. Share text via the textarea or copy from history.
  4. Download files with the "⚡ Download" button.

- **Text History**: View the last 5 shared texts with timestamps. Clear history with the "🗑️ Clear History" button.
- **Stop the Server**: Press `Ctrl+C` in the terminal/EXE window or close the console.

## 🎨 Screenshots

### Desktop UI 2.0
![image](https://github.com/user-attachments/assets/d762445d-bd1b-464e-b08b-364812bbf148)

### Mobile UI 2.0 
![image](https://github.com/user-attachments/assets/c07342a9-68c6-4497-8b8b-5c5d5973c0c7)


*Share files and text with Pokémon-powered flair!*

## 🛠️ How It Works
Pikachu FileSync uses Python’s `http.server` and `socketserver` to create a local web server. The `FileSharingHandler` class manages:
- **GET Requests**: Serves a responsive HTML page or files.
- **POST Requests**: Handles file uploads and text sharing, storing text in a `.shared_text.json` file.
- **DELETE Requests**: Clears text history.
- **Local IP Detection**: Auto-finds the server’s IP for easy access.

Version 2.0 adds text-sharing functionality, storing entries with timestamps and displaying them in a history section. The UI is mobile-optimized with responsive design, touch-friendly buttons, and clamp-based font sizing for accessibility across devices.

## 📱 EXE and Mobile Sharing Tips
- **EXE Usage**: Download the Windows EXE from the [Releases](https://github.com/husnain002/pikachu-filesync/releases) page for quick setup without Python.
- **Mobile Access**: Ensure devices are on the same Wi-Fi network. Use modern browsers (Chrome, Safari) for best performance.
- **Firewall**: Allow port `8080` in firewall settings for network access.
- **Large Files**: Older mobile browsers may struggle with large uploads.
- **Text Sharing**: Text is stored locally in `.shared_text.json` and limited to the last 5 entries for simplicity.

## 📚 Contributing
Want to supercharge Pikachu’s powers? Contributions are welcome!
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/pika-text`).
3. Make changes and commit (`git commit -m "Enhanced text sharing feature"`).
4. Push to the branch (`git push origin feature/pika-text`).
5. Open a Pull Request.

See the [Code of Conduct](CODE_OF_CONDUCT.md) and check [Issues](https://github.com/husnain002/pikachu-filesync/issues) for ideas.

## ⚠️ Notes
- **Port**: Runs on port `8080` by default. Modify `PORT` in `filesync.py` if needed.
- **Storage**: Files and text history (`.shared_text.json`) are stored in the current directory. Ensure write permissions.
- **Security**: Designed for local networks. Avoid public internet exposure without proper security.
- **EXE**: Windows-only; use the Python version for macOS/Linux.
- **Version 1.0**: Available in older releases for file-only sharing.

## 📜 License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 🙌 Acknowledgments
- Inspired by Pikachu and the Pokémon universe! ⚡
- Built with Python’s standard library and PyInstaller for the EXE.
- Thanks to the open-source community for endless inspiration.

---

**Pika-pika!** Share files and text with the speed of a Thunderbolt! 🌩️  
Star this repo if you love Pokémon and cross-device sharing! ⭐
