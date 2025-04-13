import tkinter as tk
from turtle import ScrolledCanvas, TurtleScreen
from lsystem import LSystem 
import math

class LSystemGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("L-systems")
        self.canvas_frame = tk.Frame(self.root)
        self.canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.canvas = tk.Canvas(self.canvas_frame, width=800, height=600,
                                scrollregion=(0, 0, 1600, 1200), bg='white')
        self.canvas.grid(row=0, column=0, sticky="nsew")

        self.v_scroll = tk.Scrollbar(self.canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.v_scroll.grid(row=0, column=1, sticky="ns")
        self.h_scroll = tk.Scrollbar(self.canvas_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.h_scroll.grid(row=1, column=0, sticky="ew")

        self.canvas.config(yscrollcommand=self.v_scroll.set, xscrollcommand=self.h_scroll.set)
        self.canvas_frame.rowconfigure(0, weight=1)
        self.canvas_frame.columnconfigure(0, weight=1)

        self.screen = TurtleScreen(self.canvas)
        self.screen.tracer(0, 0)

        self.lsystem = LSystem(self.screen)
        self.create_widgets()

    def create_widgets(self):
        self.controls_frame = tk.Frame(self.root)
        self.controls_frame.pack(side=tk.RIGHT, padx=10)

        self.add_label_entry("Starting X position", "-200", "x")
        self.add_label_entry("Starting Y position", "200", "y")
        self.add_label_entry("Starting angle", "0", "angle")
        self.add_label_entry("Nesting", "3", "nesting")
        self.add_label_entry("Line size", "5", "length")

        tk.Button(self.controls_frame, text="Draw first", bg="lightgreen", command=self.draw_first).pack(pady=2)
        tk.Button(self.controls_frame, text="Draw second", bg="lightgreen", command=self.draw_second).pack(pady=2)
        tk.Button(self.controls_frame, text="Draw third", bg="lightgreen", command=self.draw_third).pack(pady=2)
        tk.Button(self.controls_frame, text="Draw fourth", bg="lightgreen", command=self.draw_fourth).pack(pady=2)

        tk.Label(self.controls_frame, text="Custom").pack()
        self.add_label_entry("Axiom", "", "axiom")
        self.add_label_entry("Rules (F=F+F,...)", "", "rules")
        self.add_label_entry("Angle", "", "custom_angle")

        tk.Button(self.controls_frame, text="Draw custom", bg="lightgreen", command=self.draw_custom).pack(pady=4)
        tk.Button(self.controls_frame, text="Clear canvas", bg="tomato", command=self.lsystem.clear).pack(pady=4)

    def add_label_entry(self, label, default, attr):
        tk.Label(self.controls_frame, text=label).pack()
        entry = tk.Entry(self.controls_frame)
        entry.insert(0, default)
        entry.pack()
        setattr(self, f"{attr}_entry", entry)

    def get_common_inputs(self):
        x = int(self.x_entry.get())
        y = int(self.y_entry.get())
        angle = float(self.angle_entry.get())
        nesting = int(self.nesting_entry.get())
        length = int(self.length_entry.get())
        return x, y, angle, nesting, length

    def draw_preset(self, axiom, rules, angle_deg):
        x, y, heading, nesting, length = self.get_common_inputs()
        self.lsystem.clear()
        self.lsystem.setup_position(x, y, heading)
        result = self.lsystem.apply_rules(axiom, rules, nesting)
        self.lsystem.draw(result, angle_deg, length)
        self.screen.update()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def draw_first(self):
        self.draw_preset("F+F+F+F", {"F": "F+F-F-FF+F+F-F"}, 90)

    def draw_second(self):
        self.draw_preset("F++F++F", {"F": "F+F--F+F"}, 60)

    def draw_third(self):
        self.draw_preset("F", {"F": "F[+F]F[-F]F"}, math.degrees(math.pi / 7))

    def draw_fourth(self):
        self.draw_preset("F", {"F": "FF+[+F-F-F]-[-F+F+F]"}, math.degrees(math.pi / 8))

    def draw_custom(self):
        axiom = self.axiom_entry.get()
        raw_rules = self.rules_entry.get()
        angle = float(self.custom_angle_entry.get())
        rules = {}
        for part in raw_rules.split(','):
            if '=' in part:
                k, v = part.split('=')
                rules[k.strip()] = v.strip()
        self.draw_preset(axiom, rules, angle)
