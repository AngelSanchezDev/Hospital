import tkinter as tk
from tkinter import ttk
from controllers.configuracion_controller import ConfiguracionController

class ConfiguracionView(tk.Toplevel):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        
        self.title("Mi Perfil - Configuración")
        self.geometry("600x500")
        self.resizable(False, False)
        
        # Colores
        self.COLOR_FONDO = "#e0f2fe"
        self.COLOR_PANEL = "#ffffff"
        self.COLOR_TEXTO = "#1f2937"
        self.COLOR_BTN_GUARDAR = "#22c55e"
        self.COLOR_BTN_VOLVER = "#6b7280"
        
        self.configure(bg=self.COLOR_FONDO)
        
        self.var_nombres = tk.StringVar()
        self.var_apellidos = tk.StringVar()
        self.var_email = tk.StringVar()
        self.var_telefono = tk.StringVar()
        self.var_direccion = tk.StringVar()
        self.var_password = tk.StringVar()
        
        self._build_interface()
        self.controller = ConfiguracionController(self)
        
    def _build_interface(self):
        titulo = tk.Label(self, text="Configuración: Mi Perfil", font=("Segoe UI", 20, "bold"), bg=self.COLOR_FONDO, fg=self.COLOR_TEXTO)
        titulo.pack(pady=20)
        
        main_frame = tk.LabelFrame(self, text="Datos Personales", bg=self.COLOR_PANEL, fg=self.COLOR_TEXTO, font=("Segoe UI", 12, "bold"))
        main_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=10)
        
        labels_text = ["Nombres (*):", "Apellidos (*):", "Email (*):", "Teléfono:", "Dirección:", "Nueva Contraseña:"]
        variables = [self.var_nombres, self.var_apellidos, self.var_email, self.var_telefono, self.var_direccion, self.var_password]
        
        for i in range(len(labels_text)):
            tk.Label(main_frame, text=labels_text[i], bg=self.COLOR_PANEL, font=("Segoe UI", 10)).grid(row=i, column=0, sticky="w", pady=10, padx=20)
            if i == 5:
                tk.Entry(main_frame, textvariable=variables[i], show="*", font=("Segoe UI", 10), width=35).grid(row=i, column=1, pady=10, padx=10)
            else:
                tk.Entry(main_frame, textvariable=variables[i], font=("Segoe UI", 10), width=35).grid(row=i, column=1, pady=10, padx=10)
                
        tk.Label(main_frame, text="(Dejar en blanco para no cambiar)", bg=self.COLOR_PANEL, fg="gray", font=("Segoe UI", 8)).grid(row=5, column=2, sticky="w")
        
        frame_botones = tk.Frame(self, bg=self.COLOR_FONDO)
        frame_botones.pack(pady=10)
        
        self.btn_guardar = tk.Button(frame_botones, text="Guardar Cambios", bg=self.COLOR_BTN_GUARDAR, fg="white", font=("Segoe UI", 11, "bold"), width=20, cursor="hand2")
        self.btn_guardar.pack()

        btn_volver = tk.Button(self, text="Volver al Menú", bg=self.COLOR_BTN_VOLVER, fg="white", font=("Segoe UI", 10), cursor="hand2", command=self.cerrar_ventana)
        btn_volver.place(x=20, y=20)

    def cerrar_ventana(self):
        self.root.deiconify()
        self.destroy()
