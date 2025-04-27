import tkinter as tk
from tkinter import Canvas, ttk
from PIL import ImageTk
import threading
from MandelbrotSet import MandelbrotSet
from JuliaSet import JuliaSet

class FractalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fractal Viewer")
        
        self.width, self.height = 800, 600
        self.fractal = MandelbrotSet(width=self.width, height=self.height)
        
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        self.canvas = Canvas(self.main_frame, width=self.width, height=self.height, bg="black")
        self.canvas.pack(side=tk.LEFT)
        
        self.control_frame = ttk.Frame(self.main_frame, padding="10")
        self.control_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.status_var = tk.StringVar(value="Ready")
        self.status_bar = ttk.Label(root, textvariable=self.status_var)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.setup_controls()
        
        self.canvas.bind("<Button-1>", self.zoom_in)
        self.canvas.bind("<Button-3>", self.zoom_out)
        
        self.tk_image = None
        
        self.draw_fractal()
        
    def update_iter_label(self, event=None):
        value = self.iter_var.get()
        self.iter_value_label.config(text=str(value))

    def update_julia_real_label(self, event=None):
        value = self.julia_real_var.get()
        self.julia_real_label.config(text=f"{value:.3f}")

    def update_julia_imag_label(self, event=None):
        value = self.julia_imag_var.get()
        self.julia_imag_label.config(text=f"{value:.3f}")

    def setup_controls(self):
        ttk.Label(self.control_frame, text="Fractal Type:").pack(anchor=tk.W)
        self.fractal_type = tk.StringVar(value="Mandelbrot")
        self.type_dropdown = ttk.Combobox(
            self.control_frame, 
            textvariable=self.fractal_type, 
            values=["Mandelbrot", "Julia"],
            state="readonly"
        )
        self.type_dropdown.pack(fill=tk.X, pady=5)
        self.type_dropdown.bind("<<ComboboxSelected>>", self.change_fractal)
        
        iter_frame = ttk.Frame(self.control_frame)
        iter_frame.pack(fill=tk.X, pady=5)
        ttk.Label(iter_frame, text="Iterations:").pack(side=tk.LEFT)
        self.iter_value_label = ttk.Label(iter_frame, width=4)
        self.iter_value_label.pack(side=tk.RIGHT)
        
        self.iter_var = tk.IntVar(value=self.fractal.max_iter)
        self.iter_slider = ttk.Scale(
            self.control_frame, 
            from_=10, 
            to=1000, 
            variable=self.iter_var,
            orient=tk.HORIZONTAL
        )
        self.iter_slider.pack(fill=tk.X)
        self.update_iter_label()
        self.iter_slider.bind("<Motion>", self.update_iter_label)
        self.iter_slider.bind("<ButtonRelease-1>", self.update_iterations)
        
        self.julia_frame = ttk.LabelFrame(self.control_frame, text="Julia Set Parameters")
        
        real_frame = ttk.Frame(self.julia_frame)
        real_frame.pack(fill=tk.X, pady=2)
        ttk.Label(real_frame, text="Real Part:").pack(side=tk.LEFT)
        self.julia_real_label = ttk.Label(real_frame, width=6)
        self.julia_real_label.pack(side=tk.RIGHT)
        
        self.julia_real_var = tk.DoubleVar(value=-0.7)
        self.julia_real_slider = ttk.Scale(
            self.julia_frame, 
            from_=-2.0, 
            to=2.0, 
            variable=self.julia_real_var,
            orient=tk.HORIZONTAL
        )
        self.julia_real_slider.pack(fill=tk.X)
        self.update_julia_real_label()
        self.julia_real_slider.bind("<Motion>", self.update_julia_real_label)
        
        imag_frame = ttk.Frame(self.julia_frame)
        imag_frame.pack(fill=tk.X, pady=2)
        ttk.Label(imag_frame, text="Imaginary Part:").pack(side=tk.LEFT)
        self.julia_imag_label = ttk.Label(imag_frame, width=6)
        self.julia_imag_label.pack(side=tk.RIGHT)
        
        self.julia_imag_var = tk.DoubleVar(value=0.27015)
        self.julia_imag_slider = ttk.Scale(
            self.julia_frame, 
            from_=-2.0, 
            to=2.0, 
            variable=self.julia_imag_var,
            orient=tk.HORIZONTAL
        )
        self.julia_imag_slider.pack(fill=tk.X)
        self.update_julia_imag_label()
        self.julia_imag_slider.bind("<Motion>", self.update_julia_imag_label)
        
        self.julia_update_button = ttk.Button(
            self.julia_frame, 
            text="Update", 
            command=self.update_julia_params
        )
        self.julia_update_button.pack(pady=5)
        
        ttk.Button(
            self.control_frame, 
            text="Reset View", 
            command=self.reset_view
        ).pack(fill=tk.X, pady=10)
    
    def draw_fractal(self):
        def task():
            self.status_var.set("Rendering...")
            self.root.update_idletasks()
            
            if isinstance(self.fractal, MandelbrotSet):
                x_min = -2.0 / self.fractal.zoom + self.fractal.offset_x
                x_max = 1.0 / self.fractal.zoom + self.fractal.offset_x
                y_min = -1.0 / self.fractal.zoom + self.fractal.offset_y
                y_max = 1.0 / self.fractal.zoom + self.fractal.offset_y
            else:  # Julia set
                x_min = -1.5 / self.fractal.zoom + self.fractal.offset_x
                x_max = 1.5 / self.fractal.zoom + self.fractal.offset_x
                y_min = -1.5 / self.fractal.zoom + self.fractal.offset_y
                y_max = 1.5 / self.fractal.zoom + self.fractal.offset_y
            
            image = self.fractal.generate(x_min, x_max, y_min, y_max)
            self.tk_image = ImageTk.PhotoImage(image)
            
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)
            
            self.status_var.set("Done")
        
        threading.Thread(target=task).start()
    
    def zoom_in(self, event):
        rel_x = event.x / self.width
        rel_y = event.y / self.height
        
        if isinstance(self.fractal, MandelbrotSet):
            width_range = 3.0 / self.fractal.zoom
            height_range = 2.0 / self.fractal.zoom
        else: # Julia set
            width_range = 3.0 / self.fractal.zoom
            height_range = 3.0 / self.fractal.zoom
        
        self.fractal.offset_x += (rel_x - 0.5) * width_range
        self.fractal.offset_y += (rel_y - 0.5) * height_range
        
        self.fractal.zoom *= 2
        self.draw_fractal()
    
    def zoom_out(self, event):
        self.fractal.zoom = max(1.0, self.fractal.zoom / 2)
        self.draw_fractal()
    
    def change_fractal(self, event=None):
        selected = self.fractal_type.get()
        current_iter = self.iter_var.get()
        
        if selected == "Mandelbrot":
            self.fractal = MandelbrotSet(width=self.width, height=self.height)
            self.julia_frame.pack_forget()
        else:  # Julia
            self.fractal = JuliaSet(width=self.width, height=self.height)
            self.julia_frame.pack(fill=tk.X, pady=10)
            self.fractal.set_julia_constant(self.julia_real_var.get(), self.julia_imag_var.get())
        
        self.fractal.set_max_iter(current_iter)
        
        self.reset_view()
    
    def update_iterations(self, event=None):
        value = self.iter_var.get()
        self.fractal.set_max_iter(value)
        self.draw_fractal()
    
    def update_julia_params(self):
        if isinstance(self.fractal, JuliaSet):
            real = self.julia_real_var.get()
            imag = self.julia_imag_var.get()
            self.fractal.set_julia_constant(real, imag)
            self.draw_fractal()
    
    def reset_view(self):
        self.fractal.zoom = 1.0
        self.fractal.offset_x = 0.0
        self.fractal.offset_y = 0.0
        self.draw_fractal()
