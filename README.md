# ⚡ Pikachu FileSync

![Pikachu FileSync Banner](https://img.shields.io/badge/Pikachu%20FileSync-Pika%20Power!-yellow?style=for-the-badge&logo=python)

**Pikachu FileSync** is a lightning-fast, Pokémon-inspired file-sharing server built with Python. Share files from your computer or phone to any device on the same network with a sleek, Japanese-themed UI. Pika-pika! ⚡

## 🌟 Features

- **⚡ Cross-Device Sharing**: Share files from your phone or computer to any device on the same Wi-Fi network.
- **📂 Beautiful Interface**: Japanese-inspired, mobile-friendly HTML UI with a Pokémon twist.
- **⬆ Easy Uploads**: Drag-and-drop or tap-to-upload files with real-time progress tracking.
- **📄 File Previews**: Displays file icons based on type (PDF, images, docs, etc.).
- **💾 Download Support**: One-click downloads with a Pokémon-powered button.
- **🌐 Local Network Access**: Automatically detects and shares your local IP address.
- **💻 Standalone EXE**: Download a pre-built executable for Windows, no Python required!
- **🔒 Safe & Simple**: No external dependencies beyond Python's standard library for the source version.

## 🚀 Getting Started

### Prerequisites
- **For Source Version**: Python 3.6+ (on the host computer).
- **For EXE Version**: Windows OS (no Python needed).
- Devices (phone, tablet, or computer) on the same Wi-Fi network.
- A love for Pokémon! ⚡

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/husnain002/pikachu-filesync.git
   cd pikachu-filesync
   ```

2. Run the server on your computer:
   ```bash
   python filesync.py
   ```
#### Option 2: Use the EXE (Windows Only)
1. Visit the [Releases](https://github.com/husnain002/pikachu-filesync/releases) page.
2. Download the latest `filesync.exe` from the downloads section.
3. Double-click the EXE to start the server (no Python installation needed).
4. Allow firewall access if prompted to enable network sharing.

3. Note the server address (e.g., `http://192.168.1.100:8080`) displayed in the terminal.

### Usage
- **From a Phone**:
  1. Ensure your phone is on the same Wi-Fi network as the computer running the server.
  2. Open a browser (e.g., Chrome, Safari) on your phone.
  3. Enter the server address (e.g., `http://192.168.1.100:8080`).
  4. Tap "Browse" to select a file from your phone, then tap "Upload" to share it.
  5. Download files by tapping the "⚡ Download" button next to any listed file.

- **From a Computer**:
  1. Open a browser and visit the server address.
  2. Drag-and-drop or select files to upload.
  3. Download files with the "⚡ Download" button.

- **Stop the Server**: Press `Ctrl+C` in the terminal to shut down.

## 🎨 Screenshots


![Pikachu FileSync UI](https://github.com/user-attachments/assets/0b417763-732b-42f6-a850-0d624fe4daed) 
### Mobile UI
![Pikachu FileSync UI_Mobile](https://github.com/user-attachments/assets/d9ea17a4-ee4d-40b1-8584-f2fd4f6720a3)

*Share files from your phone with Pokémon flair!*

## 🛠️ How It Works
Pikachu FileSync uses Python's `http.server` and `socketserver` to create a local web server. The custom `FileSharingHandler` class handles:
- **GET Requests**: Serves a mobile-responsive HTML page or files.
- **POST Requests**: Processes file uploads from phones or computers.
- **Local IP Detection**: Automatically finds your machine's IP for easy access from any device.

The UI is optimized for mobile devices, with touch-friendly buttons and a responsive layout, ensuring a seamless experience for phone users.
The EXE version is a self-contained executable (bundled with PyInstaller) that runs the same server without Python. The UI is mobile-optimized with touch-friendly buttons and a responsive layout.

## 📱 EXE and Mobile Sharing Tips
- **EXE Usage**: The EXE is for Windows users who want a quick setup. Download it from the [Releases](https://github.com/husnain002/pikachu-filesync/releases) page.
- **Mobile Access**: Ensure your phone and the server computer are on the same Wi-Fi network.
- **Firewall**: The EXE may prompt for firewall access to allow network traffic on port `8080`.
- **Large Files**: Modern mobile browsers (Chrome, Safari) handle uploads well, but older browsers may have limitations.

## 📚 Contributing
Want to add more Pokémon power? Contributions are welcome! Here's how to get started:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/pika-mobile`).
3. Make your changes and commit (`git commit -m "Added mobile upload enhancements"`).
4. Push to the branch (`git push origin feature/pika-mobile`).
5. Open a Pull Request.

Please follow the [Code of Conduct](CODE_OF_CONDUCT.md) and check the [Issues](https://github.com/husnain002/pikachu-filesync/issues) for ideas.

## ⚠️ Notes
- The server runs on port `8080` by default. Change the `PORT` variable in `filesync.py` if needed.
- Files are stored in the current working directory. Ensure you have write permissions.
- This is designed for local network use. Do not expose to the public internet without proper security measures.
- Some older phone browsers may have limitations with large file uploads.
- The EXE is Windows-only; use the Python version for other OSes.

## 📜 License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 🙌 Acknowledgments
- Inspired by Pikachu and the Pokémon universe! ⚡
- Built with Python’s standard library and PyInstaller for the EXE.
- Thanks to the open-source community for endless inspiration.

---

**Pika-pika!** Share files from your phone or computer with the speed of a Thunderbolt! 🌩️  
Star this repo if you love Pokémon and cross-device file sharing! ⭐
