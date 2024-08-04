import sys
import os
import json
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QFileDialog, QVBoxLayout, QHBoxLayout, 
                             QSlider, QLabel, QComboBox, QMainWindow, QAction, QStyle, QMessageBox, QSizePolicy)
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import Qt, QUrl, QTime, QTimer
from PyQt5.QtGui import QKeyEvent, QIcon

class VideoPlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Media Player")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.init_ui()
        self.create_menu()

        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.media_player.setVideoOutput(self.video_widget)
        self.media_player.stateChanged.connect(self.media_state_changed)
        self.media_player.positionChanged.connect(self.position_changed)
        self.media_player.durationChanged.connect(self.duration_changed)

        self.last_positions = self.load_positions()
        self.current_file = ""
        self.is_audio = False
        self.is_closing = False
        self.show_remaining_time = False


        main_layout = QVBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Video display area
        self.video_widget = QVideoWidget()
        main_layout.addWidget(self.video_widget)

        # Control layout (all controls in one line)
        control_layout = QHBoxLayout()
        control_layout.setContentsMargins(5, 0, 5, 0)
        control_layout.setSpacing(5)

        button_style = """
            QPushButton {
                min-width: 25px;
                max-width: 25px;
                min-height: 25px;
                max-height: 25px;
                padding: 0px;
                font-size: 10px;
            }
        """

        self.backward_button = QPushButton('<<')
        self.backward_button.clicked.connect(self.backward)
        self.backward_button.setStyleSheet(button_style)

        self.play_button = QPushButton('Play')
        self.play_button.clicked.connect(self.play_pause_video)
        self.play_button.setStyleSheet(button_style)

        self.forward_button = QPushButton('>>')
        self.forward_button.clicked.connect(self.forward)
        self.forward_button.setStyleSheet(button_style)

        self.stop_button = QPushButton('Stop')
        self.stop_button.clicked.connect(self.stop_video)
        self.stop_button.setStyleSheet(button_style)

        control_layout.addWidget(self.backward_button)
        control_layout.addWidget(self.play_button)
        control_layout.addWidget(self.forward_button)
        control_layout.addWidget(self.stop_button)

        # Progress slider
        self.progress_slider = QSlider(Qt.Horizontal)
        self.progress_slider.setFixedHeight(15)
        self.progress_slider.sliderMoved.connect(self.set_position)
        control_layout.addWidget(self.progress_slider, 1)  # Give it more space in the layout

        # Time labels
        #self.current_time_label = QLabel("00:00:00")
        #self.current_time_label.setFixedWidth(50)
        self.total_time_label = QLabel("00:00:00")
        self.total_time_label.setFixedWidth(50)
        self.total_time_label.mousePressEvent = self.toggle_time_display
        #control_layout.addWidget(self.current_time_label)
        control_layout.addWidget(self.total_time_label)


        # Volume control
        volume_label = QLabel("Volume:")
        volume_label.setFixedWidth(45)
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(50)
        self.volume_slider.setFixedWidth(60)
        self.volume_slider.setFixedHeight(15)
        self.volume_slider.valueChanged.connect(self.set_volume)
        
        self.volume_value_label = QLabel("50%")
        self.volume_value_label.setFixedWidth(30)
        
        control_layout.addWidget(volume_label)
        control_layout.addWidget(self.volume_slider)
        control_layout.addWidget(self.volume_value_label)



        # Playback speed control
        speed_label = QLabel("Speed:")
        speed_label.setFixedWidth(40)
        self.speed_combo = QComboBox()
        self.speed_combo.setFixedWidth(50)
        self.speed_combo.setFixedHeight(20)
        speeds = ["0.5x", "0.75x", "0.85x", "1.0x", "1.25x", "1.5x", "1.75x", "2.0x"]
        self.speed_combo.addItems(speeds)
        self.speed_combo.setCurrentText("1.0x")
        self.speed_combo.currentTextChanged.connect(self.set_playback_speed)
        
        control_layout.addWidget(speed_label)
        control_layout.addWidget(self.speed_combo)



        # Wrap control layout in a widget to set fixed height
        control_widget = QWidget()
        control_widget.setLayout(control_layout)
        control_widget.setFixedHeight(30)  # Set the height of the control bar

        # Add control widget to main layout
        main_layout.addWidget(control_widget)

        self.central_widget.setLayout(main_layout)

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Video display area
        self.video_widget = QVideoWidget()
        main_layout.addWidget(self.video_widget)

        # Control layout (all controls in one line)
        control_layout = QHBoxLayout()
        control_layout.setContentsMargins(5, 0, 5, 0)
        control_layout.setSpacing(5)

        button_style = """
            QPushButton {
                min-width: 30px;
                max-width: 30px;
                min-height: 25px;
                max-height: 25px;
                padding: 0px;
                font-size: 10px;
            }
        """

        self.backward_button = QPushButton('<<')
        self.backward_button.clicked.connect(self.backward)
        self.backward_button.setStyleSheet(button_style)

        self.play_button = QPushButton('Play')
        self.play_button.clicked.connect(self.play_pause_video)
        self.play_button.setStyleSheet(button_style)

        self.forward_button = QPushButton('>>')
        self.forward_button.clicked.connect(self.forward)
        self.forward_button.setStyleSheet(button_style)

        self.stop_button = QPushButton('Stop')
        self.stop_button.clicked.connect(self.stop_video)
        self.stop_button.setStyleSheet(button_style)

        control_layout.addWidget(self.backward_button)
        control_layout.addWidget(self.play_button)
        control_layout.addWidget(self.forward_button)
        control_layout.addWidget(self.stop_button)

        # Progress slider
        self.progress_slider = QSlider(Qt.Horizontal)
        self.progress_slider.setFixedHeight(15)
        self.progress_slider.setMinimumWidth(80)
        self.progress_slider.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.progress_slider.sliderMoved.connect(self.set_position)
        control_layout.addWidget(self.progress_slider, 9)  # Reduced stretch factor from 10 to 9

        # Time labels
        self.total_time_label = QLabel("00:00:00")
        self.total_time_label.setMaximumWidth(60)
        self.total_time_label.mousePressEvent = self.toggle_time_display

        control_layout.addWidget(self.total_time_label)

        # Volume control
        volume_label = QLabel("Vol:")
        volume_label.setFixedWidth(25)
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(50)
        self.volume_slider.setFixedWidth(80)
        self.volume_slider.setFixedHeight(15)
        self.volume_slider.valueChanged.connect(self.set_volume)
        
        self.volume_value_label = QLabel("50%")
        self.volume_value_label.setFixedWidth(30)
        
        control_layout.addWidget(volume_label)
        control_layout.addWidget(self.volume_slider)
        control_layout.addWidget(self.volume_value_label)

        # Playback speed control
        speed_label = QLabel("X:")
        speed_label.setFixedWidth(15)
        self.speed_combo = QComboBox()
        self.speed_combo.setFixedWidth(70)
        self.speed_combo.setFixedHeight(20)
        speeds = ["0.5x", "0.75x", "0.85x", "1.0x", "1.25x", "1.5x", "1.75x", "2.0x"]
        self.speed_combo.addItems(speeds)
        self.speed_combo.setCurrentText("1.0x")
        self.speed_combo.currentTextChanged.connect(self.set_playback_speed)
        
        control_layout.addWidget(speed_label)
        control_layout.addWidget(self.speed_combo)



        # Wrap control layout in a widget to set fixed height
        control_widget = QWidget()
        control_widget.setLayout(control_layout)
        control_widget.setFixedHeight(30)  # Set the height of the control bar

        # Add control widget to main layout
        main_layout.addWidget(control_widget)

        self.central_widget.setLayout(main_layout)

    def create_menu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')

        open_action = QAction(QIcon.fromTheme("document-open"), 'Open', self)
        open_action.setShortcut('Ctrl+O')
        open_action.setStatusTip('Open media file')
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        exit_action = QAction(QIcon.fromTheme("application-exit"), 'Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Exit application')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

    def load_positions(self):
        try:
            with open('last_positions.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_positions(self):
        with open('last_positions.json', 'w') as f:
            json.dump(self.last_positions, f)

    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Media File", "", 
            "Media Files (*.mp3 *.mp4 *.avi *.mkv *.wav *.flac *.m4a);;All Files (*)")
        if file_name:
            self.current_file = file_name
            self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(file_name)))
            self.play_button.setEnabled(True)
            
            if file_name in self.last_positions:
                position = self.last_positions[file_name]
                self.media_player.setPosition(position)
            
            self.play_pause_video()

    def play_pause_video(self):
        if self.media_player.state() == QMediaPlayer.PlayingState:
            self.media_player.pause()
        else:
            self.media_player.play()
        
        self.is_audio = self.media_player.isAudioAvailable() and not self.media_player.isVideoAvailable()
        self.video_widget.setVisible(not self.is_audio)

    def stop_video(self):
        self.media_player.stop()
        if self.current_file:
            self.last_positions[self.current_file] = self.media_player.position()
            self.save_positions()

    def backward(self):
        self.media_player.setPosition(max(0, self.media_player.position() - 5000))

    def forward(self):
        self.media_player.setPosition(min(self.media_player.duration(), self.media_player.position() + 5000))

    def closeEvent(self, event):
        if not self.is_closing:
            self.is_closing = True
            event.ignore()
            QTimer.singleShot(0, self.safe_close)
        else:
            event.accept()

    def safe_close(self):
        try:
            if self.media_player.state() == QMediaPlayer.PlayingState:
                self.media_player.stop()

            if self.current_file:
                self.last_positions[self.current_file] = self.media_player.position()
                self.save_positions()

            self.media_player.setMedia(QMediaContent())
            
            self.close()
        except Exception as e:
            print(f"Error during closing: {e}")
            self.close()

    def media_state_changed(self, state):
        if self.media_player.state() == QMediaPlayer.PlayingState:
            self.play_button.setText("Pause")
        else:
            self.play_button.setText("Play")

    def position_changed(self, position):
        self.progress_slider.setValue(position)
        self.update_current_time(position)

    def duration_changed(self, duration):
        self.progress_slider.setRange(0, duration)
        self.update_total_time(duration)

    def set_position(self, position):
        self.media_player.setPosition(position)

    def set_volume(self, volume):
        self.media_player.setVolume(volume)
        self.volume_value_label.setText(f"{volume}%")

    def update_current_time(self, position):
        
        if self.show_remaining_time:
            remaining = self.media_player.duration() - position
            remaining_time = QTime(0, 0, 0).addMSecs(remaining)
            self.total_time_label.setText("-" + remaining_time.toString("hh:mm:ss"))

    def update_total_time(self, duration):
        total_time = QTime(0, 0, 0).addMSecs(duration)
        if self.show_remaining_time:
            self.total_time_label.setText("-" + total_time.toString("hh:mm:ss"))
        else:
            self.total_time_label.setText(total_time.toString("hh:mm:ss"))

    def toggle_time_display(self, event):
        self.show_remaining_time = not self.show_remaining_time
        self.update_total_time(self.media_player.duration())
        self.update_current_time(self.media_player.position())

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Left:
            self.backward()
        elif event.key() == Qt.Key_Right:
            self.forward()
        elif event.key() == Qt.Key_Space:
            self.play_pause_video()
        elif event.key() == Qt.Key_Up:
            self.adjust_volume(5)
        elif event.key() == Qt.Key_Down:
            self.adjust_volume(-5)
        else:
            super().keyPressEvent(event)

    def set_playback_speed(self, speed_text):
        speed = float(speed_text[:-1])
        self.media_player.setPlaybackRate(speed)

    def adjust_volume(self, delta):
        current_volume = self.media_player.volume()
        new_volume = max(0, min(100, current_volume + delta))
        self.media_player.setVolume(new_volume)
        self.volume_slider.setValue(new_volume)
        self.volume_value_label.setText(f"{new_volume}%")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = VideoPlayer()
    player.show()
    sys.exit(app.exec_())