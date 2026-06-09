import tkinter as tk
from tkinter import ttk
from controllers.caja_diaria_controller import CajaDiariaController

class CajaDiariaView(tk.Toplevel):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        
        self.title("Caja Diaria")
        self.geometry("800x600")
        self.resizable(False, False)
        
        # Colores solicitados
        self.COLOR_FONDO = "#e0f2fe" # Celeste muy claro
        self.COLOR_PANEL = "#ffffff"
        self.COLOR_TEXTO = "#1f2937"
        self.COLOR_BTN_ACTUALIZAR = "#3b82f6"  # Celeste
        self.COLOR_BTN_VOLVER = "#6b7280"  # Gris
        
        self.configure(bg=self.COLOR_FONDO)
        
        self.var_total = tk.StringVar(value="S/ 0.00")
        
        self._build_interface()
        self.controller = CajaDiariaController(self)
        
    def _build_interface(self):
        # Título principal
        titulo = tk.Label(self, text="Reporte de Caja Diaria", font=("Segoe UI", 20, "bold"), bg=self.COLOR_FONDO, fg=self.COLOR_TEXTO)
        titulo.pack(pady=20)
        
        # Contenedor principal
        main_frame = tk.Frame(self, bg=self.COLOR_FONDO)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Panel superior (Resumen)
        panel_resumen = tk.Frame(main_frame, bg=self.COLOR_FONDO)
        panel_resumen.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(panel_resumen, text="Ingreso Total del Día:", font=("Segoe UI", 14, "bold"), bg=self.COLOR_FONDO, fg=self.COLOR_TEXTO).pack(side=tk.LEFT, padx=10)
        tk.Label(panel_resumen, textvariable=self.var_total, font=("Segoe UI", 18, "bold"), bg=self.COLOR_FONDO, fg="#047857").pack(side=tk.LEFT, padx=10) # Verde oscuro para dinero
        
        self.btn_actualizar = tk.Button(panel_resumen, text="Actualizar", bg=self.COLOR_BTN_ACTUALIZAR, fg="white", font=("Segoe UI", 10, "bold"), relief=tk.RAISED, cursor="hand2", width=12)
        self.btn_actualizar.pack(side=tk.RIGHT, padx=10)
        
        # Panel central (Lista)
        panel_lista = tk.LabelFrame(main_frame, text="Pagos Recibidos Hoy", bg=self.COLOR_PANEL, fg=self.COLOR_TEXTO, font=("Segoe UI", 12, "bold"))
        panel_lista.pack(fill=tk.BOTH, expand=True, ipadx=10, ipady=10)
        
        # Treeview para la lista
        columnas = ("numero", "paciente", "fecha", "total")
        self.tree = ttk.Treeview(panel_lista, columns=columnas, show="headings", height=15)
        
        self.tree.heading("numero", text="N° Factura")
        self.tree.heading("paciente", text="Paciente")
        self.tree.heading("fecha", text="Fecha y Hora")
        self.tree.heading("total", text="Total Pagado")
        
        self.tree.column("numero", width=100, anchor="center")
        self.tree.column("paciente", width=250)
        self.tree.column("fecha", width=150, anchor="center")
        self.tree.column("total", width=100, anchor="e")
        
        scrollbar = ttk.Scrollbar(panel_lista, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=(10, 5))
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Boton volver
        btn_volver = tk.Button(self, text="Volver al Menú", bg=self.COLOR_BTN_VOLVER, fg="white", font=("Segoe UI", 10), cursor="hand2", command=self.cerrar_ventana)
        btn_volver.place(x=20, y=20)

    def cerrar_ventana(self):
        self.root.deiconify()
        self.destroy()
