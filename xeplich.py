import sys
import os
from pathlib import Path
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QSlider, QListWidget, QLabel, QFileDialog,
    QStyle
)
from PyQt5.QtMultimedia import QMediaPlayer, QMediaPlaylist, QMediaContent
from PyQt5.QtCore import Qt, QUrl

class MP3Player(QWidget):
    def __init__(self):
        super().__init__()
        
        # Khởi tạo trình phát và danh sách phát
        self.player = QMediaPlayer()
        self.playlist = QMediaPlaylist(self.player)
        self.player.setPlaylist(self.playlist)
        
        # Gọi hàm thiết lập giao diện
        self.initUI()
        
        # Gọi hàm kết nối các tín hiệu (signal)
        self.connectSignals()
        
        # Thiết lập cửa sổ
        self.setWindowTitle('Simple MP3 Player')
        self.setGeometry(300, 300, 500, 400)

    def initUI(self):
        # Layout chính
        mainLayout = QVBoxLayout()
        
        # 1. Nút chọn thư mục
        self.btnOpenDir = QPushButton('Chọn Thư Mục...')
        mainLayout.addWidget(self.btnOpenDir)
        
        # 2. Danh sách file nhạc
        self.listWidget = QListWidget()
        mainLayout.addWidget(self.listWidget)
        
        # 3. Thông tin bài hát đang phát
        self.lblCurrentSong = QLabel('Chưa có bài hát nào.')
        self.lblCurrentSong.setAlignment(Qt.AlignCenter)
        mainLayout.addWidget(self.lblCurrentSong)
        
        # 4. Các nút điều khiển
        controlLayout = QHBoxLayout()
        
        self.btnPrev = QPushButton()
        self.btnPrev.setIcon(self.style().standardIcon(QStyle.SP_MediaSkipBackward))
        
        self.btnPlay = QPushButton()
        self.btnPlay.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        
        self.btnPause = QPushButton()
        self.btnPause.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        
        self.btnStop = QPushButton()
        self.btnStop.setIcon(self.style().standardIcon(QStyle.SP_MediaStop))
        
        self.btnNext = QPushButton()
        self.btnNext.setIcon(self.style().standardIcon(QStyle.SP_MediaSkipForward))
        
        controlLayout.addWidget(self.btnPrev)
        controlLayout.addWidget(self.btnPlay)
        controlLayout.addWidget(self.btnPause)
        controlLayout.addWidget(self.btnStop)
        controlLayout.addWidget(self.btnNext)
        
        mainLayout.addLayout(controlLayout)
        
        # 5. Thanh trượt Âm lượng
        volumeLayout = QHBoxLayout()
        self.lblVolume = QLabel('Âm lượng (70):')
        self.sliderVolume = QSlider(Qt.Horizontal)
        self.sliderVolume.setRange(0, 100)
        self.sliderVolume.setValue(70)
        self.player.setVolume(70) # Đặt âm lượng mặc định
        
        volumeLayout.addWidget(self.lblVolume)
        volumeLayout.addWidget(self.sliderVolume)
        mainLayout.addLayout(volumeLayout)
        
        # 6. Thanh trượt Tốc độ
        speedLayout = QHBoxLayout()
        self.lblSpeed = QLabel('Tốc độ (1.0x):')
        self.sliderSpeed = QSlider(Qt.Horizontal)
        # Đặt phạm vi 50-200, tương ứng 0.5x đến 2.0x
        self.sliderSpeed.setRange(50, 200) 
        self.sliderSpeed.setValue(100) # Mặc định là 100 (1.0x)
        
        speedLayout.addWidget(self.lblSpeed)
        speedLayout.addWidget(self.sliderSpeed)
        mainLayout.addLayout(speedLayout)
        
        # Đặt layout chính cho cửa sổ
        self.setLayout(mainLayout)

    def connectSignals(self):
        # Nút
        self.btnOpenDir.clicked.connect(self.openDirectory)
        self.btnPlay.clicked.connect(self.player.play)
        self.btnPause.clicked.connect(self.player.pause)
        self.btnStop.clicked.connect(self.player.stop)
        self.btnNext.clicked.connect(self.playlist.next)
        self.btnPrev.clicked.connect(self.playlist.previous)
        
        # Thanh trượt
        self.sliderVolume.valueChanged.connect(self.setVolume)
        self.sliderSpeed.valueChanged.connect(self.setSpeed)
        
        # Danh sách
        self.listWidget.itemDoubleClicked.connect(self.playFromList)
        
        # Trình phát
        self.playlist.currentIndexChanged.connect(self.updateCurrentSong)
        self.player.currentMediaChanged.connect(self.updateSongInfoLabel)

    def openDirectory(self):
        # Mở hộp thoại chọn thư mục
        directory = QFileDialog.getExistingDirectory(self, "Chọn thư mục chứa file MP3")
        
        if directory:
            # Xóa danh sách phát cũ
            self.playlist.clear()
            self.listWidget.clear()
            
            # Quét các file .mp3 trong thư mục
            folder = Path(directory)
            mp3_files = list(folder.glob('*.mp3'))
            
            if not mp3_files:
                self.lblCurrentSong.setText("Không tìm thấy file MP3 nào.")
                return

            # Thêm các file tìm thấy vào danh sách phát
            for mp3_file in mp3_files:
                url = QUrl.fromLocalFile(str(mp3_file))
                self.playlist.addMedia(QMediaContent(url))
                self.listWidget.addItem(mp3_file.name)
            
            # **Quan trọng: Đặt chế độ lặp lại tất cả (Loop)**
            self.playlist.setPlaybackMode(QMediaPlaylist.Loop)
            
            # Đặt bài hát đầu tiên và bắt đầu phát
            self.playlist.setCurrentIndex(0)
            self.player.play()

    def setVolume(self, value):
        self.player.setVolume(value)
        self.lblVolume.setText(f'Âm lượng ({value}):')

    def setSpeed(self, value):
        # Chuyển đổi giá trị 50-200 thành 0.5-2.0
        rate = value / 100.0
        self.player.setPlaybackRate(rate)
        self.lblSpeed.setText(f'Tốc độ ({rate:.1f}x):')

    def playFromList(self, item):
        # Khi double-click vào một bài hát trong danh sách
        index = self.listWidget.row(item)
        self.playlist.setCurrentIndex(index)
        self.player.play()

    def updateCurrentSong(self, index):
        # Cập nhật lựa chọn trong QListWidget khi bài hát thay đổi
        if index >= 0:
            self.listWidget.setCurrentRow(index)

    def updateSongInfoLabel(self, media):
        # Cập nhật tên bài hát đang phát
        if media.isNull():
            self.lblCurrentSong.setText("...")
        else:
            url = media.canonicalUrl()
            fileName = Path(url.toLocalFile()).name
            self.lblCurrentSong.setText(f"Đang phát: {fileName}")


# Khối thực thi chính
if __name__ == '__main__':
    app = QApplication(sys.argv)
    player_app = MP3Player()
    player_app.show()
    sys.exit(app.exec_())