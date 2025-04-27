import tkinter as tk
from tkinter import ttk, Scale
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from TerrainGenerator import TerrainGenerator 

class TerrainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fractal Terrain Generator")
        self.root.geometry("800x600")
        self.size_var = tk.IntVar(value=65)
        self.roughness_var = tk.DoubleVar(value=0.7)
        
        self.create_ui()
        self.terrain_generator = TerrainGenerator(size=self.size_var.get())
        self.generate_terrain()
    
    def create_ui(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        control_frame = ttk.LabelFrame(main_frame, text="Controls", padding="10")
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        ttk.Label(control_frame, text="Size (2^n + 1):").pack(anchor=tk.W, pady=(10, 0))
        size_options = [2, 3, 5, 9, 17, 33, 65, 129]
        size_combo = ttk.Combobox(control_frame, values=size_options, textvariable=self.size_var, state="readonly", width=10)
        size_combo.pack(anchor=tk.W, pady=(0, 10))
        
        ttk.Label(control_frame, text="Roughness:").pack(anchor=tk.W, pady=(10, 0))
        roughness_scale = Scale(control_frame, variable=self.roughness_var, from_=0.1, to=1.0, orient=tk.HORIZONTAL, 
                               resolution=0.1, length=150)
        roughness_scale.pack(anchor=tk.W, pady=(0, 10))
        
        generate_button = ttk.Button(control_frame, text="Generate Terrain", command=self.on_generate)
        generate_button.pack(anchor=tk.W, pady=20)
        
        self.display_mode = tk.StringVar(value="3D")
        ttk.Label(control_frame, text="Display Mode:").pack(anchor=tk.W, pady=(10, 0))
        ttk.Radiobutton(control_frame, text="3D Surface", variable=self.display_mode, value="3D", command=self.update_display).pack(anchor=tk.W)
        ttk.Radiobutton(control_frame, text="2D Contour", variable=self.display_mode, value="2D", command=self.update_display).pack(anchor=tk.W)
        
        self.display_frame = ttk.LabelFrame(main_frame, text="Terrain Visualization", padding="10")
        self.display_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.fig = plt.Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.display_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def on_generate(self):
        size = self.size_var.get()
        self.terrain_generator = TerrainGenerator(size=size)
        self.generate_terrain()
    
    def generate_terrain(self):
        roughness = self.roughness_var.get()
        seed = np.random.seed()
        
        self.terrain = self.terrain_generator.generate(roughness=roughness, seed=seed)
        
        self.update_display()
    
    def update_display(self):
        self.fig.clear()
        
        if self.display_mode.get() == "3D":
            ax = self.fig.add_subplot(111, projection='3d')
            
            x = np.linspace(0, 1, self.terrain.shape[0])
            y = np.linspace(0, 1, self.terrain.shape[1])
            X, Y = np.meshgrid(x, y)
            
            surf = ax.plot_surface(X, Y, self.terrain, cmap='terrain', linewidth=0, 
                                 antialiased=True, rstride=1, cstride=1)
            
            ax.set_title('3D Fractal Terrain')
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlim(-1, 1)
            ax.set_zlabel('Height')
            
        else: 
            ax = self.fig.add_subplot(111)
            contour = ax.contourf(self.terrain, cmap='terrain', levels=20)
            self.fig.colorbar(contour, ax=ax)
            ax.set_title('Terrain Contour Map')
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.axis('equal')
        
        self.fig.tight_layout()
        self.canvas.draw()