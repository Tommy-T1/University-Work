#Tareq Aburajab : 2110025 
#Ammar Zubaidi : 2110227


import tkinter as tk
from tkinter import ttk
import ast
import numpy as np

class MatrixCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Matrix Calculator")

        self.create_widgets()

    def create_widgets(self):
        # Matrix A
        ttk.Label(self.root, text="Matrix A :").grid(row=0, column=0, padx=10, pady=10)
        self.matrix_A_entry = self.create_matrix_entry(1, 0)

        # Matrix B
        ttk.Label(self.root, text="Matrix B :").grid(row=2, column=0, padx=10, pady=10)
        self.matrix_B_entry = self.create_matrix_entry(3, 0)

        # Operation
        ttk.Label(self.root, text="Choose Operation:").grid(row=5, column=0, padx=10, pady=10)
        self.operation_var = tk.StringVar()
        self.operation_var.set("Addition")
        operation_menu = ttk.Combobox(self.root, textvariable=self.operation_var, values=["Addition", "Transposition", "Inversion", "Determinant", "Multiplication"])
        operation_menu.grid(row=5, column=1, padx=10, pady=10)

        # Result
        ttk.Label(self.root, text="Result:").grid(row=7, column=0, padx=10, pady=10)
        self.result_text = tk.Text(self.root, height=5, width=40)
        self.result_text.grid(row=7, column=1, padx=10, pady=10)

        # Calculate Button
        calculate_button = ttk.Button(self.root, text="Calculate", command=self.calculate)
        calculate_button.grid(row=9, column=0, columnspan=2, pady=10)

    def create_matrix_entry(self, row, column):
        matrix_entry = tk.Text(self.root, height=5, width=40)
        matrix_entry.grid(row=row, column=1, padx=10, pady=10)
        return matrix_entry

    def get_matrices(self):
        matrix_A_str = self.matrix_A_entry.get(1.0, tk.END)
        matrix_B_str = self.matrix_B_entry.get(1.0, tk.END)

        try:
            matrix_A = np.array(ast.literal_eval(matrix_A_str))
            matrix_B = np.array(ast.literal_eval(matrix_B_str))
            return matrix_A, matrix_B
        except Exception as e:
            print(f"Error parsing matrices: {e}")
            return None, None

    def calculate(self):
        matrix_A, matrix_B = self.get_matrices()

        if matrix_A is not None and matrix_B is not None:
            operation = self.operation_var.get()

            if operation == "Addition":
                result = np.add(matrix_A, matrix_B)
            elif operation == "Transposition":
                result = {"Matrix A": np.transpose(matrix_A), "Matrix B": np.transpose(matrix_B)}
            elif operation == "Inversion":
                result = {"Matrix A": np.linalg.inv(matrix_A), "Matrix B": np.linalg.inv(matrix_B)}
            elif operation == "Determinant":
                result = {"Matrix A": np.linalg.det(matrix_A), "Matrix B": np.linalg.det(matrix_B)}
            elif operation == "Multiplication":
                result = np.dot(matrix_A, matrix_B)
            else:
                result = "Invalid operation"

            self.display_result(result)

    def display_result(self, result):
        self.result_text.delete(1.0, tk.END)

        if isinstance(result, np.ndarray):
            self.result_text.insert(tk.END, str(result))
        elif isinstance(result, dict):
            for key, value in result.items():
                self.result_text.insert(tk.END, f"{key}:\n{value}\n\n")
        else:
            self.result_text.insert(tk.END, result)


if __name__ == "__main__":
    root = tk.Tk()
    app = MatrixCalculatorApp(root)
    root.mainloop()
