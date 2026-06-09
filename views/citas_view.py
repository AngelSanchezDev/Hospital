import tkinter as tk
from tkinter import ttk

import session
from controllers.citas_controller import CitasController


class CitasView(tk.Toplevel):
    def __init__(self, root):
        super().__init__(root)
        self.title("Gestión de Citas")
        self.geometry("980x720")
        self.resizable(True, True)

        encabezado = ttk.Frame(self)
        encabezado.pack(fill="x", padx=12, pady=(10, 0))
        ttk.Label(encabezado, text="Gestión de Citas", font=("Segoe UI", 16, "bold")).pack(anchor="w")
        ttk.Label(encabezado, text=session.get_resumen_usuario(), font=("Segoe UI", 10)).pack(anchor="w", pady=(4, 0))

        CitasController(self)


if __name__ == "__main__":
    main_root = tk.Tk()
    main_root.withdraw()
    citas_view = CitasView(main_root)
    citas_view.mainloop()
