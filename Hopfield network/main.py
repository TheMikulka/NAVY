import numpy as np
import tkinter as tk

class HopfieldNetwork:
    def __init__(self, size):
        self.size = size
        self.weights = np.zeros((size, size))
        
    def train(self, patterns):
        self.weights = np.zeros((self.size, self.size))
        for pattern in patterns:
            pattern = pattern.reshape(-1, 1)
            self.weights += pattern @ pattern.T
        np.fill_diagonal(self.weights, 0)
    
    def recover_sync(self, pattern):
        last_pattern = None
        max_iter = 1000
        while(not np.array_equal(pattern, last_pattern) and max_iter != 0):
            last_pattern = np.copy(pattern)
            pattern = np.sign(self.weights @ pattern)
            max_iter -= 1
        return pattern
    
    def recover_async(self, pattern, max_iter=100):
        for _ in range(max_iter):
            for i in range(self.size):
                activation = np.sign(np.dot(self.weights[:,i], pattern))
                pattern[i] = activation
        return pattern

class HopfieldGUI:
    def __init__(self, root, grid_size=5):
        self.root = root
        self.grid_size = grid_size
        self.size_block = 20
        self.network = HopfieldNetwork(grid_size**2)
        self.patterns = []
        self.current_pattern = np.ones((self.grid_size**2,)) * -1
        self.max_patterns = np.floor(self.grid_size**2 / (2* np.log2(self.grid_size**2)))
        
        self.canvas = tk.Canvas(root, width=grid_size*self.size_block, height=grid_size*self.size_block)
        self.canvas.grid(row=1, column=1)
        self.canvas.bind("<Button-1>", self.toggle_cell)
        self.draw_grid()
        
        btn_frame = tk.Frame(root)
        btn_frame.grid(row=1, column=2)
        
        tk.Button(btn_frame, text="Save pattern", command=self.save_pattern).pack(side=tk.TOP)
        tk.Button(btn_frame, text="Repair pattern Sync", command=self.recover_sync).pack(side=tk.TOP)
        tk.Button(btn_frame, text="Repair pattern Async", command=self.recover_async).pack(side=tk.TOP)
        tk.Button(btn_frame, text="Show saved patterns", command=self.show_saved_patterns).pack(side=tk.TOP)
        tk.Button(btn_frame, text="Clear grid", command=self.clear_grid).pack(side=tk.TOP)
        tk.Label(btn_frame, text=f"Max recommended saved patterns: {self.max_patterns}").pack(side=tk.TOP)
        
        self.info_label = tk.Label(btn_frame, text="")
        self.info_label.pack(side=tk.TOP)

    def draw_grid(self):
        self.cells = []
        for i in range(self.grid_size):
            row = []
            for j in range(self.grid_size):
                x1, y1 = j * self.size_block, i * self.size_block
                x2, y2 = x1 + self.size_block, y1 + self.size_block
                
                fill_color = "black" if self.current_pattern[i * self.grid_size + j] == 1 else "white"
                rect = self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill_color, outline="black")
                row.append(rect)
            self.cells.append(row)
    
    def toggle_cell(self, event):
        i, j = event.y // self.size_block, event.x // self.size_block
        if 0 <= i < self.grid_size and 0 <= j < self.grid_size:
            index = i * self.grid_size + j
            self.current_pattern[index] *= -1
            new_fill = "black" if self.current_pattern[index] == 1 else "white"
            self.canvas.itemconfig(self.cells[i][j], fill=new_fill)
        
    def save_pattern(self):
        self.patterns.append(self.current_pattern.copy())
        self.info_label.config(text="Pattern saved", fg="green")
        self.info_label.after(1000, lambda: self.info_label.config(text=""))
        self.network.train(self.patterns)

    def recover_sync(self):
        recovered = self.network.recover_sync(self.current_pattern.copy())
        self.update_grid(recovered)

    def recover_async(self):
        recovered = self.network.recover_async(self.current_pattern.copy())
        self.update_grid(recovered)

    def update_grid(self, pattern):
        self.current_pattern = pattern
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                fill_color = "black" if self.current_pattern[i * self.grid_size + j] == 1 else "white"
                self.canvas.itemconfig(self.cells[i][j], fill=fill_color)

    def show_saved_patterns(self):
        if not self.patterns:
            self.info_label.config(text="No saved patterns", fg="red")
            self.info_label.after(1000, lambda: self.info_label.config(text=""))
            return

        top = tk.Toplevel(self.root)
        top.title("Saved patterns")
        
        for idx, pattern in enumerate(self.patterns):
            frame = tk.Frame(top)
            frame.pack(pady=5)
            tk.Label(frame, text=f"Pattern {idx + 1}").pack()

            btn_frame = tk.Frame(frame)
            btn_frame.pack(side="left", padx=5)

            tk.Button(btn_frame, text="Show matrix", command=lambda i=idx: self.show_matrix(i)).pack()
            tk.Button(btn_frame, text="Show matrix without zeros", command=lambda i=idx: self.show_matrix_no_zeros(i)).pack()
            tk.Button(btn_frame, text="Show vector", command=lambda i=idx: self.show_vector(i)).pack()
            tk.Button(btn_frame, text="Show weighted matrix", command=lambda i=idx: self.show_weighted_matrix(i)).pack()
            tk.Button(btn_frame, text="Delete", command=lambda i=idx: self.delete_pattern(i, top), bg="pink").pack()
            
            pattern_canvas = tk.Canvas(frame, width=self.grid_size*self.size_block, height=self.grid_size*self.size_block)
            pattern_canvas.pack()

            for i in range(self.grid_size):
                for j in range(self.grid_size):
                    x1, y1 = j * self.size_block, i * self.size_block
                    x2, y2 = x1 + self.size_block, y1 + self.size_block
                    fill_color = "black" if pattern[i * self.grid_size + j] == 1 else "white"
                    pattern_canvas.create_rectangle(x1, y1, x2, y2, fill=fill_color, outline="black")
    
    def show_matrix(self, index):
        pattern = self.patterns[index].reshape((self.grid_size, self.grid_size))
        self.display_matrix_in_window(pattern, title=f"Matrix of Pattern {index+1}")
    
    def show_matrix_no_zeros(self, index):
        pattern = self.patterns[index].reshape((self.grid_size, self.grid_size))
        pattern = np.where(pattern == 1, "1", " ") 
        self.display_matrix_in_window(pattern, title=f"Matrix without zeros of Pattern {index+1}")
    
    def show_vector(self, index):
        pattern = self.patterns[index]
        self.display_matrix_in_window(pattern.reshape(1, -1), title=f"Vector of Pattern {index+1}")
    
    def show_weighted_matrix(self, index):
        pattern = self.patterns[index].reshape(-1, 1)
        weight_matrix = pattern @ pattern.T
        np.fill_diagonal(weight_matrix, 0)
        self.display_matrix_in_window(weight_matrix, title=f"Weighted Matrix of Pattern {index+1}")

    def display_matrix_in_window(self, matrix, title):
        top = tk.Toplevel(self.root)
        top.title(title)
        text_widget = tk.Text(top, wrap="none")
        text_widget.insert("1.0", "\n".join(["\t".join(map(str, row)) for row in matrix]))
        text_widget.pack(expand=True, fill="both")

    def delete_pattern(self, index, window):
        del self.patterns[index]
        self.network.train(self.patterns)
        window.destroy()
        self.show_saved_patterns()

    def clear_grid(self):
        self.current_pattern.fill(-1)
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                self.canvas.itemconfig(self.cells[i][j], fill="white")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Hopfield")
    app = HopfieldGUI(root)
    root.mainloop()
