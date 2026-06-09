import tkinter as tk
from tkinter import ttk

import session
from controllers.facturacion_controller import FacturacionController


class FacturacionView(tk.Toplevel):
    def __init__(self, root):
        super().__init__(root)
        self.title("Facturación Electrónica")
        self.geometry("1020x780")
        self.resizable(True, True)
        self.configure(bg="white")

        style = ttk.Style(self)
        style.configure("Facturacion.TFrame", background="white")
        style.configure("Facturacion.TLabel", background="white", foreground="#1f2937")

        encabezado = ttk.Frame(self, style="Facturacion.TFrame")
        encabezado.pack(fill="x", padx=12, pady=(10, 0))
        ttk.Label(encabezado, text="Facturación Electrónica", font=("Segoe UI", 16, "bold"), style="Facturacion.TLabel").pack(anchor="w")
        ttk.Label(encabezado, text=session.get_resumen_usuario(), font=("Segoe UI", 10), style="Facturacion.TLabel").pack(anchor="w", pady=(4, 0))

        FacturacionController(self)


if __name__ == "__main__":
    main_root = tk.Tk()
    main_root.withdraw()
    facturacion_view = FacturacionView(main_root)
    facturacion_view.mainloop()
