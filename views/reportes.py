import tkinter as tk
from tkinter import ttk
from controllers.reporte_controller import ReporteController

class ReportesView(tk.Toplevel):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        
        self.title("Generación de Reportes PDF")
        self.geometry("600x400")
        self.resizable(False, False)
        
        # Colores solicitados
        self.COLOR_FONDO = "#e0f2fe"
        self.COLOR_PANEL = "#ffffff"
        self.COLOR_TEXTO = "#1f2937"
        self.COLOR_BTN = "#3b82f6"  # Celeste
        self.COLOR_BTN_VOLVER = "#6b7280"  # Gris
        
        self.configure(bg=self.COLOR_FONDO)
        self._build_interface()
        self.controller = ReporteController(self)
        
    def _build_interface(self):
        # Título principal
        titulo = tk.Label(self, text="Módulo de Reportes", font=("Segoe UI", 20, "bold"), bg=self.COLOR_FONDO, fg=self.COLOR_TEXTO)
        titulo.pack(pady=20)
        
        main_frame = tk.Frame(self, bg=self.COLOR_PANEL)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=20)
        
        instrucciones = tk.Label(main_frame, text="Seleccione el reporte que desea generar (PDF):", font=("Segoe UI", 12), bg=self.COLOR_PANEL, fg=self.COLOR_TEXTO)
        instrucciones.pack(pady=10)
        
        # Grid para los botones
        btn_frame = tk.Frame(main_frame, bg=self.COLOR_PANEL)
        btn_frame.pack(pady=10)
        
        self.btn_pacientes = tk.Button(btn_frame, text="Directorio de Pacientes", bg=self.COLOR_BTN, fg="white", font=("Segoe UI", 11, "bold"), width=25, height=2, cursor="hand2")
        self.btn_pacientes.grid(row=0, column=0, padx=10, pady=10)
        
        self.btn_ingresos = tk.Button(btn_frame, text="Historial de Ingresos", bg=self.COLOR_BTN, fg="white", font=("Segoe UI", 11, "bold"), width=25, height=2, cursor="hand2")
        self.btn_ingresos.grid(row=0, column=1, padx=10, pady=10)
        
        self.btn_auditoria = tk.Button(btn_frame, text="Auditoría Reciente", bg=self.COLOR_BTN, fg="white", font=("Segoe UI", 11, "bold"), width=25, height=2, cursor="hand2")
        self.btn_auditoria.grid(row=1, column=0, padx=10, pady=10)
        
        self.btn_personal = tk.Button(btn_frame, text="Directorio del Personal", bg=self.COLOR_BTN, fg="white", font=("Segoe UI", 11, "bold"), width=25, height=2, cursor="hand2")
        self.btn_personal.grid(row=1, column=1, padx=10, pady=10)

        # Boton volver
        btn_volver = tk.Button(self, text="Volver al Menú", bg=self.COLOR_BTN_VOLVER, fg="white", font=("Segoe UI", 10), cursor="hand2", command=self.cerrar_ventana)
        btn_volver.place(x=20, y=20)

    def cerrar_ventana(self):
        self.root.deiconify()
        self.destroy()
