import tkinter as tk
from tkinter import ttk, messagebox

class MatrixApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Generador de Matriz")

        # Entrada para el número de filas y columnas
        tk.Label(root, text="Filas:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_rows = tk.Entry(root, width=5)
        self.entry_rows.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(root, text="Columnas:").grid(row=0, column=2, padx=5, pady=5)
        self.entry_cols = tk.Entry(root, width=5)
        self.entry_cols.grid(row=0, column=3, padx=5, pady=5)

        self.generate_button = tk.Button(root, text="Generar Matriz", command=self.generate_matrix)
        self.generate_button.grid(row=0, column=4, padx=10, pady=10)

        # Frame para la matriz y sus entradas
        self.matrix_frame = tk.Frame(root)
        self.matrix_frame.grid(row=2, column=0, columnspan=5, padx=5, pady=5)

        # Botón para mostrar la matriz
        self.submit_button = tk.Button(root, text="Mostrar Matriz", command=self.show_matrix, state="disabled")
        self.submit_button.grid(row=3, column=0, columnspan=5, pady=10)

        # Botón para calcular el criterio (suma ponderada)
        self.criteria_button = tk.Button(root, text="Criterio valor esperado", command=self.calculate_criteria, state="disabled")
        self.criteria_button.grid(row=4, column=0, columnspan=5, pady=10)

        # Botón para calcular la máxima posibilidad
        self.max_button = tk.Button(root, text="C. Máxima Posibilidad", command=self.calculate_max_possibility, state="disabled")
        self.max_button.grid(row=5, column=0, columnspan=5, pady=10)

        # Botón para calcular las lamentaciones mínimas
        self.lament_button = tk.Button(root, text="C. Lamentaciones Mínimas", command=self.calculate_lamentaciones_minimas, state="disabled")
        self.lament_button.grid(row=6, column=0, columnspan=5, pady=10)

        # Botón para calcular la mínima varianza
        self.varianza_button = tk.Button(root, text="C. Mínima Varianza", command=self.calculate_minima_varianza, state="disabled")
        self.varianza_button.grid(row=7, column=0, columnspan=5, pady=10)

        # Botón para el cuadro resumen
        self.resumen_button = tk.Button(root, text="CUADRO RESUMEN", command=self.calculate_cuadro_resumen, state="disabled")
        self.resumen_button.grid(row=8, column=0, columnspan=5, pady=10)

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
            tk.Label(self.matrix_frame, text="Títulos de Columnas:", font=("Arial", 10, "bold"))\
                .grid(row=0, column=1, columnspan=self.cols, pady=5)
            for j in range(self.cols):
                entry = tk.Entry(self.matrix_frame, width=10, font=("Arial", 10, "bold"))
                entry.grid(row=1, column=j+1, padx=2, pady=2)
                self.col_entries.append(entry)

            # Títulos de filas
            tk.Label(self.matrix_frame, text="Títulos de Filas:", font=("Arial", 10, "bold"))\
                .grid(row=2, column=0, rowspan=self.rows, padx=5, pady=5)
            for i in range(self.rows):
                entry = tk.Entry(self.matrix_frame, width=10, font=("Arial", 10, "bold"))
                entry.grid(row=i+3, column=0, padx=2, pady=2)
                self.row_entries.append(entry)

            # Entradas para la matriz de valores
            self.entries = []
            for i in range(self.rows):
                row_entries = []
                for j in range(self.cols):
                    entry = tk.Entry(self.matrix_frame, width=10)
                    entry.grid(row=i+3, column=j+1, padx=2, pady=2)
                    row_entries.append(entry)
                self.entries.append(row_entries)

            # Fila de probabilidades (pesos) para cada columna
            tk.Label(self.matrix_frame, text="Probabilidades:", font=("Arial", 10, "bold"))\
                .grid(row=self.rows+3, column=0, pady=5)
            self.prob_entries = []
            for j in range(self.cols):
                entry = tk.Entry(self.matrix_frame, width=10, font=("Arial", 10, "bold"),
                                 relief="solid", borderwidth=2)
                entry.grid(row=self.rows+3, column=j+1, padx=2, pady=2)
                self.prob_entries.append(entry)

            # Habilitar los botones
            self.submit_button["state"] = "normal"
            self.criteria_button["state"] = "normal"
            self.max_button["state"] = "normal"
            self.lament_button["state"] = "normal"
            self.varianza_button["state"] = "normal"
            self.resumen_button["state"] = "normal"

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

        # Obtener y validar las probabilidades
        probabilities = []
        for entry in self.prob_entries:
            value = entry.get()
            try:
                num_value = float(value) if '.' in value else int(value)
                probabilities.append(num_value)
            except ValueError:
                messagebox.showerror("Error", "Los valores de probabilidades deben ser numéricos.")
                return

        # Ventana para mostrar la matriz
        table_window = tk.Toplevel(self.root)
        table_window.title("Visualización de Matriz")

        style = ttk.Style()
        style.configure("Treeview", rowheight=30, font=("Arial", 12), borderwidth=2, relief="solid")
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"),
                        background="white", foreground="black", borderwidth=2, relief="solid")

        tree = ttk.Treeview(table_window, columns=["Fila"] + col_titles, show="headings", style="Treeview")
        tree.heading("Fila", text="Fila", anchor="center")
        tree.column("Fila", width=120, anchor="center")
        for col in col_titles:
            tree.heading(col, text=col, anchor="center")
            tree.column(col, width=120, anchor="center")

        for i in range(self.rows):
            tree.insert("", "end", values=(row_titles[i],) +
                        tuple(self.format_number(n) for n in [float(x.get()) if '.' in x.get() else int(x.get()) for x in self.entries[i]]))
        # Insertar la fila de probabilidades en negrilla
        tree.insert("", "end", values=("Probabilidades",) +
                    tuple(self.format_number(p) for p in probabilities), tags=("bold",))
        tree.tag_configure("bold", font=("Arial", 12, "bold"))
        tree.pack(expand=True, fill="both")

    def calculate_criteria(self):
        """
        Suma ponderada: Para cada alternativa se calcula:
          criterio = sum(valor * probabilidad)
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

        criteria_results = []
        for i in range(self.rows):
            weighted_sum = 0
            for j in range(self.cols):
                weighted_sum += matrix[i][j] * probabilities[j]
            criteria_results.append(weighted_sum)

        result_window = tk.Toplevel(self.root)
        result_window.title("Resultado del Criterio")

        style = ttk.Style()
        style.configure("Treeview", rowheight=30, font=("Arial", 12),
                        borderwidth=2, relief="solid")
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"),
                        background="white", foreground="black", borderwidth=2, relief="solid")

        tree = ttk.Treeview(result_window, columns=("Alternativa", "Criterio"),
                            show="headings", style="Treeview")
        tree.heading("Alternativa", text="Alternativa", anchor="center")
        tree.heading("Criterio", text="Criterio", anchor="center")
        tree.column("Alternativa", width=150, anchor="center")
        tree.column("Criterio", width=150, anchor="center")

        for i in range(self.rows):
            alt = self.row_entries[i].get()
            criterio_val = self.format_number(criteria_results[i])
            tree.insert("", "end", values=(alt, criterio_val))

        tree.pack(expand=True, fill="both")

    def calculate_max_possibility(self):
        """
        Identifica la columna con la mayor probabilidad y en esa columna
        busca el valor máximo. Luego muestra la alternativa (fila) que posee ese valor.
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

        result_label = tk.Label(result_window, text=f"{self.row_entries[max_row_index].get()} = {self.format_number(max_value)}",
                                 font=("Arial", 14))
        result_label.pack(padx=20, pady=20)

    def calculate_lamentaciones_minimas(self):
        """
        Para cada columna se extrae el valor máximo (fila "MAX"), se crea una matriz de diferencias:
            diferencia = (máximo de la columna) - (valor original)
        Luego, se multiplica cada diferencia por la probabilidad correspondiente y se suma para cada alternativa.
        Se muestran dos tablas:
         1. La matriz de diferencias con la fila "MAX" incluida.
         2. La tabla con el cálculo final para cada alternativa.
        """
        # Recuperar la matriz de valores
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

        # Recuperar las probabilidades
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

        # Recuperar títulos de filas y columnas
        row_titles = [entry.get() for entry in self.row_entries]
        col_titles = [entry.get() for entry in self.col_entries]

        # Calcular la fila "MAX" para cada columna
        max_row = []
        for j in range(self.cols):
            col_values = [matrix[i][j] for i in range(self.rows)]
            max_val = max(col_values)
            max_row.append(max_val)

        # Calcular la matriz de diferencias
        diff_matrix = []
        for i in range(self.rows):
            diff_row = []
            for j in range(self.cols):
                diff_row.append(max_row[j] - matrix[i][j])
            diff_matrix.append(diff_row)

        # Calcular la suma ponderada para cada alternativa (fila) usando la matriz de diferencias
        final_results = []
        for i in range(self.rows):
            weighted_sum = 0
            for j in range(self.cols):
                weighted_sum += probabilities[j] * diff_matrix[i][j]
            final_results.append(weighted_sum)

        # Ventana para mostrar los resultados
        result_window = tk.Toplevel(self.root)
        result_window.title("C. Lamentaciones Mínimas esperadas")

        style = ttk.Style()
        style.configure("Treeview", rowheight=30, font=("Arial", 12),
                        borderwidth=2, relief="solid")
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"),
                        background="white", foreground="black", borderwidth=2, relief="solid")

        # --- Tabla 1: Matriz de diferencias con la fila "MAX" ---
        frame1 = tk.Frame(result_window)
        frame1.pack(padx=10, pady=10, fill="both", expand=True)

        label1 = tk.Label(frame1, text="Matriz de Lamentaciones Mínimas (diferencias)", font=("Arial", 12, "bold"))
        label1.pack()

        tree1 = ttk.Treeview(frame1, columns=["Alternativa"] + col_titles, show="headings", height=self.rows+1)
        tree1.heading("Alternativa", text="Alternativa", anchor="center")
        tree1.column("Alternativa", width=120, anchor="center")
        for col in col_titles:
            tree1.heading(col, text=col, anchor="center")
            tree1.column(col, width=120, anchor="center")

        for i in range(self.rows):
            tree1.insert("", "end", values=(row_titles[i],) + tuple(self.format_number(v) for v in diff_matrix[i]))
        tree1.insert("", "end", values=("MAX",) + tuple(self.format_number(v) for v in max_row), tags=("bold",))
        tree1.tag_configure("bold", font=("Arial", 12, "bold"))
        tree1.pack(fill="both", expand=True)

        # --- Tabla 2: Resultados finales (suma ponderada de diferencias) ---
        frame2 = tk.Frame(result_window)
        frame2.pack(padx=10, pady=10, fill="both", expand=True)

        label2 = tk.Label(frame2, text="Resultados Finales", font=("Arial", 12, "bold"))
        label2.pack()

        tree2 = ttk.Treeview(frame2, columns=("Alternativa", "Cálculo"), show="headings", height=self.rows)
        tree2.heading("Alternativa", text="Alternativa", anchor="center")
        tree2.column("Alternativa", width=150, anchor="center")
        tree2.heading("Cálculo", text="Cálculo", anchor="center")
        tree2.column("Cálculo", width=250, anchor="center")

        for i in range(self.rows):
            calc_str = "(" + " + ".join(f"{self.format_number(probabilities[j])}*{self.format_number(diff_matrix[i][j])}" for j in range(self.cols)) + ")"
            calc_value = self.format_number(final_results[i])
            tree2.insert("", "end", values=(row_titles[i], f"{calc_str} = {calc_value}"))
        tree2.pack(fill="both", expand=True)

    def calculate_minima_varianza(self):
        """
        Utiliza el resultado de la tabla Criterio para calcular, para cada alternativa,
        la siguiente operación:
        
          MV_i = ∑₍ⱼ₎ p_j * ( x_{ij} - C_i )^2
          
        donde:
          • C_i = ∑₍ⱼ₎ p_j * x_{ij}   (valor del criterio)
          
        Se muestra una ventana con dos tablas:
          1. La tabla de Criterio.
          2. Una tabla con el detalle del cálculo de Mínima Varianza para cada alternativa.
        """
        # Recuperar la matriz de valores
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

        # Recuperar las probabilidades
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

        # Recuperar los títulos de las filas (alternativas)
        row_titles = [entry.get() for entry in self.row_entries]

        # Calcular el criterio para cada alternativa: C_i = ∑ p_j * x_{ij}
        criteria_list = []
        for i in range(self.rows):
            c = 0
            for j in range(self.cols):
                c += probabilities[j] * matrix[i][j]
            criteria_list.append(c)

        # Calcular la "mínima varianza" para cada alternativa:
        # MV_i = ∑ p_j * ( x_{ij} - C_i )^2
        varianza_list = []
        for i in range(self.rows):
            v = 0
            for j in range(self.cols):
                diff = matrix[i][j] - criteria_list[i]
                v += probabilities[j] * (diff ** 2)
            varianza_list.append(v)

        # Crear ventana para mostrar ambas tablas
        result_window = tk.Toplevel(self.root)
        result_window.title("C. Mínima Varianza")

        # --- Tabla 1: Tabla de Criterio ---
        frame1 = tk.Frame(result_window)
        frame1.pack(padx=10, pady=10, fill="both", expand=True)

        label1 = tk.Label(frame1, text="Tabla de Criterio", font=("Arial", 12, "bold"))
        label1.pack()

        tree1 = ttk.Treeview(frame1, columns=("Alternativa", "Criterio"),
                             show="headings", height=self.rows)
        tree1.heading("Alternativa", text="Alternativa", anchor="center")
        tree1.column("Alternativa", width=150, anchor="center")
        tree1.heading("Criterio", text="Criterio", anchor="center")
        tree1.column("Criterio", width=150, anchor="center")

        for i in range(self.rows):
            tree1.insert("", "end", values=(row_titles[i], self.format_number(criteria_list[i])))
        tree1.pack(fill="both", expand=True)

        # --- Tabla 2: Detalle de la operación "Mínima Varianza" ---
        frame2 = tk.Frame(result_window)
        frame2.pack(padx=10, pady=10, fill="both", expand=True)

        label2 = tk.Label(frame2, text="Tabla de Mínima Varianza", font=("Arial", 12, "bold"))
        label2.pack()

        tree2 = ttk.Treeview(frame2, columns=("Alternativa", "Cálculo"), show="headings", height=self.rows)
        tree2.heading("Alternativa", text="Alternativa", anchor="center")
        tree2.column("Alternativa", width=150, anchor="center")
        tree2.heading("Cálculo", text="Cálculo", anchor="center")
        tree2.column("Cálculo", width=400, anchor="center")

        for i in range(self.rows):
            # Armar la expresión de cada alternativa:
            terms = []
            for j in range(self.cols):
                term = f"{self.format_number(probabilities[j])}*({self.format_number(matrix[i][j])} - ({self.format_number(criteria_list[i])}))^2"
                terms.append(term)
            calc_str = " + ".join(terms)
            final_str = f"{calc_str} = {self.format_number(varianza_list[i])}"
            tree2.insert("", "end", values=(row_titles[i], final_str))
        tree2.pack(fill="both", expand=True)

    def calculate_cuadro_resumen(self):
        """
        Crea un cuadro resumen con 4 columnas (C1, C2, C3 y C4) donde:
          - C1: Rango (de mayor a menor) del criterio (suma ponderada)
          - C2: Rango (únicamente 1 para la alternativa con mayor valor en la columna con mayor probabilidad; el resto "-"
                 se muestra como -)
          - C3: Rango (de menor a mayor) de las lamentaciones mínimas
          - C4: Rango (de menor a mayor) de la mínima varianza
        Luego, se cuenta en cada fila la cantidad de "1" y se determina la mejor opción (la alternativa con mayor cantidad de 1).
        Se muestra una tabla resumen y se indica la mejor opción.
        """
        # Recuperar la matriz de valores
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
            
        # Recuperar las probabilidades
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

        # Recuperar los títulos de las filas (alternativas)
        row_titles = [entry.get() for entry in self.row_entries]
        
        # C1: Criterio (suma ponderada)
        C1 = []
        for i in range(self.rows):
            c = sum(matrix[i][j] * probabilities[j] for j in range(self.cols))
            C1.append(c)
            
        # C2: Máxima Posibilidad: Se toma el valor de la columna con mayor probabilidad
        max_prob_index = probabilities.index(max(probabilities))
        C2_values = [matrix[i][max_prob_index] for i in range(self.rows)]
        max_C2 = max(C2_values)
        # Solo la alternativa con el máximo en esa columna recibe rango 1; el resto se marca como "-"
        ranking_C2 = []
        for i in range(self.rows):
            if C2_values[i] == max_C2:
                ranking_C2.append(1)
            else:
                ranking_C2.append("-")
                
        # C3: Lamentaciones Mínimas: Para cada alternativa
        # Primero, obtener el máximo de cada columna
        max_row = []
        for j in range(self.cols):
            max_j = max(matrix[i][j] for i in range(self.rows))
            max_row.append(max_j)
        C3 = []
        for i in range(self.rows):
            lam = sum(probabilities[j] * (max_row[j] - matrix[i][j]) for j in range(self.cols))
            C3.append(lam)
            
        # C4: Mínima Varianza: Para cada alternativa
        C4 = []
        for i in range(self.rows):
            var = sum(probabilities[j] * ((matrix[i][j] - C1[i])**2) for j in range(self.cols))
            C4.append(var)
            
        # Rangos:
        # Para C1: Ordenar de mayor a menor (mayor valor = rango 1)
        ranking_C1 = [0] * self.rows
        sorted_indices = sorted(range(self.rows), key=lambda i: C1[i], reverse=True)
        rank = 1
        for idx in sorted_indices:
            ranking_C1[idx] = rank
            rank += 1
        
        # Para C3: Ordenar de menor a mayor (menor valor = rango 1)
        ranking_C3 = [0] * self.rows
        sorted_indices = sorted(range(self.rows), key=lambda i: C3[i])
        rank = 1
        for idx in sorted_indices:
            ranking_C3[idx] = rank
            rank += 1
        
        # Para C4: Ordenar de menor a mayor (menor valor = rango 1)
        ranking_C4 = [0] * self.rows
        sorted_indices = sorted(range(self.rows), key=lambda i: C4[i])
        rank = 1
        for idx in sorted_indices:
            ranking_C4[idx] = rank
            rank += 1
        
        # Armar la tabla resumen:
        # Cada fila: [Alternativa, ranking_C1, ranking_C2, ranking_C3, ranking_C4]
        summary = []
        for i in range(self.rows):
            summary.append([row_titles[i], ranking_C1[i], ranking_C2[i], ranking_C3[i], ranking_C4[i]])
        
        # Determinar la mejor opción: Contar cuántos "1" tiene cada fila (ignorando "-" en C2)
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
        
        # Mostrar el cuadro resumen en una nueva ventana
        result_window = tk.Toplevel(self.root)
        result_window.title("Cuadro Resumen")
        
        style = ttk.Style()
        style.configure("Treeview", rowheight=30, font=("Arial", 12), borderwidth=2, relief="solid")
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"),
                        background="white", foreground="black", borderwidth=2, relief="solid")
        
        tree = ttk.Treeview(result_window, columns=("Alternativa", "C1", "C2", "C3", "C4"), show="headings")
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
        tree.pack(expand=True, fill="both")
        
        # Mostrar la mejor opción
        label_best = tk.Label(result_window, text=f"La mejor opción es: {best_alternative}", font=("Arial", 14, "bold"))
        label_best.pack(padx=10, pady=10)

    def format_number(self, num):
        """Devuelve el número sin decimales si es entero, o con decimales si es flotante."""
        return int(num) if num == int(num) else num

if __name__ == "__main__":
    root = tk.Tk()
    app = MatrixApp(root)
    root.mainloop()
