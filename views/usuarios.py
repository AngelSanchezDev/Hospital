import tkinter as tk
from tkinter import ttk
from controllers.usuario_controller import UsuarioController

class UsuariosView(tk.Toplevel):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        
        self.title("Gestión de Usuarios")
        self.geometry("1100x650")
        self.resizable(True, True)
        
        # Colores
        self.COLOR_FONDO = "#e0f2fe"
        self.COLOR_PANEL = "#ffffff"
        self.COLOR_TEXTO = "#1f2937"
        self.COLOR_BTN_GUARDAR = "#22c55e"
        self.COLOR_BTN_EDITAR = "#3b82f6"
        self.COLOR_BTN_ELIMINAR = "#ef4444"
        self.COLOR_BTN_LIMPIAR = "#6b7280"
        
        self.configure(bg=self.COLOR_FONDO)
        
        self.var_username = tk.StringVar()
        self.var_nombres = tk.StringVar()
        self.var_apellidos = tk.StringVar()
        self.var_email = tk.StringVar()
        self.var_telefono = tk.StringVar()
        self.var_direccion = tk.StringVar()
        self.var_password = tk.StringVar()
        self.var_estado = tk.StringVar(value="Activo")
        
        self._build_interface()
        self.controller = UsuarioController(self)
        
    def _build_interface(self):
        titulo = tk.Label(self, text="Gestión de Personal / Usuarios", font=("Segoe UI", 20, "bold"), bg=self.COLOR_FONDO, fg=self.COLOR_TEXTO)
        titulo.pack(pady=20)
        
        main_frame = tk.Frame(self, bg=self.COLOR_FONDO)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Panel izquierdo (Formulario)
        panel_form = tk.LabelFrame(main_frame, text="Datos del Usuario", bg=self.COLOR_PANEL, fg=self.COLOR_TEXTO, font=("Segoe UI", 12, "bold"))
        panel_form.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10), ipadx=10, ipady=10)
        
        # Campos
        campos = [
            ("Username (*):", self.var_username, False),
            ("Nombres (*):", self.var_nombres, False),
            ("Apellidos (*):", self.var_apellidos, False),
            ("Email (*):", self.var_email, False),
            ("Contraseña:", self.var_password, True),
            ("Teléfono:", self.var_telefono, False),
            ("Dirección:", self.var_direccion, False)
        ]
        
        for i, (label, var, is_pw) in enumerate(campos):
            tk.Label(panel_form, text=label, bg=self.COLOR_PANEL, font=("Segoe UI", 10)).grid(row=i, column=0, sticky="w", pady=5, padx=10)
            if is_pw:
                tk.Entry(panel_form, textvariable=var, show="*", font=("Segoe UI", 10), width=25).grid(row=i, column=1, pady=5, padx=10)
            else:
                tk.Entry(panel_form, textvariable=var, font=("Segoe UI", 10), width=25).grid(row=i, column=1, pady=5, padx=10)
        
        tk.Label(panel_form, text="Estado:", bg=self.COLOR_PANEL, font=("Segoe UI", 10)).grid(row=7, column=0, sticky="w", pady=5, padx=10)
        ttk.Combobox(panel_form, textvariable=self.var_estado, values=["Activo", "Inactivo"], state="readonly", font=("Segoe UI", 10), width=23).grid(row=7, column=1, pady=5, padx=10)
        
        tk.Label(panel_form, text="(Dejar contraseña en blanco al editar para no cambiarla)", bg=self.COLOR_PANEL, fg="gray", font=("Segoe UI", 8)).grid(row=8, column=0, columnspan=2, pady=5)

        # Botones Formulario
        frame_botones_form = tk.Frame(panel_form, bg=self.COLOR_PANEL)
        frame_botones_form.grid(row=9, column=0, columnspan=2, pady=15)
        
        self.btn_guardar = tk.Button(frame_botones_form, text="Guardar", bg=self.COLOR_BTN_GUARDAR, fg="white", font=("Segoe UI", 10, "bold"), relief=tk.RAISED, cursor="hand2", width=12)
        self.btn_guardar.grid(row=0, column=0, padx=5)
        
        self.btn_limpiar = tk.Button(frame_botones_form, text="Limpiar", bg=self.COLOR_BTN_LIMPIAR, fg="white", font=("Segoe UI", 10, "bold"), relief=tk.RAISED, cursor="hand2", width=12)
        self.btn_limpiar.grid(row=0, column=1, padx=5)
        
        # Panel derecho (Lista)
        panel_lista = tk.LabelFrame(main_frame, text="Directorio de Personal", bg=self.COLOR_PANEL, fg=self.COLOR_TEXTO, font=("Segoe UI", 12, "bold"))
        panel_lista.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, ipadx=10, ipady=10)
        
        columnas = ("id", "username", "nombre_completo", "email", "estado", "tel", "dir", "nombres", "apellidos")
        self.tree = ttk.Treeview(panel_lista, columns=columnas, show="headings", height=15)
        
        self.tree.heading("id", text="ID")
        self.tree.heading("username", text="Username")
        self.tree.heading("nombre_completo", text="Nombre Completo")
        self.tree.heading("email", text="Email")
        self.tree.heading("estado", text="Estado")
        
        self.tree.column("id", width=0, stretch=tk.NO)
        self.tree.column("username", width=100)
        self.tree.column("nombre_completo", width=200)
        self.tree.column("email", width=150)
        self.tree.column("estado", width=70, anchor="center")
        self.tree.column("tel", width=0, stretch=tk.NO)
        self.tree.column("dir", width=0, stretch=tk.NO)
        self.tree.column("nombres", width=0, stretch=tk.NO)
        self.tree.column("apellidos", width=0, stretch=tk.NO)
        
        scrollbar = ttk.Scrollbar(panel_lista, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=(10, 5))
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        frame_botones_lista = tk.Frame(panel_lista, bg=self.COLOR_PANEL)
        frame_botones_lista.pack(side=tk.BOTTOM, pady=10)
        
        self.btn_editar = tk.Button(frame_botones_lista, text="Editar", bg=self.COLOR_BTN_EDITAR, fg="white", font=("Segoe UI", 10, "bold"), relief=tk.RAISED, cursor="hand2", width=12)
        self.btn_editar.pack(side=tk.LEFT, padx=10)
        
        self.btn_eliminar = tk.Button(frame_botones_lista, text="Eliminar", bg=self.COLOR_BTN_ELIMINAR, fg="white", font=("Segoe UI", 10, "bold"), relief=tk.RAISED, cursor="hand2", width=12)
        self.btn_eliminar.pack(side=tk.LEFT, padx=10)

        btn_volver = tk.Button(self, text="Volver al Menú", bg=self.COLOR_BTN_LIMPIAR, fg="white", font=("Segoe UI", 10), cursor="hand2", command=self.cerrar_ventana)
        btn_volver.place(x=20, y=20)

    def cerrar_ventana(self):
        self.root.deiconify()
        self.destroy()
