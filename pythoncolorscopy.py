import tkinter as tk
from tkinter import filedialog, scrolledtext
from PIL import Image, ImageTk
import os

class ColorSorterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("调色盘复制机")
        self.root.geometry("800x600")

        self.top_frame = tk.Frame(self.root)
        self.top_frame.pack(pady=10, fill=tk.X)
        
        self.middle_frame = tk.Frame(self.root)
        self.middle_frame.pack(pady=10, fill=tk.BOTH, expand=True)
        
        self.bottom_frame = tk.Frame(self.root)
        self.bottom_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        # 按钮们
        self.path_label = tk.Label(self.top_frame, text="未选择图片")
        self.path_label.pack(side=tk.LEFT, padx=5)
        
        self.select_button = tk.Button(self.top_frame, text="选择图片", command=self.select_image)
        self.select_button.pack(side=tk.LEFT, padx=5)

        self.save_button = tk.Button(self.top_frame, text="保存调色盘", command=self.save_colors)
        self.save_button.pack(side=tk.LEFT, padx=5)

        # 按照亮度排序选框
        self.sort_var = tk.BooleanVar(value=True)
        self.sort_check = tk.Checkbutton(
            self.top_frame, 
            text="按亮度排序", 
            variable=self.sort_var,
            command=self.display_image_and_colors
        )
        self.sort_check.pack(side=tk.LEFT, padx=5)

        # 图片预览
        self.canvas = tk.Canvas(self.middle_frame, width=300, height=300, bg='white')
        self.canvas.pack(pady=5)

        # 文本框
        self.colors_text = scrolledtext.ScrolledText(self.bottom_frame, height=10, width=50)
        self.colors_text.pack(pady=5, fill=tk.BOTH, expand=True)

        self.image_path = None
        self.photo = None

    def select_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("图片文件", "*.png *.jpg *.jpeg *.bmp *.gif")]
        )
        if file_path:
            self.image_path = file_path
            self.path_label.config(text=os.path.basename(file_path))
            self.display_image_and_colors()

    def get_sorted_hex_colors(self, image_path):
        try:
            img = Image.open(image_path).convert("RGB")
            unique_colors = set(img.getdata())

            if self.sort_var.get():
                def luminance(rgb):
                    r, g, b = rgb
                    return 0.2126*r + 0.7152*g + 0.0722*b
                sorted_colors = sorted(unique_colors, key=luminance)
            else:
                sorted_colors = list(unique_colors)

            hex_colors = [f"#{r:02x}{g:02x}{b:02x}" for r, g, b in sorted_colors]
            return hex_colors
        except Exception as e:
            return [f"出错: {str(e)}"]

    def display_image_and_colors(self):
        if not self.image_path:
            return

        # 小图片
        img = Image.open(self.image_path)
        img.thumbnail((300, 300))
        self.photo = ImageTk.PhotoImage(img)
        self.canvas.delete("全部")
        self.canvas.create_image(150, 150, image=self.photo)

        # 取色
        colors = self.get_sorted_hex_colors(self.image_path)
        self.colors_text.delete(1.0, tk.END)
        sort_status = "按亮度排序" if self.sort_var.get() else "未排序"
        self.colors_text.insert(tk.END, f";这个图有 {len(colors)} 种颜色 ({sort_status}):\n\n")
        for color in colors:
            self.colors_text.insert(tk.END, f"{color}\n")

    def save_colors(self):
        if not self.image_path:
            self.colors_text.delete(1.0, tk.END)
            self.colors_text.insert(tk.END, "请先选择图片.\n")
            return

        colors = self.get_sorted_hex_colors(self.image_path)
        if not colors or colors[0].startswith("出错"):
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("文本文件", "*.txt")],
            title="保存调色盘至"
        )
        if file_path:
            try:
                sort_status = "按亮度排序" if self.sort_var.get() else "未排序"
                with open(file_path, 'w') as f:
                    f.write(f";这个图有 {len(colors)} 种颜色 ({sort_status}):\n\n")
                    for color in colors:
                        f.write(f"{color}\n")
                self.colors_text.delete(1.0, tk.END)
                self.colors_text.insert(tk.END, f"Colors saved to {os.path.basename(file_path)}\n\n")
                self.colors_text.insert(tk.END, f"Found {len(colors)} colors ({sort_status}):\n\n")
                for color in colors:
                    self.colors_text.insert(tk.END, f"{color}\n")
            except Exception as e:
                self.colors_text.delete(1.0, tk.END)
                self.colors_text.insert(tk.END, f"Error saving file: {str(e)}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = ColorSorterGUI(root)
    root.mainloop()
