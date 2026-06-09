import tkinter as tk
from tkinter import ttk
from controllers.pago_controller import PagoController

class PagosView(tk.Toplevel):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        
        self.title("Gestión de Tipos de Pago")
        self.geometry("800x600")
        self.resizable(False, False)
        
        # Colores solicitados
        self.COLOR_FONDO = "#e0f2fe" # Celeste muy claro (casi blanco)
        self.COLOR_PANEL = "#ffffff"
        self.COLOR_TEXTO = "#1f2937"
        self.COLOR_BTN_GUARDAR = "#22c55e" # Verde
        self.COLOR_BTN_EDITAR = "#3b82f6"  # Celeste
        self.COLOR_BTN_ELIMINAR = "#ef4444" # Rojo
        self.COLOR_BTN_LIMPIAR = "#6b7280"  # Gris
        
        self.configure(bg=self.COLOR_FONDO)
        
        # Variables del formulario
        self.var_nombre = tk.StringVar()
        self.var_descripcion = tk.StringVar()
        self.var_estado = tk.StringVar(value="Activo")
        
        self._build_interface()
        
        # Inicializar controlador
        self.controller = PagoController(self)
        
    def _build_interface(self):
        # Título principal
        titulo = tk.Label(self, text="Gestión de Tipos de Pago", font=("Segoe UI", 20, "bold"), bg=self.COLOR_FONDO, fg=self.COLOR_TEXTO)
        titulo.pack(pady=20)
        
        # Contenedor principal
        main_frame = tk.Frame(self, bg=self.COLOR_FONDO)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Panel izquierdo (Formulario)
        panel_form = tk.LabelFrame(main_frame, text="Datos del Pago", bg=self.COLOR_PANEL, fg=self.COLOR_TEXTO, font=("Segoe UI", 12, "bold"))
        panel_form.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10), ipadx=10, ipady=10)
        
        # Nombre
        tk.Label(panel_form, text="Nombre (*):", bg=self.COLOR_PANEL, font=("Segoe UI", 10)).grid(row=0, column=0, sticky="w", pady=10, padx=10)
        tk.Entry(panel_form, textvariable=self.var_nombre, font=("Segoe UI", 10), width=25).grid(row=0, column=1, pady=10, padx=10)
        
        # Descripción
        tk.Label(panel_form, text="Descripción:", bg=self.COLOR_PANEL, font=("Segoe UI", 10)).grid(row=1, column=0, sticky="w", pady=10, padx=10)
        tk.Entry(panel_form, textvariable=self.var_descripcion, font=("Segoe UI", 10), width=25).grid(row=1, column=1, pady=10, padx=10)
        
        # Estado
        tk.Label(panel_form, text="Estado:", bg=self.COLOR_PANEL, font=("Segoe UI", 10)).grid(row=2, column=0, sticky="w", pady=10, padx=10)
        combo_estado = ttk.Combobox(panel_form, textvariable=self.var_estado, values=["Activo", "Inactivo"], state="readonly", font=("Segoe UI", 10), width=23)
        combo_estado.grid(row=2, column=1, pady=10, padx=10)
        
        # Botones Formulario
        frame_botones_form = tk.Frame(panel_form, bg=self.COLOR_PANEL)
        frame_botones_form.grid(row=3, column=0, columnspan=2, pady=20)
        
        self.btn_guardar = tk.Button(frame_botones_form, text="Guardar", bg=self.COLOR_BTN_GUARDAR, fg="white", font=("Segoe UI", 10, "bold"), relief=tk.RAISED, cursor="hand2", width=12)
        self.btn_guardar.grid(row=0, column=0, padx=5)
        
        self.btn_limpiar = tk.Button(frame_botones_form, text="Limpiar", bg=self.COLOR_BTN_LIMPIAR, fg="white", font=("Segoe UI", 10, "bold"), relief=tk.RAISED, cursor="hand2", width=12)
        self.btn_limpiar.grid(row=0, column=1, padx=5)
        
        # Panel derecho (Lista)
        panel_lista = tk.LabelFrame(main_frame, text="Lista de Pagos", bg=self.COLOR_PANEL, fg=self.COLOR_TEXTO, font=("Segoe UI", 12, "bold"))
        panel_lista.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, ipadx=10, ipady=10)
        
        # Treeview para la lista
        columnas = ("id", "nombre", "descripcion", "estado", "fecha")
        self.tree = ttk.Treeview(panel_lista, columns=columnas, show="headings", height=15)
        
        self.tree.heading("id", text="ID")
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("descripcion", text="Descripción")
        self.tree.heading("estado", text="Estado")
        self.tree.heading("fecha", text="Fecha Creación")
        
        self.tree.column("id", width=40, anchor="center")
        self.tree.column("nombre", width=120)
        self.tree.column("descripcion", width=150)
        self.tree.column("estado", width=70, anchor="center")
        self.tree.column("fecha", width=100, anchor="center")
        
        scrollbar = ttk.Scrollbar(panel_lista, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=(10, 5))
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Botones de Acción (Lista)
        frame_botones_lista = tk.Frame(panel_lista, bg=self.COLOR_PANEL)
        frame_botones_lista.pack(side=tk.BOTTOM, pady=10)
        
        self.btn_editar = tk.Button(frame_botones_lista, text="Editar", bg=self.COLOR_BTN_EDITAR, fg="white", font=("Segoe UI", 10, "bold"), relief=tk.RAISED, cursor="hand2", width=12)
        self.btn_editar.pack(side=tk.LEFT, padx=10)
        
        self.btn_eliminar = tk.Button(frame_botones_lista, text="Eliminar", bg=self.COLOR_BTN_ELIMINAR, fg="white", font=("Segoe UI", 10, "bold"), relief=tk.RAISED, cursor="hand2", width=12)
        self.btn_eliminar.pack(side=tk.LEFT, padx=10)

        # Boton volver (en la raiz, arriba a la izquierda)
        btn_volver = tk.Button(self, text="Volver al Menú", bg=self.COLOR_BTN_LIMPIAR, fg="white", font=("Segoe UI", 10), cursor="hand2", command=self.cerrar_ventana)
        btn_volver.place(x=20, y=20)

    def cerrar_ventana(self):
        self.root.deiconify()
        self.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    app = PagosView(root)
    app.protocol("WM_DELETE_WINDOW", app.cerrar_ventana)
    app.mainloop()
