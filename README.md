
# Play All 

A simple, feature-rich media player built with Python and PyQt5.

## Features

- Play, pause, and stop videos or audios
- Seek through video using a progress slider
- Display current and total playback time
- Adjust volume
- Control playback speed (0.5x to 2.0x)
- Remember last playback position for each video
- Keyboard shortcuts for easy control

## Requirements

python3 -m venv playall  
source playall/bin/activate
pip install -r requirements.txt


- Python 3.6+
- PyQt5
- PyQt5-multimediawidgets

## Installation

1. Ensure you have Python 3.6+ installed on your system.
2. Clone this repository:
   git clone https://github.com/ErikZhou/PlayAll.git
3. Navigate to the project directory:
   cd mp4player
4. Install the required dependencies:
   pip install PyQt5 PyQt5-multimediawidgets
## Usage

To run the Play All:

1. Navigate to the project directory in your terminal.
2. Run the following command:
   python mp4player.py
### Opening a Video

- Click on "File" in the menu bar and select "Open", or use the keyboard shortcut Ctrl+O (Cmd+O on macOS).
- Select an MP4 file from your file system.
- If you've played this video before, you'll be asked if you want to resume from where you left off.

### Playback Controls

- Play/Pause: Click the "Play" button or press the Spacebar.
- Stop: Click the "Stop" button.
- Seek Forward: Click the ">>" button or press the Right Arrow key.
- Seek Backward: Click the "<<" button or press the Left Arrow key.
- Adjust Volume: Use the volume slider.
- Change Playback Speed: Select a speed from the dropdown menu (0.5x to 2.0x).

### Progress Control

- Click or drag the progress slider to jump to a specific point in the video.

### Keyboard Shortcuts

- Spacebar: Play/Pause
- Left Arrow: Seek backward
- Right Arrow: Seek forward
- Ctrl+O (Cmd+O on macOS): Open file
- Ctrl+Q (Cmd+Q on macOS): Quit application

## Exiting the Application

- Click on "File" in the menu bar and select "Exit", use the keyboard shortcut Ctrl+Q (Cmd+Q on macOS), or simply close the window.
- The current playback position will be saved automatically.

## Troubleshooting

If you encounter any issues:
- Ensure you have the latest versions of PyQt5 and PyQt5-multimediawidgets installed.
- Check that your MP4 file is not corrupted and is fully supported by the player.
- If the application crashes, try running it from the command line to see any error messages.
- Make sure you have the necessary codecs installed on your system for playing MP4 files.

## Known Limitations

- The player currently supports MP4 files only. Other video formats may not work correctly.
- Some features may not be available on all operating systems due to limitations in the PyQt5 multimedia framework.

## Contributing

Contributions are welcome! If you'd like to contribute to this project, please follow these steps:

1. Fork the repository
2. Create a new branch for your feature (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Please ensure your code adheres to the existing style to maintain consistency.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- PyQt5 for providing the GUI framework
- All contributors who have helped to improve this project

## Contact

Erik Zhou - 

Project Link: [https://github.com/ErikZhou/PlayAll](https://github.com/ErikZhou/PlayAll)
