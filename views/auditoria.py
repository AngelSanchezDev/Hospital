import tkinter as tk
from tkinter import ttk
from controllers.auditoria_controller import AuditoriaController

class AuditoriaView(tk.Toplevel):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        
        self.title("Registro de Auditoría")
        self.geometry("1000x600")
        self.resizable(True, True)
        
        # Colores
        self.COLOR_FONDO = "#e0f2fe"
        self.COLOR_PANEL = "#ffffff"
        self.COLOR_TEXTO = "#1f2937"
        self.COLOR_BTN = "#3b82f6"
        self.COLOR_BTN_VOLVER = "#6b7280"
        
        self.configure(bg=self.COLOR_FONDO)
        self._build_interface()
        self.controller = AuditoriaController(self)
        
    def _build_interface(self):
        titulo = tk.Label(self, text="Auditoría de Sistema (Sólo Lectura)", font=("Segoe UI", 20, "bold"), bg=self.COLOR_FONDO, fg=self.COLOR_TEXTO)
        titulo.pack(pady=20)
        
        main_frame = tk.Frame(self, bg=self.COLOR_FONDO)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        panel_lista = tk.LabelFrame(main_frame, text="Cambios Recientes", bg=self.COLOR_PANEL, fg=self.COLOR_TEXTO, font=("Segoe UI", 12, "bold"))
        panel_lista.pack(fill=tk.BOTH, expand=True, ipadx=10, ipady=10)
        
        columnas = ("id", "fecha", "accion", "tabla", "usuario", "anterior", "nuevo")
        self.tree = ttk.Treeview(panel_lista, columns=columnas, show="headings", height=20)
        
        self.tree.heading("id", text="ID")
        self.tree.heading("fecha", text="Fecha")
        self.tree.heading("accion", text="Acción")
        self.tree.heading("tabla", text="Tabla")
        self.tree.heading("usuario", text="Usuario BD")
        self.tree.heading("anterior", text="Datos Anteriores")
        self.tree.heading("nuevo", text="Datos Nuevos")
        
        self.tree.column("id", width=50, stretch=tk.NO)
        self.tree.column("fecha", width=140, stretch=tk.NO)
        self.tree.column("accion", width=80, stretch=tk.NO)
        self.tree.column("tabla", width=100, stretch=tk.NO)
        self.tree.column("usuario", width=120, stretch=tk.NO)
        self.tree.column("anterior", width=200)
        self.tree.column("nuevo", width=200)
        
        scrollbar_y = ttk.Scrollbar(panel_lista, orient="vertical", command=self.tree.yview)
        scrollbar_x = ttk.Scrollbar(panel_lista, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        self.tree.grid(row=0, column=0, sticky="nsew", padx=10, pady=5)
        scrollbar_y.grid(row=0, column=1, sticky="ns")
        scrollbar_x.grid(row=1, column=0, sticky="ew", padx=10)
        
        panel_lista.grid_rowconfigure(0, weight=1)
        panel_lista.grid_columnconfigure(0, weight=1)

        frame_botones = tk.Frame(main_frame, bg=self.COLOR_FONDO)
        frame_botones.pack(fill=tk.X, pady=10)
        
        self.btn_actualizar = tk.Button(frame_botones, text="Actualizar", bg=self.COLOR_BTN, fg="white", font=("Segoe UI", 10, "bold"), width=15, cursor="hand2")
        self.btn_actualizar.pack(side=tk.RIGHT)

        btn_volver = tk.Button(self, text="Volver al Menú", bg=self.COLOR_BTN_VOLVER, fg="white", font=("Segoe UI", 10), cursor="hand2", command=self.cerrar_ventana)
        btn_volver.place(x=20, y=20)

    def cerrar_ventana(self):
        self.root.deiconify()
        self.destroy()
