import tkinter as tk
from tkinter import messagebox
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from database.conexion import conexion
import session


class MenuPrincipal(tk.Tk):
    """Menú principal con sidebar lateral estilo ERP"""

    # ── Paleta ──────────────────────────────────────────────────────────
    C_SIDEBAR_BG   = "#0f4c81"   # Azul marino oscuro
    C_SIDEBAR_HVR  = "#1a6bb5"   # Azul más claro al hover
    C_SIDEBAR_SEL  = "#1e88e5"   # Azul brillante seleccionado
    C_CONTENT_BG   = "#eaf4fb"   # Celeste muy claro
    C_HEADER_BG    = "#1565c0"   # Azul medio header
    C_WHITE        = "#ffffff"
    C_TEXT_LIGHT   = "#d0e8ff"
    C_TEXT_DARK    = "#1f2937"
    C_ACCENT       = "#22c55e"   # Verde
    C_FOOTER       = "#0d3a63"

    ITEMS = [
        ("🏠", "Dashboard",          "abrir_dashboard"),
        ("👥", "Pacientes",          "abrir_pacientes"),
        ("📅", "Citas",              "abrir_citas"),
        ("🧾", "Facturación",        "abrir_facturacion"),
        ("💳", "Pagos",              "abrir_pagos"),
        ("💰", "Caja Diaria",        "abrir_caja_diaria"),
        ("📋", "Cuentas por Cobrar", "abrir_cxc"),
        ("📊", "Reportes",           "abrir_reportes"),
        ("🔍", "Auditoría",          "abrir_auditoria"),
        ("👤", "Usuarios",           "abrir_usuarios"),
        ("⚙️",  "Configuración",     "abrir_configuracion"),
        ("🚪", "Salir",              "salir_sistema"),
    ]

    def __init__(self):
        super().__init__()
        self.title("Sistema Hospitalario")
        self.geometry("1100x700")
        self.resizable(True, True)
        self.configure(bg=self.C_CONTENT_BG)
        self._validar_conexion()
        self._build()

    # ── Conexión ────────────────────────────────────────────────────────
    def _validar_conexion(self):
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT 1")
            cursor.close()
        except Exception as e:
            messagebox.showerror("Error de Conexión",
                                 f"No se pudo conectar a la base de datos:\n{str(e)}")
            self.destroy()

    # ── UI ──────────────────────────────────────────────────────────────
    def _build(self):
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        self._build_sidebar()
        self._build_content()

    def _build_sidebar(self):
        sidebar = tk.Frame(self, bg=self.C_SIDEBAR_BG, width=220)
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_propagate(False)

        # Logo / nombre sistema
        logo_frame = tk.Frame(sidebar, bg=self.C_SIDEBAR_BG, pady=20)
        logo_frame.pack(fill="x")
        tk.Label(logo_frame, text="🏥", font=("Segoe UI", 30),
                 bg=self.C_SIDEBAR_BG, fg=self.C_WHITE).pack()
        tk.Label(logo_frame, text="Hospital",
                 font=("Segoe UI", 14, "bold"),
                 bg=self.C_SIDEBAR_BG, fg=self.C_WHITE).pack()
        tk.Label(logo_frame, text="Sistema de Gestión",
                 font=("Segoe UI", 8),
                 bg=self.C_SIDEBAR_BG, fg=self.C_TEXT_LIGHT).pack()

        # Separador
        tk.Frame(sidebar, bg=self.C_SIDEBAR_SEL, height=1).pack(fill="x", padx=15, pady=(0, 10))

        # Menú items
        self._btn_refs = []
        for icon, label, method in self.ITEMS:
            self._add_menu_item(sidebar, icon, label, method)

        # Footer (usuario)
        tk.Frame(sidebar, bg=self.C_FOOTER, height=1).pack(fill="x", padx=15, pady=(10, 0), side="bottom")
        footer = tk.Frame(sidebar, bg=self.C_FOOTER, pady=10)
        footer.pack(fill="x", side="bottom")
        usuario_str = session.get_resumen_usuario()
        tk.Label(footer, text=usuario_str, font=("Segoe UI", 8),
                 bg=self.C_FOOTER, fg=self.C_TEXT_LIGHT,
                 wraplength=200, justify="center").pack(padx=10)

    def _add_menu_item(self, parent, icon, label, method):
        color_bg  = self.C_SIDEBAR_BG
        color_sel = self.C_SIDEBAR_SEL
        color_hvr = self.C_SIDEBAR_HVR

        row = tk.Frame(parent, bg=color_bg, cursor="hand2")
        row.pack(fill="x", pady=1)

        inner = tk.Frame(row, bg=color_bg)
        inner.pack(fill="x", padx=10, pady=4)

        lbl_icon = tk.Label(inner, text=icon, font=("Segoe UI Emoji", 14),
                            bg=color_bg, fg=self.C_WHITE, width=2, anchor="w")
        lbl_icon.pack(side="left", padx=(5, 8))

        lbl_text = tk.Label(inner, text=label, font=("Segoe UI", 10),
                            bg=color_bg, fg=self.C_TEXT_LIGHT, anchor="w")
        lbl_text.pack(side="left", fill="x", expand=True)

        widgets = [row, inner, lbl_icon, lbl_text]

        def on_enter(e, w=widgets):
            for ww in w: ww.config(bg=color_hvr)
            lbl_text.config(fg=self.C_WHITE)

        def on_leave(e, w=widgets):
            for ww in w: ww.config(bg=color_bg)
            lbl_text.config(fg=self.C_TEXT_LIGHT)

        def on_click(e=None, m=method):
            getattr(self, m)()

        for w in widgets:
            w.bind("<Enter>", on_enter)
            w.bind("<Leave>", on_leave)
            w.bind("<Button-1>", on_click)

    def _build_content(self):
        content = tk.Frame(self, bg=self.C_CONTENT_BG)
        content.grid(row=0, column=1, sticky="nsew")
        content.columnconfigure(0, weight=1)
        content.rowconfigure(1, weight=1)

        # Header
        header = tk.Frame(content, bg=self.C_HEADER_BG, height=70)
        header.grid(row=0, column=0, sticky="ew")
        header.grid_propagate(False)

        tk.Label(header, text="Sistema Financiero Hospitalario",
                 font=("Segoe UI", 18, "bold"),
                 bg=self.C_HEADER_BG, fg=self.C_WHITE).pack(side="left", padx=25, pady=18)

        # Tarjetas de acceso rápido en el área principal
        cards_area = tk.Frame(content, bg=self.C_CONTENT_BG)
        cards_area.grid(row=1, column=0, sticky="nsew", padx=30, pady=30)

        grupos = [
            ("🩺 Atención Médica", [
                ("👥", "Pacientes",      "abrir_pacientes"),
                ("📅", "Citas",          "abrir_citas"),
            ]),
            ("💵 Finanzas", [
                ("🧾", "Facturación",    "abrir_facturacion"),
                ("💳", "Pagos",          "abrir_pagos"),
                ("💰", "Caja Diaria",    "abrir_caja_diaria"),
                ("📋", "CxC",            "abrir_cxc"),
            ]),
            ("📈 Análisis", [
                ("🏠", "Dashboard",      "abrir_dashboard"),
                ("📊", "Reportes",       "abrir_reportes"),
            ]),
            ("🔧 Administración", [
                ("🔍", "Auditoría",      "abrir_auditoria"),
                ("👤", "Usuarios",       "abrir_usuarios"),
                ("⚙️",  "Config.",       "abrir_configuracion"),
            ]),
        ]

        for col_i, (grupo_titulo, items) in enumerate(grupos):
            col_frame = tk.Frame(cards_area, bg=self.C_CONTENT_BG)
            col_frame.grid(row=0, column=col_i, sticky="n", padx=10)
            cards_area.columnconfigure(col_i, weight=1)

            tk.Label(col_frame, text=grupo_titulo,
                     font=("Segoe UI", 11, "bold"),
                     bg=self.C_CONTENT_BG, fg=self.C_TEXT_DARK).pack(anchor="w", pady=(0, 8))

            for icon, label, method in items:
                self._add_card(col_frame, icon, label, method)

        # Footer
        footer = tk.Frame(content, bg=self.C_FOOTER, height=35)
        footer.grid(row=2, column=0, sticky="ew")
        footer.grid_propagate(False)
        tk.Label(footer, text="v1.0 — Sistema Hospitalario © 2026",
                 font=("Segoe UI", 9),
                 bg=self.C_FOOTER, fg=self.C_TEXT_LIGHT).pack(pady=8)

    def _add_card(self, parent, icon, label, method):
        card = tk.Frame(parent, bg=self.C_WHITE,
                        relief="flat", bd=0,
                        cursor="hand2")
        card.pack(fill="x", pady=4, ipady=6, ipadx=8)

        inner = tk.Frame(card, bg=self.C_WHITE)
        inner.pack(fill="x", padx=10, pady=4)

        lbl_i = tk.Label(inner, text=icon, font=("Segoe UI Emoji", 16),
                         bg=self.C_WHITE, fg=self.C_SIDEBAR_BG)
        lbl_i.pack(side="left", padx=(0, 10))

        lbl_t = tk.Label(inner, text=label, font=("Segoe UI", 11),
                         bg=self.C_WHITE, fg=self.C_TEXT_DARK, anchor="w")
        lbl_t.pack(side="left")

        all_w = [card, inner, lbl_i, lbl_t]

        def on_enter(e, w=all_w):
            for ww in w: ww.config(bg="#dbeafe")
            card.config(relief="groove")

        def on_leave(e, w=all_w):
            for ww in w: ww.config(bg=self.C_WHITE)
            card.config(relief="flat")

        def on_click(e=None, m=method):
            getattr(self, m)()

        for w in all_w:
            w.bind("<Enter>", on_enter)
            w.bind("<Leave>", on_leave)
            w.bind("<Button-1>", on_click)

    # ── Navegación ──────────────────────────────────────────────────────
    def _open_toplevel(self, ViewClass):
        self.withdraw()
        view = ViewClass(self)
        def on_close():
            view.destroy()
            self.deiconify()
        view.protocol("WM_DELETE_WINDOW", on_close)

    def abrir_dashboard(self):
        try:
            from views.dashboard import DashboardView
            self.destroy()
            DashboardView().mainloop()
        except Exception as e:
            messagebox.showerror("Error", f"Error al abrir Dashboard:\n{str(e)}")

    def abrir_pacientes(self):
        try:
            from views.pacientes import PacientesView
            self.destroy()
            PacientesView().mainloop()
        except Exception as e:
            messagebox.showerror("Error", f"Error al abrir Pacientes:\n{str(e)}")

    def abrir_citas(self):
        try:
            from views.citas_view import CitasView
            self._open_toplevel(CitasView)
        except Exception as e:
            messagebox.showerror("Error", f"Error al abrir Citas:\n{str(e)}")

    def abrir_facturacion(self):
        try:
            from views.facturacion_view import FacturacionView
            self._open_toplevel(FacturacionView)
        except Exception as e:
            messagebox.showerror("Error", f"Error al abrir Facturación:\n{str(e)}")

    def abrir_pagos(self):
        try:
            from views.pagos import PagosView
            self._open_toplevel(PagosView)
        except Exception as e:
            messagebox.showerror("Error", f"Error al abrir Pagos:\n{str(e)}")

    def abrir_caja_diaria(self):
        try:
            from views.caja_diaria import CajaDiariaView
            self._open_toplevel(CajaDiariaView)
        except Exception as e:
            messagebox.showerror("Error", f"Error al abrir Caja Diaria:\n{str(e)}")

    def abrir_cxc(self):
        try:
            from views.cxc import CxcView
            self._open_toplevel(CxcView)
        except Exception as e:
            messagebox.showerror("Error", f"Error al abrir Cuentas por Cobrar:\n{str(e)}")

    def abrir_reportes(self):
        try:
            from views.reportes import ReportesView
            self._open_toplevel(ReportesView)
        except Exception as e:
            messagebox.showerror("Error", f"Error al abrir Reportes:\n{str(e)}")

    def abrir_auditoria(self):
        try:
            from views.auditoria import AuditoriaView
            self._open_toplevel(AuditoriaView)
        except Exception as e:
            messagebox.showerror("Error", f"Error al abrir Auditoría:\n{str(e)}")

    def abrir_usuarios(self):
        try:
            from views.usuarios import UsuariosView
            self._open_toplevel(UsuariosView)
        except Exception as e:
            messagebox.showerror("Error", f"Error al abrir Usuarios:\n{str(e)}")

    def abrir_configuracion(self):
        try:
            from views.configuracion import ConfiguracionView
            self._open_toplevel(ConfiguracionView)
        except Exception as e:
            messagebox.showerror("Error", f"Error al abrir Configuración:\n{str(e)}")

    def salir_sistema(self):
        if messagebox.askyesno("Confirmar Salida",
                               "¿Estás seguro de que deseas salir del sistema?"):
            self.destroy()


if __name__ == "__main__":
    app = MenuPrincipal()
    app.mainloop()
