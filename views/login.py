import os
import sys
import tkinter as tk
from tkinter import messagebox

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database.conexion import conexion
import session


class LoginView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hospital - Acceso")
        self.geometry("460x560")
        self.resizable(False, False)
        self.configure(bg="#eaf4fb")

        self._build_ui()

    def _build_ui(self):
        header = tk.Frame(self, bg="#1565c0", height=150)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="Hospital",
            bg="#1565c0",
            fg="white",
            font=("Segoe UI", 26, "bold")
        ).pack(pady=(28, 4))

        tk.Label(
            header,
            text="Acceso al sistema",
            bg="#1565c0",
            fg="#dbeafe",
            font=("Segoe UI", 11)
        ).pack()

        form = tk.Frame(self, bg="white", bd=0, highlightthickness=1, highlightbackground="#cfe3f5")
        form.pack(fill="both", expand=True, padx=28, pady=24)

        tk.Label(form, text="Usuario", bg="white", fg="#1f2937", font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=24, pady=(28, 6))
        self.entry_user = tk.Entry(form, width=30, font=("Segoe UI", 11), relief="solid", bd=1)
        self.entry_user.pack(fill="x", padx=24)

        tk.Label(form, text="Contraseña", bg="white", fg="#1f2937", font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=24, pady=(18, 6))
        self.entry_pw = tk.Entry(form, show="*", width=30, font=("Segoe UI", 11), relief="solid", bd=1)
        self.entry_pw.pack(fill="x", padx=24)

        self.btn_login = tk.Button(
            form,
            text="ENTRAR",
            command=self.intentar_login,
            bg="#3182ce",
            fg="white",
            activebackground="#2563eb",
            activeforeground="white",
            font=("Segoe UI", 12, "bold"),
            relief="flat",
            cursor="hand2"
        )
        self.btn_login.pack(fill="x", padx=24, pady=(28, 12), ipady=8)

        tk.Label(
            form,
            text="Sistema hospitalario empresarial",
            bg="white",
            fg="#6b7280",
            font=("Segoe UI", 9)
        ).pack(pady=(18, 0))

        self.bind("<Return>", lambda event: self.intentar_login())

    def intentar_login(self):
        user = self.entry_user.get().strip()
        pw = self.entry_pw.get().strip()

        if not user or not pw:
            messagebox.showwarning("Validación", "Ingrese usuario y contraseña")
            return

        try:
            cursor = conexion.cursor()
            query = """
                SELECT TOP 1
                    u.id_usuario,
                    u.nombres,
                    u.apellidos,
                    u.email,
                    r.nombre AS rol
                FROM Usuario u
                LEFT JOIN UsuarioRol ur ON ur.id_usuario = u.id_usuario
                LEFT JOIN Rol r ON r.id_rol = ur.id_rol
                WHERE u.username = ? AND u.password_hash = ? AND u.eliminado = 0
                ORDER BY CASE
                    WHEN r.nombre = 'Administrador' THEN 1
                    WHEN r.nombre = 'Medico' THEN 2
                    WHEN r.nombre = 'Recepcion' THEN 3
                    ELSE 4
                END, ur.fecha_asignacion ASC
            """
            cursor.execute(query, (user, pw))
            resultado = cursor.fetchone()

            if resultado:
                session.iniciar_sesion({
                    "id_usuario": resultado[0],
                    "username": user,
                    "nombres": resultado[1],
                    "apellidos": resultado[2],
                    "email": resultado[3],
                    "rol": resultado[4] or "Sin rol",
                })
                messagebox.showinfo("Login Exitoso", f"Bienvenido, {resultado[1]}")
                self.destroy()
                from views.menu_principal import MenuPrincipal
                menu = MenuPrincipal()
                menu.mainloop()
            else:
                messagebox.showerror("Error", "Usuario o contraseña incorrectos")
        except Exception as e:
            messagebox.showerror("Error de conexión", f"Error: {str(e)}")


if __name__ == "__main__":
    app = LoginView()
    app.mainloop()
