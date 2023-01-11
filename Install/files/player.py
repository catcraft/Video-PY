import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtCore import QUrl, Qt, QObject

class VideoPlayer(QMainWindow):
    def __init__(self, display_monitor, file_name):
        super().__init__()
        
        # Set up the media player and video widget
        self.media_player = QMediaPlayer(self)
        self.video_widget = QVideoWidget(self)
        self.media_player.setVideoOutput(self.video_widget)

        # Set the window size and layout
        self.setCentralWidget(self.video_widget)
        self.resize(640, 480)

        # Load the specified video file
        self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(file_name)))

        # Connect the positionChanged signal to the check_position slot
        self.media_player.positionChanged.connect(self.check_position)

        self.media_player.play()

        # Set the window to be borderless
        self.setWindowFlag(Qt.FramelessWindowHint)


    def check_position(self, position):
        # Check if the position is at the end of the video
        if position == self.media_player.duration():
            # If it is, seek back to the beginning and start playing again
            self.media_player.setPosition(0)
            self.media_player.play()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    display_monitor = int(sys.argv[1])
    file_name = sys.argv[2]
    player = VideoPlayer(display_monitor, file_name)
    
    monitor = QDesktopWidget().screenGeometry(display_monitor)
    player.move(monitor.left(), monitor.top())
    player.showMaximized()
    sys.exit(app.exec_())
