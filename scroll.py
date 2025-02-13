import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedTk

class MatrixApp:
    def __init__(self, root):
        self.root = root
        root.title("Matrix App")
        
        # Frame para ingresar número de filas y columnas
        input_frame = ttk.Frame(root, padding="10")
        input_frame.pack(fill="x", expand=True)
        
        ttk.Label(input_frame, text="Filas:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_rows = ttk.Entry(input_frame, width=5)
        self.entry_rows.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Columnas:").grid(row=0, column=2, padx=5, pady=5)
        self.entry_cols = ttk.Entry(input_frame, width=5)
        self.entry_cols.grid(row=0, column=3, padx=5, pady=5)
        
        generate_button = ttk.Button(input_frame, text="Generar Matriz", command=self.generate_matrix)
        generate_button.grid(row=0, column=4, padx=5, pady=5)
        
        # Frame para la matriz y sus entradas
        self.matrix_frame = ttk.Frame(root, padding="10")
        self.matrix_frame.pack()
        
        # Frame para los botones de operaciones
        operations_frame = ttk.Frame(root, padding="10")
        operations_frame.pack()
        
        self.submit_button = ttk.Button(operations_frame, text="Mostrar Matriz", state="disabled", command=self.show_matrix)
        self.submit_button.grid(row=0, column=0, padx=5, pady=5)
        
        self.criteria_button = ttk.Button(operations_frame, text="Criterio", state="disabled", command=self.calculate_criteria)
        self.criteria_button.grid(row=0, column=1, padx=5, pady=5)
        
        self.max_button = ttk.Button(operations_frame, text="Máxima Posibilidad", state="disabled", command=self.calculate_max_possibility)
        self.max_button.grid(row=0, column=2, padx=5, pady=5)
        
        self.lament_button = ttk.Button(operations_frame, text="Lamentaciones Mínimas", state="disabled", command=self.calculate_lamentaciones_minimas)
        self.lament_button.grid(row=0, column=3, padx=5, pady=5)
        
        self.varianza_button = ttk.Button(operations_frame, text="Mínima Varianza", state="disabled", command=self.calculate_minima_varianza)
        self.varianza_button.grid(row=0, column=4, padx=5, pady=5)
        
        self.resumen_button = ttk.Button(operations_frame, text="Cuadro Resumen", state="disabled", command=self.calculate_cuadro_resumen)
        self.resumen_button.grid(row=0, column=5, padx=5, pady=5)
        
        self.min_possibility_button = ttk.Button(operations_frame, text="Mínima Posibilidad", state="disabled", command=self.calculate_minima_possibility)
        self.min_possibility_button.grid(row=0, column=6, padx=5, pady=5)
        
        self.resumen_min_button = ttk.Button(operations_frame, text="Cuadro Resumen Mínimo", state="disabled", command=self.calculate_cuadro_resumen_minimo)
        self.resumen_min_button.grid(row=0, column=7, padx=5, pady=5)
        
        # Inicialización de listas de entradas
        self.col_entries = []
        self.row_entries = []
        self.entries = []
        self.prob_entries = []

    def create_scrollable_treeview(self, parent, **kwargs):
        """
        Crea un contenedor en el 'parent' con un Treeview y barras de desplazamiento vertical y horizontal.
        Devuelve el Treeview.
        """
        container = ttk.Frame(parent)
        container.pack(expand=True, fill="both")
        vsb = ttk.Scrollbar(container, orient="vertical")
        hsb = ttk.Scrollbar(container, orient="horizontal")
        tree = ttk.Treeview(container, yscrollcommand=vsb.set, xscrollcommand=hsb.set, **kwargs)
        vsb.config(command=tree.yview)
        hsb.config(command=tree.xview)
        tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        return tree

    def generate_matrix(self):
        try:
            self.rows = int(self.entry_rows.get())
            self.cols = int(self.entry_cols.get())
            if self.rows <= 0 or self.cols <= 0:
                raise ValueError

            # Limpiar contenido anterior del frame
            for widget in self.matrix_frame.winfo_children():
                widget.destroy()

            self.col_entries = []
            self.row_entries = []

            # Títulos de columnas
            ttk.Label(self.matrix_frame, text="Títulos de Columnas:", font=("Arial", 10, "bold"))\
                .grid(row=0, column=1, columnspan=self.cols, pady=5)
            for j in range(self.cols):
                entry = ttk.Entry(self.matrix_frame, width=10, font=("Arial", 10, "bold"))
                entry.grid(row=1, column=j+1, padx=2, pady=2)
                self.col_entries.append(entry)

            # Títulos de filas
            ttk.Label(self.matrix_frame, text="Títulos de Filas:", font=("Arial", 10, "bold"))\
                .grid(row=2, column=0, rowspan=self.rows, padx=5, pady=5)
            for i in range(self.rows):
                entry = ttk.Entry(self.matrix_frame, width=10, font=("Arial", 10, "bold"))
                entry.grid(row=i+3, column=0, padx=2, pady=2)
                self.row_entries.append(entry)

            # Entradas para la matriz de valores
            self.entries = []
            for i in range(self.rows):
                row_entries = []
                for j in range(self.cols):
                    entry = ttk.Entry(self.matrix_frame, width=10)
                    entry.grid(row=i+3, column=j+1, padx=2, pady=2)
                    row_entries.append(entry)
                self.entries.append(row_entries)

            # Fila de probabilidades (pesos) para cada columna
            ttk.Label(self.matrix_frame, text="Probabilidades:", font=("Arial", 10, "bold"))\
                .grid(row=self.rows+3, column=0, pady=5)
            self.prob_entries = []
            for j in range(self.cols):
                entry = ttk.Entry(self.matrix_frame, width=10, font=("Arial", 10, "bold"))
                entry.grid(row=self.rows+3, column=j+1, padx=2, pady=2)
                self.prob_entries.append(entry)

            # Habilitar los botones de operaciones
            self.submit_button["state"] = "normal"
            self.criteria_button["state"] = "normal"
            self.max_button["state"] = "normal"
            self.lament_button["state"] = "normal"
            self.varianza_button["state"] = "normal"
            self.resumen_button["state"] = "normal"
            self.min_possibility_button["state"] = "normal"
            self.resumen_min_button["state"] = "normal"

        except ValueError:
            messagebox.showerror("Error", "Ingrese valores válidos para filas y columnas.")

    def show_matrix(self):
        col_titles = [entry.get() for entry in self.col_entries]
        row_titles = [entry.get() for entry in self.row_entries]

        matrix = []
        for row_entries in self.entries:
            row = []
            for entry in row_entries:
                value = entry.get()
                try:
                    num_value = float(value) if '.' in value else int(value)
                    row.append(num_value)
                except ValueError:
                    messagebox.showerror("Error", "Todos los valores de la matriz deben ser numéricos.")
                    return
            matrix.append(row)

        probabilities = []
        for entry in self.prob_entries:
            value = entry.get()
            try:
                num_value = float(value) if '.' in value else int(value)
                probabilities.append(num_value)
            except ValueError:
                messagebox.showerror("Error", "Los valores de probabilidades deben ser numéricos.")
                return

        table_window = tk.Toplevel(self.root)
        table_window.title("Visualización de Matriz")

        style = ttk.Style(table_window)
        style.configure("Treeview", rowheight=30, font=("Arial", 12), borderwidth=2, relief="solid")
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"),
                        background="white", foreground="black", borderwidth=2, relief="solid")
        # Se crea el tree con scrollbars usando el método auxiliar
        tree = self.create_scrollable_treeview(table_window, columns=["Fila"] + col_titles, show="headings", style="Treeview")
        tree.heading("Fila", text="Fila", anchor="center")
        tree.column("Fila", width=120, anchor="center")
        for col in col_titles:
            tree.heading(col, text=col, anchor="center")
            tree.column(col, width=120, anchor="center")

        for i in range(self.rows):
            tree.insert("", "end", values=(row_titles[i],) +
                        tuple(self.format_number(n) for n in [float(x.get()) if '.' in x.get() else int(x.get()) for x in self.entries[i]]))
        tree.insert("", "end", values=("Probabilidades",) +
                    tuple(self.format_number(p) for p in probabilities), tags=("bold",))
        tree.tag_configure("bold", font=("Arial", 12, "bold"))

    def calculate_criteria(self):
        row_titles = [entry.get() for entry in self.row_entries]

        matrix = []
        for row_entries in self.entries:
            row = []
            for entry in row_entries:
                value = entry.get()
                try:
                    num_value = float(value) if '.' in value else int(value)
                    row.append(num_value)
                except ValueError:
                    messagebox.showerror("Error", "Todos los valores de la matriz deben ser numéricos.")
                    return
            matrix.append(row)

        probabilities = []
        for entry in self.prob_entries:
            value = entry.get()
            try:
                num_value = float(value) if '.' in value else int(value)
                probabilities.append(num_value)
            except ValueError:
                messagebox.showerror("Error", "Los valores de probabilidades deben ser numéricos.")
                return

        if len(probabilities) != self.cols:
            messagebox.showerror("Error", "La cantidad de probabilidades debe coincidir con el número de columnas.")
            return

        criteria_results = []
        for i in range(self.rows):
            weighted_sum = 0
            for j in range(self.cols):
                weighted_sum += matrix[i][j] * probabilities[j]
            criteria_results.append(weighted_sum)

        result_window = tk.Toplevel(self.root)
        result_window.title("Resultado del Criterio")

        style = ttk.Style(result_window)
        style.configure("Treeview", rowheight=30, font=("Arial", 12), borderwidth=2, relief="solid")
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"),
                        background="white", foreground="black", borderwidth=2, relief="solid")
        tree = self.create_scrollable_treeview(result_window, columns=("Alternativa", "Criterio"), show="headings", style="Treeview")
        tree.heading("Alternativa", text="Alternativa", anchor="center")
        tree.heading("Criterio", text="Criterio", anchor="center")
        tree.column("Alternativa", width=150, anchor="center")
        tree.column("Criterio", width=150, anchor="center")

        for i in range(self.rows):
            alt = self.row_entries[i].get()
            criterio_val = self.format_number(criteria_results[i])
            tree.insert("", "end", values=(alt, criterio_val))

    def calculate_max_possibility(self):
        row_titles = [entry.get() for entry in self.row_entries]

        matrix = []
        for row_entries in self.entries:
            row = []
            for entry in row_entries:
                value = entry.get()
                try:
                    num_value = float(value) if '.' in value else int(value)
                    row.append(num_value)
                except ValueError:
                    messagebox.showerror("Error", "Todos los valores de la matriz deben ser numéricos.")
                    return
            matrix.append(row)

        probabilities = []
        for entry in self.prob_entries:
            value = entry.get()
            try:
                num_value = float(value) if '.' in value else int(value)
                probabilities.append(num_value)
            except ValueError:
                messagebox.showerror("Error", "Los valores de probabilidades deben ser numéricos.")
                return

        if len(probabilities) != self.cols:
            messagebox.showerror("Error", "La cantidad de probabilidades debe coincidir con el número de columnas.")
            return

        max_prob = max(probabilities)
        max_prob_index = probabilities.index(max_prob)

        max_value = None
        max_row_index = None
        for i in range(self.rows):
            val = matrix[i][max_prob_index]
            if max_value is None or val > max_value:
                max_value = val
                max_row_index = i

        result_window = tk.Toplevel(self.root)
        result_window.title("Máxima Posibilidad")
        result_label = ttk.Label(result_window, text=f"{self.row_entries[max_row_index].get()} = {self.format_number(max_value)}",
                                 font=("Arial", 14))
        result_label.pack(padx=20, pady=20)

    def calculate_lamentaciones_minimas(self):
        matrix = []
        for row_entries in self.entries:
            row = []
            for entry in row_entries:
                value = entry.get()
                try:
                    num_value = float(value) if '.' in value else int(value)
                    row.append(num_value)
                except ValueError:
                    messagebox.showerror("Error", "Todos los valores de la matriz deben ser numéricos.")
                    return
            matrix.append(row)

        probabilities = []
        for entry in self.prob_entries:
            value = entry.get()
            try:
                num_value = float(value) if '.' in value else int(value)
                probabilities.append(num_value)
            except ValueError:
                messagebox.showerror("Error", "Los valores de probabilidades deben ser numéricos.")
                return

        if len(probabilities) != self.cols:
            messagebox.showerror("Error", "La cantidad de probabilidades debe coincidir con el número de columnas.")
            return

        row_titles = [entry.get() for entry in self.row_entries]
        col_titles = [entry.get() for entry in self.col_entries]

        max_row = []
        for j in range(self.cols):
            col_values = [matrix[i][j] for i in range(self.rows)]
            max_val = max(col_values)
            max_row.append(max_val)

        diff_matrix = []
        for i in range(self.rows):
            diff_row = []
            for j in range(self.cols):
                diff_row.append(max_row[j] - matrix[i][j])
            diff_matrix.append(diff_row)

        final_results = []
        for i in range(self.rows):
            weighted_sum = 0
            for j in range(self.cols):
                weighted_sum += probabilities[j] * diff_matrix[i][j]
            final_results.append(weighted_sum)

        result_window = tk.Toplevel(self.root)
        result_window.title("Lamentaciones Mínimas")

        style = ttk.Style(result_window)
        style.configure("Treeview", rowheight=30, font=("Arial", 12), borderwidth=2, relief="solid")
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"),
                        background="white", foreground="black", borderwidth=2, relief="solid")

        # Para el primer treeview con la matriz de diferencias
        frame1 = ttk.Frame(result_window, padding="10")
        frame1.pack(fill="both", expand=True)
        label1 = ttk.Label(frame1, text="Matriz de Lamentaciones Mínimas (diferencias)", font=("Arial", 12, "bold"))
        label1.pack()
        tree1 = self.create_scrollable_treeview(frame1, columns=["Alternativa"] + col_titles, show="headings")
        tree1.heading("Alternativa", text="Alternativa", anchor="center")
        tree1.column("Alternativa", width=120, anchor="center")
        for col in col_titles:
            tree1.heading(col, text=col, anchor="center")
            tree1.column(col, width=120, anchor="center")
        for i in range(self.rows):
            tree1.insert("", "end", values=(row_titles[i],) + tuple(self.format_number(v) for v in diff_matrix[i]))
        tree1.insert("", "end", values=("MAX",) + tuple(self.format_number(v) for v in max_row), tags=("bold",))
        tree1.tag_configure("bold", font=("Arial", 12, "bold"))

        # Para el segundo treeview con los resultados finales
        frame2 = ttk.Frame(result_window, padding="10")
        frame2.pack(fill="both", expand=True)
        label2 = ttk.Label(frame2, text="Resultados Finales", font=("Arial", 12, "bold"))
        label2.pack()
        tree2 = self.create_scrollable_treeview(frame2, columns=("Alternativa", "Cálculo"), show="headings")
        tree2.heading("Alternativa", text="Alternativa", anchor="center")
        tree2.column("Alternativa", width=150, anchor="center")
        tree2.heading("Cálculo", text="Cálculo", anchor="center")
        tree2.column("Cálculo", width=250, anchor="center")
        for i in range(self.rows):
            calc_str = "(" + " + ".join(f"{self.format_number(probabilities[j])}*{self.format_number(diff_matrix[i][j])}" for j in range(self.cols)) + ")"
            calc_value = self.format_number(final_results[i])
            tree2.insert("", "end", values=(row_titles[i], f"{calc_str} = {calc_value}"))

    def calculate_minima_varianza(self):
        matrix = []
        for row_entries in self.entries:
            row = []
            for entry in row_entries:
                value = entry.get()
                try:
                    num_value = float(value) if '.' in value else int(value)
                    row.append(num_value)
                except ValueError:
                    messagebox.showerror("Error", "Todos los valores de la matriz deben ser numéricos.")
                    return
            matrix.append(row)
        probabilities = []
        for entry in self.prob_entries:
            value = entry.get()
            try:
                num_value = float(value) if '.' in value else int(value)
                probabilities.append(num_value)
            except ValueError:
                messagebox.showerror("Error", "Los valores de probabilidades deben ser numéricos.")
                return
        if len(probabilities) != self.cols:
            messagebox.showerror("Error", "La cantidad de probabilidades debe coincidir con el número de columnas.")
            return
        row_titles = [entry.get() for entry in self.row_entries]
        criteria_list = []
        for i in range(self.rows):
            c = 0
            for j in range(self.cols):
                c += probabilities[j] * matrix[i][j]
            criteria_list.append(c)
        varianza_list = []
        for i in range(self.rows):
            v = 0
            for j in range(self.cols):
                diff = matrix[i][j] - criteria_list[i]
                v += probabilities[j] * (diff ** 2)
            varianza_list.append(v)
        result_window = tk.Toplevel(self.root)
        result_window.title("Mínima Varianza")
        style = ttk.Style(result_window)
        style.configure("Treeview", rowheight=30, font=("Arial", 12), borderwidth=2, relief="solid")
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"),
                        background="white", foreground="black", borderwidth=2, relief="solid")

        frame1 = ttk.Frame(result_window, padding="10")
        frame1.pack(fill="both", expand=True)
        label1 = ttk.Label(frame1, text="Tabla de Criterio", font=("Arial", 12, "bold"))
        label1.pack()
        tree1 = self.create_scrollable_treeview(frame1, columns=("Alternativa", "Criterio"), show="headings")
        tree1.heading("Alternativa", text="Alternativa", anchor="center")
        tree1.column("Alternativa", width=150, anchor="center")
        tree1.heading("Criterio", text="Criterio", anchor="center")
        tree1.column("Criterio", width=150, anchor="center")
        for i in range(self.rows):
            tree1.insert("", "end", values=(row_titles[i], self.format_number(criteria_list[i])))

        frame2 = ttk.Frame(result_window, padding="10")
        frame2.pack(fill="both", expand=True)
        label2 = ttk.Label(frame2, text="Tabla de Mínima Varianza", font=("Arial", 12, "bold"))
        label2.pack()
        tree2 = self.create_scrollable_treeview(frame2, columns=("Alternativa", "Cálculo"), show="headings")
        tree2.heading("Alternativa", text="Alternativa", anchor="center")
        tree2.column("Alternativa", width=150, anchor="center")
        tree2.heading("Cálculo", text="Cálculo", anchor="center")
        tree2.column("Cálculo", width=400, anchor="center")
        for i in range(self.rows):
            terms = []
            for j in range(self.cols):
                term = f"{self.format_number(probabilities[j])}*({self.format_number(matrix[i][j])} - ({self.format_number(criteria_list[i])}))^2"
                terms.append(term)
            calc_str = " + ".join(terms)
            final_str = f"{calc_str} = {self.format_number(varianza_list[i])}"
            tree2.insert("", "end", values=(row_titles[i], final_str))

    def calculate_minima_possibility(self):
        """
        Funcionalidad:
          - Busca la probabilidad mínima.
          - Se posiciona en la columna asociada a esa probabilidad.
          - Busca en esa columna el valor mínimo de la matriz.
          - Muestra el nombre de la fila (alternativa) y el valor mínimo.
        """
        row_titles = [entry.get() for entry in self.row_entries]

        matrix = []
        for row_entries in self.entries:
            row = []
            for entry in row_entries:
                value = entry.get()
                try:
                    num_value = float(value) if '.' in value else int(value)
                    row.append(num_value)
                except ValueError:
                    messagebox.showerror("Error", "Todos los valores de la matriz deben ser numéricos.")
                    return
            matrix.append(row)

        probabilities = []
        for entry in self.prob_entries:
            value = entry.get()
            try:
                num_value = float(value) if '.' in value else int(value)
                probabilities.append(num_value)
            except ValueError:
                messagebox.showerror("Error", "Los valores de probabilidades deben ser numéricos.")
                return

        if len(probabilities) != self.cols:
            messagebox.showerror("Error", "La cantidad de probabilidades debe coincidir con el número de columnas.")
            return

        min_prob = min(probabilities)
        min_prob_index = probabilities.index(min_prob)

        min_value = None
        min_row_index = None
        for i in range(self.rows):
            val = matrix[i][min_prob_index]
            if min_value is None or val < min_value:
                min_value = val
                min_row_index = i

        result_window = tk.Toplevel(self.root)
        result_window.title("Mínima Posibilidad")
        result_label = ttk.Label(result_window, 
                                 text=f"{self.row_entries[min_row_index].get()} = {self.format_number(min_value)}",
                                 font=("Arial", 14))
        result_label.pack(padx=20, pady=20)

    def calculate_cuadro_resumen(self):
        matrix = []
        for row_entries in self.entries:
            row = []
            for entry in row_entries:
                try:
                    val_str = entry.get()
                    num_value = float(val_str) if '.' in val_str else int(val_str)
                    row.append(num_value)
                except:
                    messagebox.showerror("Error", "Todos los valores de la matriz deben ser numéricos.")
                    return
            matrix.append(row)
        probabilities = []
        for entry in self.prob_entries:
            try:
                val_str = entry.get()
                num_value = float(val_str) if '.' in val_str else int(val_str)
                probabilities.append(num_value)
            except:
                messagebox.showerror("Error", "Los valores de probabilidades deben ser numéricos.")
                return
        if len(probabilities) != self.cols:
            messagebox.showerror("Error", "La cantidad de probabilidades debe coincidir con el número de columnas.")
            return
        row_titles = [entry.get() for entry in self.row_entries]
        C1 = []
        for i in range(self.rows):
            c = sum(matrix[i][j] * probabilities[j] for j in range(self.cols))
            C1.append(c)
        max_prob_index = probabilities.index(max(probabilities))
        C2_values = [matrix[i][max_prob_index] for i in range(self.rows)]
        max_C2 = max(C2_values)
        ranking_C2 = []
        for i in range(self.rows):
            if C2_values[i] == max_C2:
                ranking_C2.append(1)
            else:
                ranking_C2.append("-")
        max_row = []
        for j in range(self.cols):
            max_j = max(matrix[i][j] for i in range(self.rows))
            max_row.append(max_j)
        C3 = []
        for i in range(self.rows):
            lam = sum(probabilities[j] * (max_row[j] - matrix[i][j]) for j in range(self.cols))
            C3.append(lam)
        C4 = []
        for i in range(self.rows):
            var = sum(probabilities[j] * ((matrix[i][j] - C1[i])**2) for j in range(self.cols))
            C4.append(var)
        ranking_C1 = [0] * self.rows
        sorted_indices = sorted(range(self.rows), key=lambda i: C1[i], reverse=True)
        rank = 1
        for idx in sorted_indices:
            ranking_C1[idx] = rank
            rank += 1
        ranking_C3 = [0] * self.rows
        sorted_indices = sorted(range(self.rows), key=lambda i: C3[i])
        rank = 1
        for idx in sorted_indices:
            ranking_C3[idx] = rank
            rank += 1
        ranking_C4 = [0] * self.rows
        sorted_indices = sorted(range(self.rows), key=lambda i: C4[i])
        rank = 1
        for idx in sorted_indices:
            ranking_C4[idx] = rank
            rank += 1
        summary = []
        for i in range(self.rows):
            summary.append([row_titles[i], ranking_C1[i], ranking_C2[i], ranking_C3[i], ranking_C4[i]])
        ones_count = []
        for i in range(self.rows):
            count = 0
            if ranking_C1[i] == 1:
                count += 1
            if ranking_C2[i] == 1:
                count += 1
            if ranking_C3[i] == 1:
                count += 1
            if ranking_C4[i] == 1:
                count += 1
            ones_count.append(count)
        max_ones = max(ones_count)
        best_indices = [i for i, cnt in enumerate(ones_count) if cnt == max_ones]
        best_alternative = row_titles[best_indices[0]] if best_indices else "Ninguna"
        result_window = tk.Toplevel(self.root)
        result_window.title("Cuadro Resumen")
        style = ttk.Style(result_window)
        style.configure("Treeview", rowheight=30, font=("Arial", 12), borderwidth=2, relief="solid")
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"),
                        background="white", foreground="black", borderwidth=2, relief="solid")
        tree = self.create_scrollable_treeview(result_window, columns=("Alternativa", "C1", "C2", "C3", "C4"), show="headings")
        tree.heading("Alternativa", text="Alternativa", anchor="center")
        tree.column("Alternativa", width=150, anchor="center")
        tree.heading("C1", text="C1", anchor="center")
        tree.column("C1", width=100, anchor="center")
        tree.heading("C2", text="C2", anchor="center")
        tree.column("C2", width=100, anchor="center")
        tree.heading("C3", text="C3", anchor="center")
        tree.column("C3", width=100, anchor="center")
        tree.heading("C4", text="C4", anchor="center")
        tree.column("C4", width=100, anchor="center")
        for row in summary:
            tree.insert("", "end", values=tuple(row))
        label_best = ttk.Label(result_window, text=f"La mejor opción es: {best_alternative}", font=("Arial", 14, "bold"))
        label_best.pack(padx=10, pady=10)

    def calculate_cuadro_resumen_minimo(self):
        """
        Funcionalidad:
          - Calcula los cuatro criterios (C1, C2, C3, C4) para cada alternativa.
          - Para C1, C3 y C4 se asigna un ranking en orden ascendente (el menor valor obtiene 1).
          - Para C2 se toma el valor de la columna asociada a la menor probabilidad y se asigna 1
            únicamente a la alternativa que tenga el valor mínimo; al resto se les asigna "-".
          - Se arma una tabla resumen con los rangos y se determina la mejor opción,
            tomando como criterio principal la mayor cantidad de “1” (y en caso de empate, se usa un criterio de desempate).
        """
        matrix = []
        for row_entries in self.entries:
            row = []
            for entry in row_entries:
                try:
                    val_str = entry.get()
                    num_value = float(val_str) if '.' in val_str else int(val_str)
                    row.append(num_value)
                except:
                    messagebox.showerror("Error", "Todos los valores de la matriz deben ser numéricos.")
                    return
            matrix.append(row)
        probabilities = []
        for entry in self.prob_entries:
            try:
                val_str = entry.get()
                num_value = float(val_str) if '.' in val_str else int(val_str)
                probabilities.append(num_value)
            except:
                messagebox.showerror("Error", "Los valores de probabilidades deben ser numéricos.")
                return
        if len(probabilities) != self.cols:
            messagebox.showerror("Error", "La cantidad de probabilidades debe coincidir con el número de columnas.")
            return
        row_titles = [entry.get() for entry in self.row_entries]

        # C1: Suma ponderada
        C1 = []
        for i in range(self.rows):
            c = sum(matrix[i][j] * probabilities[j] for j in range(self.cols))
            C1.append(c)
        ranking_C1 = [0] * self.rows
        sorted_indices = sorted(range(self.rows), key=lambda i: C1[i])
        rank = 1
        for idx in sorted_indices:
            ranking_C1[idx] = rank
            rank += 1

        # C2: Usar la columna asociada a la menor probabilidad
        min_prob = min(probabilities)
        min_prob_index = probabilities.index(min_prob)
        C2 = [matrix[i][min_prob_index] for i in range(self.rows)]
        min_C2 = min(C2)
        ranking_C2 = []
        for i in range(self.rows):
            if C2[i] == min_C2:
                ranking_C2.append(1)
            else:
                ranking_C2.append("-")
        
        # C3: Lamentaciones mínimas
        max_row = []
        for j in range(self.cols):
            max_j = max(matrix[i][j] for i in range(self.rows))
            max_row.append(max_j)
        C3 = []
        for i in range(self.rows):
            lam = sum(probabilities[j] * (max_row[j] - matrix[i][j]) for j in range(self.cols))
            C3.append(lam)
        ranking_C3 = [0] * self.rows
        sorted_indices = sorted(range(self.rows), key=lambda i: C3[i])
        rank = 1
        for idx in sorted_indices:
            ranking_C3[idx] = rank
            rank += 1

        # C4: Mínima varianza
        C4 = []
        for i in range(self.rows):
            var = sum(probabilities[j] * ((matrix[i][j] - C1[i])**2) for j in range(self.cols))
            C4.append(var)
        ranking_C4 = [0] * self.rows
        sorted_indices = sorted(range(self.rows), key=lambda i: C4[i])
        rank = 1
        for idx in sorted_indices:
            ranking_C4[idx] = rank
            rank += 1

        summary = []
        for i in range(self.rows):
            summary.append([row_titles[i], ranking_C1[i], ranking_C2[i], ranking_C3[i], ranking_C4[i]])

        ones_count = []
        for i in range(self.rows):
            count = 0
            if ranking_C1[i] == 1:
                count += 1
            if ranking_C2[i] == 1:
                count += 1
            if ranking_C3[i] == 1:
                count += 1
            if ranking_C4[i] == 1:
                count += 1
            ones_count.append(count)
        max_ones = max(ones_count)
        best_indices = [i for i, cnt in enumerate(ones_count) if cnt == max_ones]
        if len(best_indices) > 1:
            total_ranks = []
            for i in best_indices:
                s = 0
                s += ranking_C1[i] if isinstance(ranking_C1[i], int) else 999
                s += ranking_C2[i] if isinstance(ranking_C2[i], int) else 999
                s += ranking_C3[i] if isinstance(ranking_C3[i], int) else 999
                s += ranking_C4[i] if isinstance(ranking_C4[i], int) else 999
                total_ranks.append(s)
            best_index = best_indices[total_ranks.index(min(total_ranks))]
        else:
            best_index = best_indices[0]
        best_alternative = row_titles[best_index]

        result_window = tk.Toplevel(self.root)
        result_window.title("Cuadro Resumen Mínimo")
        style = ttk.Style(result_window)
        style.configure("Treeview", rowheight=30, font=("Arial", 12), borderwidth=2, relief="solid")
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"),
                        background="white", foreground="black", borderwidth=2, relief="solid")
        tree = self.create_scrollable_treeview(result_window, columns=("Alternativa", "C1", "C2", "C3", "C4"), show="headings")
        tree.heading("Alternativa", text="Alternativa", anchor="center")
        tree.column("Alternativa", width=150, anchor="center")
        tree.heading("C1", text="C1", anchor="center")
        tree.column("C1", width=100, anchor="center")
        tree.heading("C2", text="C2", anchor="center")
        tree.column("C2", width=100, anchor="center")
        tree.heading("C3", text="C3", anchor="center")
        tree.column("C3", width=100, anchor="center")
        tree.heading("C4", text="C4", anchor="center")
        tree.column("C4", width=100, anchor="center")
        for row in summary:
            tree.insert("", "end", values=tuple(row))
        label_best = ttk.Label(result_window, text=f"La mejor opción es: {best_alternative}", font=("Arial", 14, "bold"))
        label_best.pack(padx=10, pady=10)

    def format_number(self, num):
        """Devuelve el número sin decimales si es entero, o con decimales si es flotante."""
        return int(num) if num == int(num) else num

if __name__ == "__main__":
    root = ThemedTk(theme="arc")
    app = MatrixApp(root)
    root.mainloop()
