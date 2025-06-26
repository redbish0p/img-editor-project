import cv2
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk


class ImageProcessorApp:
    """Класс, реализующий основное приложение"""
    def __init__(self, root):
        self.root = root
        self.root.title("Обработка изображений")
        
        # Изображение, с которым проводятся все операции
        self.image = None
        # Изображение, отображаемое в окне
        self.display_image = None
        # Оригинальное изображение
        self.original_image = None

        # Создание интерфейса
        self.create_widgets()

    def create_widgets(self):
        """Создаёт интерфейс приложения""" 
        # Фрейм для изображения
        self.image_frame = tk.Frame(self.root)
        self.image_frame.pack(side=tk.TOP, padx=5, pady=5)
        
        self.canvas = tk.Canvas(self.image_frame, 
                                width=600, 
                                height=400, 
                                bg='gray')
        self.canvas.pack()
        
        # Фрейм для управления
        self.control_frame = tk.Frame(self.root)
        self.control_frame.pack(side=tk.BOTTOM, padx=5, pady=5)
        
        # Кнопка загрузки изображения
        self.load_btn = tk.Button(self.control_frame,
                                  text="Загрузить изображение",
                                  command=self.load_image)
        self.load_btn.grid(row=0, column=0, padx=5, pady=5)
        
        # Кнопка снимка изображения с камеры
        self.camera_btn = tk.Button(self.control_frame, 
                                    text="Сделать снимок с камеры", 
                                    command=self.capture_from_camera)
        self.camera_btn.grid(row=0, column=1, padx=5, pady=5)
        
        # Каналы изображения
        self.channel_var = tk.StringVar(value="all")
        tk.Label(self.control_frame,
                 text="Каналы:").grid(row=1, column=0, padx=5, pady=5)
        tk.Radiobutton(self.control_frame, 
                       text="Все", 
                       variable=self.channel_var, 
                       value="all", 
                       command=self.update_channels).grid(row=1, column=1)
        tk.Radiobutton(self.control_frame, 
                       text="Красный", 
                       variable=self.channel_var, 
                       value="red", 
                       command=self.update_channels).grid(row=1, column=2)
        tk.Radiobutton(self.control_frame, 
                       text="Зеленый", 
                       variable=self.channel_var, 
                       value="green", 
                       command=self.update_channels).grid(row=1, column=3)
        tk.Radiobutton(self.control_frame, 
                       text="Синий", 
                       variable=self.channel_var, 
                       value="blue", 
                       command=self.update_channels).grid(row=1, column=4)
        
        # Обрезка изображения
        tk.Label(self.control_frame,
                  text="Обрезка (x1,y1,x2,y2):").grid(row=2, column=0, 
                                                      padx=5, pady=5)
        self.crop_x1_entry = tk.Entry(self.control_frame, width=5)
        self.crop_x1_entry.grid(row=2, column=1, padx=5, pady=5)
        self.crop_y1_entry = tk.Entry(self.control_frame, width=5)
        self.crop_y1_entry.grid(row=2, column=2, padx=5, pady=5)
        self.crop_x2_entry = tk.Entry(self.control_frame, width=5)
        self.crop_x2_entry.grid(row=2, column=3, padx=5, pady=5)
        self.crop_y2_entry = tk.Entry(self.control_frame, width=5)
        self.crop_y2_entry.grid(row=2, column=4, padx=5, pady=5)
        self.crop_btn = tk.Button(self.control_frame, 
                                  text="Применить обрезку", 
                                  command=self.apply_crop)
        self.crop_btn.grid(row=2, column=5, padx=5, pady=5)
        
        # Рисование круга
        tk.Label(self.control_frame, text="Круг (x,y,радиус):").grid(row=3, column=0, padx=5, pady=5)
        self.circle_x_entry = tk.Entry(self.control_frame, width=5)
        self.circle_x_entry.grid(row=3, column=1, padx=5, pady=5)
        self.circle_y_entry = tk.Entry(self.control_frame, width=5)
        self.circle_y_entry.grid(row=3, column=2, padx=5, pady=5)
        self.circle_r_entry = tk.Entry(self.control_frame, width=5)
        self.circle_r_entry.grid(row=3, column=3, padx=5, pady=5)
        self.draw_circle_btn = tk.Button(self.control_frame, 
                                        text="Нарисовать круг", 
                                        command=self.draw_circle)
        self.draw_circle_btn.grid(row=3, column=4, padx=5, pady=5)
        
        # Вращение изображения
        tk.Label(self.control_frame, 
                 text="Угол поворота:").grid(row=4, column=0, padx=5, pady=5)
        self.rotate_entry = tk.Entry(self.control_frame, width=10)
        self.rotate_entry.grid(row=4, column=1, padx=5, pady=5)
        self.rotate_btn = tk.Button(self.control_frame, 
                                    text="Повернуть", 
                                    command=self.rotate_image)
        self.rotate_btn.grid(row=4, column=2, padx=5, pady=5)
        
        # Сброс изображения
        self.reset_btn = tk.Button(self.control_frame, 
                                   text="Сбросить изображение", 
                                   command=self.reset_image)
        self.reset_btn.grid(row=5, column=0, columnspan=6, pady=5)
    
    def load_image(self):
        """Загружает изображение из файла"""
        file_path = filedialog.askopenfilename(filetypes=[("Изображения",
                                                           "*.jpg *.jpeg *.png")])
        if file_path:
            try:
                self.image = cv2.imread(file_path)
                if self.image is None:
                    raise ValueError("Не удалось прочитать изображение")
                self.original_image = self.image.copy()
                self.display_image = self.image.copy()
                self.show_image()
            except Exception as e:
                messagebox.showerror("Ошибка", 
                                     f"Ошибка загрузки изображения: {str(e)}")
    
    def capture_from_camera(self):
        """Получает снимок с веб-камеры"""
        try:
            cam = cv2.VideoCapture(0)
            if not cam.isOpened():
                raise ValueError("Не удалось открыть камеру")
            
            ret, frame = cam.read()
            if not ret:
                raise ValueError("Не удалось получить кадр")
            
            # Конвертация из BGR в RGB для правильного отображения
            self.image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            self.original_image = self.image.copy()
            self.display_image = self.image.copy()
            self.show_image()
            
            cam.release()
        except Exception as e:
            messagebox.showerror("Ошибка", 
                                 f"Ошибка при захвате с камеры: {str(e)}")
            if 'cam' in locals():
                if cam is not None:
                    cam.release()
    
    def show_image(self):
        """Показывает изображение в окне"""
        if self.display_image is not None:
            # Конвертация из BGR в RGB для правильного отображения
            img = cv2.cvtColor(self.display_image, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            
            # Масштабирование изображения для отображения
            img_width, img_height = img.size
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            
            scale = min(canvas_width / img_width, canvas_height / img_height)
            new_width = int(img_width * scale)
            new_height = int(img_height * scale)
            img = img.resize((new_width, new_height), Image.LANCZOS)
            
            self.tk_image = ImageTk.PhotoImage(img)
            self.canvas.create_image(canvas_width//2, 
                                     canvas_height//2, 
                                     anchor=tk.CENTER, 
                                     image=self.tk_image)
    
    def update_channels(self):
        """Показывает определённый канал изображения"""
        if self.image is not None:
            channel = self.channel_var.get()
            if channel == "all":
                self.display_image = self.image.copy()
            else:
                b, g, r = cv2.split(self.image)
                if channel == "red":
                    self.display_image = cv2.merge([b*0, g*0, r])
                elif channel == "green":
                    self.display_image = cv2.merge([b*0, g, r*0])
                elif channel == "blue":
                    self.display_image = cv2.merge([b, g*0, r*0])
            self.show_image()
    
    def apply_crop(self):
        """Выполняет обрезку изображения по введенным координатам"""
        if self.image is not None:
            try:
                x1 = int(self.crop_x1_entry.get())
                y1 = int(self.crop_y1_entry.get())
                x2 = int(self.crop_x2_entry.get())
                y2 = int(self.crop_y2_entry.get())
                
                if x1 == x2 or y1 == y2:
                    raise ValueError("Координаты не содержат пикселей")

                # Убедимся, что x1 < x2 и y1 < y2
                x1, x2 = min(x1, x2), max(x1, x2)
                y1, y2 = min(y1, y2), max(y1, y2)
                
                # Проверка на выход за границы изображения
                h, w = self.image.shape[:2]
                if x1 < 0 or y1 < 0 or x2 > w or y2 > h:
                    raise ValueError("Координаты выходят за границы изображения")
                
                # Обрезаем изображение
                self.image = self.image[y1:y2, x1:x2]
                self.display_image = self.image.copy()
                self.show_image()
                
            except ValueError as e:
                messagebox.showerror("Ошибка", 
                                     f"Некорректные координаты: {str(e)}")
    
    def draw_circle(self):
        """Рисует круг на изображении по введенным координатам"""
        if self.image is not None:
            try:
                x = int(self.circle_x_entry.get())
                y = int(self.circle_y_entry.get())
                radius = int(self.circle_r_entry.get())
                
                # Проверка на выход за границы изображения
                h, w = self.image.shape[:2]
                if x < 0 or y < 0 or x > w or y > h:
                    raise ValueError("Координаты выходят за границы изображения")
                
                # Рисуем круг на изображении
                cv2.circle(self.image, (x, y), radius, (0, 0, 255), 2)
                self.display_image = self.image.copy()
                self.show_image()
                
            except ValueError as e:
                messagebox.showerror("Ошибка", 
                                     f"Некорректные параметры круга: {str(e)}")
    
    def rotate_image(self):
        """Поворачивает изображение на определённый угол"""
        if self.image is not None:
            try:
                angle = float(self.rotate_entry.get())
                
                # Получаем центр изображения
                (h, w) = self.image.shape[:2]
                center = (w // 2, h // 2)
                
                # Выполняем вращение
                M = cv2.getRotationMatrix2D(center, angle, 1.0)
                self.image = cv2.warpAffine(self.image, M, (w, h))
                self.display_image = self.image.copy()
                self.show_image()
            except ValueError:
                messagebox.showerror("Ошибка", 
                                     "Введите корректное число для угла поворота")
    
    def reset_image(self):
        """Возвращает изображение к исходному"""
        if self.original_image is not None:
            self.image = self.original_image.copy()
            self.display_image = self.image.copy()
            self.show_image()
            self.channel_var.set("all")


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessorApp(root)
    root.mainloop()