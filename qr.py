import sys
import os
import time
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QTextEdit, QComboBox, QTabWidget, QFormLayout, 
                             QSpinBox, QColorDialog, QFileDialog, QMessageBox, 
                             QGroupBox, QCheckBox, QSlider, QAction, QStatusBar,
                             QDateEdit, QTimeEdit, QListWidget, QProgressBar)
from PyQt5.QtCore import Qt, QDate, QTime, QUrl
from PyQt5.QtGui import QPixmap, QImage, QColor, QDesktopServices, QDragEnterEvent, QDropEvent
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import (
    SquareModuleDrawer, GappedSquareModuleDrawer, CircleModuleDrawer, 
    RoundedModuleDrawer, VerticalBarsDrawer, HorizontalBarsDrawer
)
from qrcode.image.styles.colormasks import (
    SolidFillColorMask, RadialGradiantColorMask, SquareGradiantColorMask,
    HorizontalGradiantColorMask, VerticalGradiantColorMask
)
from PIL import Image, ImageDraw, ImageFont, ImageOps

# --- Helper Class: Ô nhập liệu hỗ trợ Kéo Thả ---
class DragDropLineEdit(QLineEdit):
    def __init__(self, parent=None, placeholder=""):
        super().__init__(parent)
        self.setPlaceholderText(placeholder)
        self.setAcceptDrops(True)
        self.setReadOnly(True)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        if files:
            # Lấy file đầu tiên
            self.setText(files[0])

# --- Main App ---
class QRApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QR Code Generator Ultimate Pro - Fix & Features")
        self.setGeometry(50, 50, 1200, 800)
        
        # Variables
        self.qr_color = "#000000"
        self.bg_color = "#FFFFFF"
        self.grad_color = "#0000FF"
        self.generated_image = None
        self.last_save_path = ""
        self._img_data_ref = None # Quan trọng: Giữ tham chiếu data ảnh để tránh lỗi QImage
        self.history_data = []

        self.init_ui()
        self.create_menu()
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.status_msg("Sẵn sàng. Kéo thả ảnh logo vào ô nhập liệu để chọn nhanh.")

    def init_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)

        # === LEFT PANEL (Inputs & Settings) ===
        left_layout = QVBoxLayout()
        main_layout.addLayout(left_layout, 60)

        # 1. Config Nhanh (Presets) - TÍNH NĂNG MỚI
        preset_group = QGroupBox("🚀 Cấu hình nhanh (Presets)")
        preset_layout = QHBoxLayout()
        self.combo_preset = QComboBox()
        self.combo_preset.addItems(["-- Chọn mẫu có sẵn --", "Facebook Blue", "Zalo Blue", "Youtube Red", "Forest Green", "Elegant Black", "Love Pink", "Golden Luxury"])
        self.combo_preset.currentIndexChanged.connect(self.apply_preset)
        self.btn_random = QPushButton("🎲 Ngẫu nhiên")
        self.btn_random.clicked.connect(self.random_style)
        preset_layout.addWidget(QLabel("Mẫu:"))
        preset_layout.addWidget(self.combo_preset)
        preset_layout.addWidget(self.btn_random)
        preset_group.setLayout(preset_layout)
        left_layout.addWidget(preset_group)

        # 2. Tabs Input
        self.tabs_input = QTabWidget()
        self.setup_input_tabs()
        left_layout.addWidget(self.tabs_input)

        # 3. Tabs Settings (Advanced)
        self.tabs_settings = QTabWidget()
        self.setup_settings_tabs()
        left_layout.addWidget(self.tabs_settings)

        # 4. Generate Button
        btn_layout = QHBoxLayout()
        self.btn_generate = QPushButton("⚡ TẠO QR CODE")
        self.btn_generate.setStyleSheet("background-color: #007AFF; color: white; font-weight: bold; padding: 12px; font-size: 14px;")
        self.btn_generate.clicked.connect(self.generate_single_qr)
        
        self.btn_reset = QPushButton("↺ Reset")
        self.btn_reset.clicked.connect(self.reset_settings)
        self.btn_reset.setStyleSheet("padding: 12px;")

        btn_layout.addWidget(self.btn_generate)
        btn_layout.addWidget(self.btn_reset)
        left_layout.addLayout(btn_layout)

        # === RIGHT PANEL (Preview & Tools) ===
        right_layout = QVBoxLayout()
        main_layout.addLayout(right_layout, 40)

        # Preview Label
        self.lbl_preview = QLabel("Bản xem trước")
        self.lbl_preview.setAlignment(Qt.AlignCenter)
        self.lbl_preview.setStyleSheet("border: 2px dashed #ccc; background-color: #f0f0f0; border-radius: 8px;")
        self.lbl_preview.setMinimumSize(400, 400)
        right_layout.addWidget(self.lbl_preview)

        # Zoom & Info
        zoom_layout = QHBoxLayout()
        zoom_layout.addWidget(QLabel("🔍 Zoom:"))
        self.slider_zoom = QSlider(Qt.Horizontal)
        self.slider_zoom.setRange(100, 600)
        self.slider_zoom.setValue(400)
        self.slider_zoom.valueChanged.connect(self.update_preview_display)
        zoom_layout.addWidget(self.slider_zoom)
        right_layout.addLayout(zoom_layout)

        # Save Actions
        action_layout = QHBoxLayout()
        self.btn_save = QPushButton("💾 Lưu Ảnh")
        self.btn_save.clicked.connect(self.save_image)
        self.btn_copy = QPushButton("📋 Sao Chép")
        self.btn_copy.clicked.connect(self.copy_to_clipboard)
        self.btn_open_folder = QPushButton("📂 Mở Thư mục") # TÍNH NĂNG MỚI
        self.btn_open_folder.clicked.connect(self.open_save_folder)

        action_layout.addWidget(self.btn_save)
        action_layout.addWidget(self.btn_copy)
        action_layout.addWidget(self.btn_open_folder)
        right_layout.addLayout(action_layout)

        # History List - TÍNH NĂNG MỚI
        history_group = QGroupBox("📜 Lịch sử tạo gần đây")
        h_layout = QVBoxLayout()
        self.list_history = QListWidget()
        self.list_history.setMaximumHeight(150)
        self.list_history.itemClicked.connect(self.load_history_item)
        h_layout.addWidget(self.list_history)
        history_group.setLayout(h_layout)
        right_layout.addWidget(history_group)

    def setup_input_tabs(self):
        # Tab 1: Text
        self.tab_text = QWidget()
        l1 = QVBoxLayout()
        self.txt_content = QTextEdit()
        self.txt_content.setPlaceholderText("Nhập nội dung bất kỳ...")
        l1.addWidget(QLabel("Nội dung văn bản:")) # Added label
        l1.addWidget(self.txt_content)
        self.tabs_input.addTab(self.tab_text, "📝 Văn bản")

        # Tab 2: Wifi
        self.tab_wifi = QWidget()
        l2 = QFormLayout()
        self.wifi_ssid = QLineEdit()
        self.wifi_pass = QLineEdit(); self.wifi_pass.setEchoMode(QLineEdit.Password)
        self.wifi_auth = QComboBox(); self.wifi_auth.addItems(["WPA", "WEP", "nopass"])
        l2.addRow("Tên Wifi:", self.wifi_ssid)
        l2.addRow("Mật khẩu:", self.wifi_pass)
        l2.addRow("Bảo mật:", self.wifi_auth)
        self.tab_wifi.setLayout(l2)
        self.tabs_input.addTab(self.tab_wifi, "📶 Wifi")

        # Tab 3: Card/Social
        self.tab_social = QWidget()
        l3 = QFormLayout()
        self.soc_type = QComboBox()
        self.soc_type.addItems(["Facebook", "Youtube", "Zalo (Link)", "Website", "Email", "SĐT"])
        self.soc_val = QLineEdit()
        l3.addRow("Loại:", self.soc_type)
        l3.addRow("Giá trị/Link:", self.soc_val)
        self.tab_social.setLayout(l3)
        self.tabs_input.addTab(self.tab_social, "🌐 Social")

        # Tab 4: Batch (Hàng loạt) - TÍNH NĂNG MỚI
        self.tab_batch = QWidget()
        l4 = QVBoxLayout()
        self.txt_batch = QTextEdit()
        self.txt_batch.setPlaceholderText("Nhập danh sách mã, mỗi mã một dòng...")
        self.btn_batch_run = QPushButton("🏃 Chạy tạo hàng loạt")
        self.btn_batch_run.clicked.connect(self.run_batch)
        self.progress_batch = QProgressBar()
        l4.addWidget(QLabel("Danh sách dữ liệu:"))
        l4.addWidget(self.txt_batch)
        l4.addWidget(self.btn_batch_run)
        l4.addWidget(self.progress_batch)
        self.tab_batch.setLayout(l4)
        self.tabs_input.addTab(self.tab_batch, "📚 Hàng loạt")

    def setup_settings_tabs(self):
        # Tab Visual
        self.tab_vis = QWidget()
        l_vis = QFormLayout()
        
        # Colors
        c_lay = QHBoxLayout()
        self.btn_color = QPushButton("Màu QR"); self.btn_color.clicked.connect(lambda: self.choose_color('qr'))
        self.btn_bg = QPushButton("Màu Nền"); self.btn_bg.clicked.connect(lambda: self.choose_color('bg'))
        self.chk_trans = QCheckBox("Trong suốt")
        c_lay.addWidget(self.btn_color); c_lay.addWidget(self.btn_bg); c_lay.addWidget(self.chk_trans)
        l_vis.addRow("Màu sắc:", c_lay)

        # Logo & Caption - TÍNH NĂNG MỚI
        self.inp_logo = DragDropLineEdit(placeholder="Kéo ảnh logo vào đây...")
        self.btn_clr_logo = QPushButton("X"); self.btn_clr_logo.setFixedWidth(30); self.btn_clr_logo.clicked.connect(lambda: self.inp_logo.clear())
        
        logo_lay = QHBoxLayout(); logo_lay.addWidget(self.inp_logo); logo_lay.addWidget(self.btn_clr_logo)
        l_vis.addRow("Logo:", logo_lay)

        # Slider Logo Size
        self.slider_logo_size = QSlider(Qt.Horizontal)
        self.slider_logo_size.setRange(1, 5); self.slider_logo_size.setValue(3)
        l_vis.addRow("Cỡ Logo:", self.slider_logo_size)

        # Caption (Chữ dưới QR)
        self.inp_caption = QLineEdit()
        self.inp_caption.setPlaceholderText("VD: Quét để thanh toán")
        l_vis.addRow("Chữ dưới QR:", self.inp_caption)

        self.tab_vis.setLayout(l_vis)
        self.tabs_settings.addTab(self.tab_vis, "🎨 Giao diện")

        # Tab Style (Advanced)
        self.tab_style = QWidget()
        l_style = QFormLayout()
        self.combo_drawer = QComboBox()
        self.combo_drawer.addItems(["Vuông (Cổ điển)", "Bo góc (Rounded)", "Tròn (Circle)", "Kẻ dọc", "Kẻ ngang"])
        self.combo_mask = QComboBox()
        self.combo_mask.addItems(["Màu đơn", "Gradient Dọc", "Gradient Ngang", "Gradient Tròn"])
        self.btn_grad_color = QPushButton("Màu Gradient"); self.btn_grad_color.clicked.connect(lambda: self.choose_color('grad'))
        
        l_style.addRow("Kiểu dáng:", self.combo_drawer)
        l_style.addRow("Hiệu ứng màu:", self.combo_mask)
        l_style.addRow("Màu phụ:", self.btn_grad_color)
        self.tab_style.setLayout(l_style)
        self.tabs_settings.addTab(self.tab_style, "⚙️ Nâng cao")

    def create_menu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')
        exit_act = QAction('Thoát', self); exit_act.triggered.connect(self.close)
        file_menu.addAction(exit_act)

    # --- Logic ---

    def choose_color(self, target):
        c = QColorDialog.getColor()
        if c.isValid():
            h = c.name()
            if target == 'qr': self.qr_color = h; self.btn_color.setStyleSheet(f"background:{h};color:white")
            elif target == 'bg': self.bg_color = h; self.btn_bg.setStyleSheet(f"background:{h}")
            elif target == 'grad': self.grad_color = h; self.btn_grad_color.setStyleSheet(f"background:{h};color:white")

    def get_input_data(self):
        idx = self.tabs_input.currentIndex()
        if idx == 0: return self.txt_content.toPlainText()
        elif idx == 1: 
            return f"WIFI:S:{self.wifi_ssid.text()};T:{self.wifi_auth.currentText()};P:{self.wifi_pass.text()};;"
        elif idx == 2:
            type_ = self.soc_type.currentText()
            val = self.soc_val.text()
            if "SĐT" in type_: return f"tel:{val}"
            if "Email" in type_: return f"mailto:{val}"
            return val # Link
        return ""

    def apply_preset(self, idx):
        if idx == 0: return # Default
        name = self.combo_preset.currentText()
        
        # Reset colors first
        self.chk_trans.setChecked(False)
        
        if "Facebook" in name:
            self.qr_color = "#1877F2"; self.bg_color = "#FFFFFF"; self.combo_drawer.setCurrentIndex(1) # Rounded
        elif "Zalo" in name:
            self.qr_color = "#0068FF"; self.bg_color = "#FFFFFF"; self.combo_drawer.setCurrentIndex(2) # Circle
        elif "Youtube" in name:
            self.qr_color = "#FF0000"; self.bg_color = "#FFFFFF"; self.combo_drawer.setCurrentIndex(0)
        elif "Forest" in name:
            self.qr_color = "#228B22"; self.bg_color = "#F0FFF0"; self.combo_drawer.setCurrentIndex(3) # Vertical
        elif "Elegant" in name:
            self.qr_color = "#000000"; self.bg_color = "#D4AF37"; self.combo_drawer.setCurrentIndex(1)
        elif "Love" in name:
            self.qr_color = "#FF1493"; self.bg_color = "#FFC0CB"; self.combo_drawer.setCurrentIndex(2)
        elif "Luxury" in name:
            self.qr_color = "#DAA520"; self.bg_color = "#2C2C2C"; self.combo_drawer.setCurrentIndex(1)
            self.combo_mask.setCurrentIndex(3); self.grad_color = "#FFFF00"

        # Update Buttons
        self.btn_color.setStyleSheet(f"background:{self.qr_color};color:white")
        self.btn_bg.setStyleSheet(f"background:{self.bg_color}")
        self.status_msg(f"Đã áp dụng mẫu: {name}")

    def random_style(self):
        import random
        drawers = [0, 1, 2, 3, 4]
        self.combo_drawer.setCurrentIndex(random.choice(drawers))
        
        # Random vivid colors
        def r_col(): return f"#{random.randint(0, 0xFFFFFF):06x}"
        self.qr_color = r_col()
        self.bg_color = "#FFFFFF"
        self.btn_color.setStyleSheet(f"background:{self.qr_color};color:white")
        self.btn_bg.setStyleSheet(f"background:{self.bg_color}")
        self.status_msg("Đã chọn style ngẫu nhiên!")

    def generate_single_qr(self):
        data = self.get_input_data()
        if not data.strip():
            QMessageBox.warning(self, "Lỗi", "Chưa nhập dữ liệu!")
            return
        
        try:
            # Tạo ảnh
            img = self.create_qr_image(data)
            self.generated_image = img
            self.update_preview_display()
            
            # Thêm vào history
            short_txt = (data[:25] + '..') if len(data) > 25 else data
            self.history_data.append(data)
            self.list_history.addItem(f"{time.strftime('%H:%M')} - {short_txt}")
            self.status_msg("Tạo mã thành công!")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", str(e))

    def create_qr_image(self, data):
        # 1. Basic QR
        qr = qrcode.QRCode(version=None, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=2)
        qr.add_data(data)
        qr.make(fit=True)

        # 2. Config Drawers
        drawers = [SquareModuleDrawer(), RoundedModuleDrawer(), CircleModuleDrawer(), VerticalBarsDrawer(), HorizontalBarsDrawer()]
        sel_drawer = drawers[self.combo_drawer.currentIndex()]
        
        # 3. Colors & Masks
        c_qr = QColor(self.qr_color).getRgb()[:3]
        c_bg = QColor(self.bg_color).getRgb()[:3]
        if self.chk_trans.isChecked(): c_bg = (255, 255, 255, 0)
        c_grad = QColor(self.grad_color).getRgb()[:3]

        masks = [
            SolidFillColorMask(c_qr, c_bg),
            VerticalGradiantColorMask(c_bg, c_qr, c_grad),
            HorizontalGradiantColorMask(c_bg, c_qr, c_grad),
            RadialGradiantColorMask(c_bg, c_qr, c_grad)
        ]
        
        # 4. Logo Logic
        logo_file = self.inp_logo.text()
        embed_logo = None
        if logo_file and os.path.exists(logo_file):
            embed_logo = logo_file

        # Generate
        img = qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=sel_drawer,
            color_mask=masks[self.combo_mask.currentIndex()],
            embeded_image_path=embed_logo
        ).convert("RGBA")

        # 5. Resize Logo Manually (Optional advanced control)
        # Note: 'qrcode' lib resizes logo automatically based on error correction coverage.
        # But if we want to force size, we manipulate it here?
        # Better: let lib handle insertion, we handle post-processing caption.
        
        # 6. Add Caption (Chữ dưới)
        caption = self.inp_caption.text()
        if caption:
            # Expand image height
            w, h = img.size
            extra_h = 60 # pixels for text
            new_img = Image.new("RGBA", (w, h + extra_h), c_bg if not self.chk_trans.isChecked() else (0,0,0,0))
            new_img.paste(img, (0, 0))
            
            draw = ImageDraw.Draw(new_img)
            # Try load font, fallback default
            try:
                font = ImageFont.truetype("arial.ttf", 24)
            except:
                font = ImageFont.load_default()
            
            # Center text (Newer Pillow uses textbbox)
            try:
                # Pillow >= 10
                left, top, right, bottom = draw.textbbox((0, 0), caption, font=font)
                text_w = right - left
                text_h = bottom - top
            except:
                # Old Pillow
                text_w, text_h = draw.textsize(caption, font=font)
                
            draw.text(((w - text_w) / 2, h + (extra_h - text_h) / 2 - 5), caption, fill=c_qr, font=font)
            img = new_img

        return img

    def update_preview_display(self):
        if not self.generated_image: return
        
        # Sửa lỗi Crash QImage: Giữ tham chiếu bytes
        img = self.generated_image
        self._img_data_ref = img.tobytes("raw", "RGBA") # Store in self
        
        qim = QImage(self._img_data_ref, img.size[0], img.size[1], QImage.Format_RGBA8888)
        pix = QPixmap.fromImage(qim)
        
        scale = self.slider_zoom.value()
        self.lbl_preview.setPixmap(pix.scaled(scale, scale, Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def run_batch(self):
        lines = self.txt_batch.toPlainText().split('\n')
        lines = [x.strip() for x in lines if x.strip()]
        
        if not lines:
            QMessageBox.warning(self, "Lỗi", "Danh sách trống!")
            return
            
        folder = QFileDialog.getExistingDirectory(self, "Chọn thư mục lưu ảnh")
        if not folder: return

        self.progress_batch.setValue(0)
        self.progress_batch.setMaximum(len(lines))
        
        for i, line in enumerate(lines):
            try:
                img = self.create_qr_image(line)
                # Clean filename
                safe_name = "".join([c for c in line if c.isalnum() or c in (' ','-','_')]).strip()[:20]
                img.save(os.path.join(folder, f"QR_{i+1}_{safe_name}.png"))
                self.progress_batch.setValue(i + 1)
                QApplication.processEvents() # Keep UI responsive
            except Exception as e:
                print(f"Lỗi dòng {i}: {e}")
        
        QMessageBox.information(self, "Xong", f"Đã tạo {len(lines)} ảnh trong thư mục!")
        self.last_save_path = folder

    def save_image(self):
        if not self.generated_image: return
        path, _ = QFileDialog.getSaveFileName(self, "Lưu", self.last_save_path, "PNG (*.png);;JPG (*.jpg)")
        if path:
            self.generated_image.save(path)
            self.last_save_path = os.path.dirname(path)
            self.status_msg("Đã lưu ảnh!")

    def copy_to_clipboard(self):
        if not self.generated_image: return
        img = self.generated_image
        data = img.tobytes("raw", "RGBA")
        qim = QImage(data, img.size[0], img.size[1], QImage.Format_RGBA8888)
        QApplication.clipboard().setImage(qim)
        self.status_msg("Đã copy vào Clipboard!")

    def open_save_folder(self):
        if self.last_save_path and os.path.exists(self.last_save_path):
            QDesktopServices.openUrl(QUrl.fromLocalFile(self.last_save_path))
        else:
            self.status_msg("Chưa có thư mục lưu nào được ghi nhận.")

    def load_history_item(self, item):
        # Lấy lại text từ history list (bỏ phần giờ)
        txt = item.text().split(' - ', 1)[1] if ' - ' in item.text() else item.text()
        # Tìm data full tương ứng (đơn giản hóa: dùng text hiển thị)
        # Để chính xác, nên lưu dict. Ở đây demo dùng text trực tiếp
        # Nạp lại vào Tab Text để user sửa
        self.tabs_input.setCurrentIndex(0)
        self.txt_content.setText(txt)
        # Tự động generate lại?
        self.generate_single_qr()

    def reset_settings(self):
        self.qr_color = "#000000"; self.bg_color = "#FFFFFF"
        self.btn_color.setStyleSheet(f"background:{self.qr_color};color:white")
        self.btn_bg.setStyleSheet(f"background:{self.bg_color}")
        self.inp_logo.clear()
        self.inp_caption.clear()
        self.combo_preset.setCurrentIndex(0)
        self.combo_drawer.setCurrentIndex(0)
        self.combo_mask.setCurrentIndex(0)
        self.generated_image = None
        self.lbl_preview.clear()
        self.lbl_preview.setText("Bản xem trước")
        self.status_msg("Đã Reset!")

    def status_msg(self, msg):
        self.statusBar.showMessage(msg, 5000)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = QRApp()
    window.show()
    sys.exit(app.exec_())