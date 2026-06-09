import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from controllers.dashboard_controller import DashboardController
from views.menu_principal import MenuPrincipal

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class DashboardView(tk.Tk):
    # Paleta
    C_BG       = "#eaf4fb"
    C_HEADER   = "#1565c0"
    C_WHITE    = "#ffffff"
    C_TEXT     = "#1f2937"
    C_SIDEBAR  = "#0f4c81"
    C_FOOTER   = "#0d3a63"
    C_TL_LIGHT = "#d0e8ff"

    KPI_COLORS = {
        "facturado_hoy":        ("#dbeafe", "#1565c0", "💵"),
        "facturado_mes":        ("#dbeafe", "#1565c0", "📅"),
        "cobrado_hoy":          ("#dcfce7", "#166534", "✅"),
        "cobrado_mes":          ("#dcfce7", "#166534", "📈"),
        "facturas_pendientes":  ("#fef9c3", "#854d0e", "⚠️"),
        "reservaciones_activas":("#ede9fe", "#5b21b6", "📋"),
        "citas_hoy":            ("#fce7f3", "#9d174d", "🗓️"),
        "total_pacientes":      ("#e0f2fe", "#0369a1", "👥"),
    }

    KPI_LABELS = {
        "facturado_hoy":        "Facturado Hoy",
        "facturado_mes":        "Facturado Mes",
        "cobrado_hoy":          "Cobrado Hoy",
        "cobrado_mes":          "Cobrado Mes",
        "facturas_pendientes":  "Facturas Pendientes",
        "reservaciones_activas":"Reservas Activas",
        "citas_hoy":            "Citas Hoy",
        "total_pacientes":      "Total Pacientes",
    }

    MONEY_KEYS = {"facturado_hoy", "facturado_mes", "cobrado_hoy", "cobrado_mes"}

    def __init__(self):
        super().__init__()
        self.title("Dashboard Financiero — Hospital")
        self.geometry("1400x860")
        self.configure(bg=self.C_BG)

        self.controller = None
        self.indicator_labels = {}
        self.ingresos_canvas = None
        self.tipo_pago_canvas = None

        self._init_controller()
        if self.controller:
            self._build()
            self.refresh()

    # ── Init ────────────────────────────────────────────────────────────
    def _init_controller(self):
        try:
            self.controller = DashboardController()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo conectar:\n{str(e)}")

    def regreso_menu(self):
        self.destroy()
        MenuPrincipal().mainloop()

    # ── Build ────────────────────────────────────────────────────────────
    def _build(self):
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self._build_header()
        self._build_body()
        self._build_footer()

    def _build_header(self):
        hdr = tk.Frame(self, bg=self.C_HEADER, height=65)
        hdr.grid(row=0, column=0, sticky="ew")
        hdr.grid_propagate(False)

        tk.Label(hdr, text="📊  Dashboard Financiero",
                 font=("Segoe UI", 17, "bold"),
                 bg=self.C_HEADER, fg=self.C_WHITE).pack(side="left", padx=25, pady=15)

        btn_excel = tk.Button(hdr, text="⬇ Exportar Excel",
                              command=self._exportar_excel,
                              bg="#22c55e", fg="white",
                              font=("Segoe UI", 10, "bold"),
                              relief="flat", cursor="hand2",
                              padx=12, pady=6)
        btn_excel.pack(side="right", padx=10, pady=12)

        btn_refresh = tk.Button(hdr, text="🔄 Actualizar",
                                command=self.refresh,
                                bg="#3b82f6", fg="white",
                                font=("Segoe UI", 10, "bold"),
                                relief="flat", cursor="hand2",
                                padx=12, pady=6)
        btn_refresh.pack(side="right", padx=5, pady=12)

        btn_volver = tk.Button(hdr, text="← Menú",
                               command=self.regreso_menu,
                               bg="#6b7280", fg="white",
                               font=("Segoe UI", 10, "bold"),
                               relief="flat", cursor="hand2",
                               padx=12, pady=6)
        btn_volver.pack(side="right", padx=5, pady=12)

    def _build_body(self):
        body = tk.Frame(self, bg=self.C_BG)
        body.grid(row=1, column=0, sticky="nsew", padx=20, pady=15)
        body.columnconfigure(0, weight=1)
        body.rowconfigure(1, weight=1)
        body.rowconfigure(2, weight=1)

        self._build_kpi_strip(body)       # row 0
        self._build_charts_row(body)      # row 1
        self._build_tables_row(body)      # row 2

    def _build_footer(self):
        ft = tk.Frame(self, bg=self.C_FOOTER, height=32)
        ft.grid(row=2, column=0, sticky="ew")
        ft.grid_propagate(False)
        tk.Label(ft, text="v1.0 — Sistema Hospitalario © 2026",
                 font=("Segoe UI", 9),
                 bg=self.C_FOOTER, fg=self.C_TL_LIGHT).pack(pady=6)

    # ── KPI strip ────────────────────────────────────────────────────────
    def _build_kpi_strip(self, parent):
        strip = tk.Frame(parent, bg=self.C_BG)
        strip.grid(row=0, column=0, sticky="ew", pady=(0, 12))

        keys = list(self.KPI_COLORS.keys())
        for col_i, key in enumerate(keys):
            bg, fg, icon = self.KPI_COLORS[key]
            label_text   = self.KPI_LABELS[key]

            card = tk.Frame(strip, bg=bg, bd=0, relief="flat")
            card.grid(row=0, column=col_i, padx=6, sticky="nsew")
            strip.columnconfigure(col_i, weight=1)

            tk.Label(card, text=icon, font=("Segoe UI Emoji", 18),
                     bg=bg).pack(pady=(10, 0))
            tk.Label(card, text=label_text, font=("Segoe UI", 9),
                     bg=bg, fg=fg).pack()
            val_lbl = tk.Label(card, text="—",
                               font=("Segoe UI", 14, "bold"),
                               bg=bg, fg=fg)
            val_lbl.pack(pady=(2, 10))

            self.indicator_labels[key] = val_lbl

    # ── Gráficos ─────────────────────────────────────────────────────────
    def _build_charts_row(self, parent):
        row = tk.Frame(parent, bg=self.C_BG)
        row.grid(row=1, column=0, sticky="nsew", pady=(0, 12))
        row.columnconfigure(0, weight=2)
        row.columnconfigure(1, weight=1)
        row.rowconfigure(0, weight=1)

        self.ingresos_frame = tk.LabelFrame(row, text=" Ingresos últimos 7 días ",
                                            bg=self.C_WHITE, fg=self.C_SIDEBAR,
                                            font=("Segoe UI", 10, "bold"))
        self.ingresos_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

        self.tipo_pago_frame = tk.LabelFrame(row, text=" Distribución por tipo de pago ",
                                             bg=self.C_WHITE, fg=self.C_SIDEBAR,
                                             font=("Segoe UI", 10, "bold"))
        self.tipo_pago_frame.grid(row=0, column=1, sticky="nsew")

    # ── Tablas ───────────────────────────────────────────────────────────
    def _build_tables_row(self, parent):
        row = tk.Frame(parent, bg=self.C_BG)
        row.grid(row=2, column=0, sticky="nsew")
        row.columnconfigure(0, weight=1)
        row.columnconfigure(1, weight=1)
        row.rowconfigure(0, weight=1)

        # Citas del día
        citas_lf = tk.LabelFrame(row, text=" 🗓️  Citas de Hoy ",
                                 bg=self.C_WHITE, fg=self.C_SIDEBAR,
                                 font=("Segoe UI", 10, "bold"))
        citas_lf.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

        cols_citas = ("hora", "paciente", "medico", "estado")
        self.tree_citas = ttk.Treeview(citas_lf, columns=cols_citas,
                                        show="headings", height=7)
        for col, head, w in [
            ("hora",     "Hora",    70),
            ("paciente", "Paciente",180),
            ("medico",   "Médico",  180),
            ("estado",   "Estado",   90),
        ]:
            self.tree_citas.heading(col, text=head)
            self.tree_citas.column(col, width=w, anchor="center" if col in ("hora","estado") else "w")
        self.tree_citas.pack(fill="both", expand=True, padx=8, pady=8)

        # Últimas facturas
        facturas_lf = tk.LabelFrame(row, text=" 🧾  Últimas Facturas ",
                                    bg=self.C_WHITE, fg=self.C_SIDEBAR,
                                    font=("Segoe UI", 10, "bold"))
        facturas_lf.grid(row=0, column=1, sticky="nsew")

        cols_fac = ("numero", "paciente", "total", "estado", "fecha")
        self.tree_facturas = ttk.Treeview(facturas_lf, columns=cols_fac,
                                           show="headings", height=7)
        for col, head, w in [
            ("numero",   "N° Factura", 110),
            ("paciente", "Paciente",   160),
            ("total",    "Total S/",    80),
            ("estado",   "Estado",      80),
            ("fecha",    "Fecha",        85),
        ]:
            self.tree_facturas.heading(col, text=head)
            self.tree_facturas.column(col, width=w,
                                      anchor="e" if col == "total" else
                                      "center" if col in ("estado","fecha","numero") else "w")
        self.tree_facturas.pack(fill="both", expand=True, padx=8, pady=8)

        # Tags de color por estado
        for tree in (self.tree_citas, self.tree_facturas):
            tree.tag_configure("pendiente", background="#fef9c3")
            tree.tag_configure("pagado",    background="#dcfce7")
            tree.tag_configure("anulado",   background="#fee2e2")

    # ── Refresh ──────────────────────────────────────────────────────────
    def refresh(self):
        if not self.controller:
            return

        # KPIs
        try:
            indicadores = self.controller.obtener_indicadores()
            for key, lbl in self.indicator_labels.items():
                val = indicadores.get(key, 0)
                texto = f"S/ {float(val):,.2f}" if key in self.MONEY_KEYS else f"{int(val):,}"
                lbl.config(text=texto)
        except Exception as e:
            messagebox.showerror("Error", f"Error en KPIs:\n{str(e)}")

        # Gráfico de ingresos
        try:
            labels, values = self.controller.ingresos_por_dia()
            self._render_ingresos(labels, values)
        except Exception as e:
            self._chart_error(self.ingresos_frame, str(e))

        # Gráfico de tipo de pago
        try:
            pagos = self.controller.pagos_por_tipo()
            self._render_tipo_pago(pagos)
        except Exception as e:
            self._chart_error(self.tipo_pago_frame, str(e))

        # Tabla de citas
        try:
            self.tree_citas.delete(*self.tree_citas.get_children())
            for row in self.controller.ultimas_citas_hoy():
                hora, pac, med, estado = row
                tag = estado.lower() if estado else ""
                self.tree_citas.insert("", "end",
                                       values=(str(hora)[:5], pac, med, estado),
                                       tags=(tag,))
        except Exception as e:
            pass  # No bloquear si no hay citas

        # Tabla de facturas
        try:
            self.tree_facturas.delete(*self.tree_facturas.get_children())
            for row in self.controller.ultimas_facturas():
                num, pac, total, estado, fecha = row
                tag = estado.lower() if estado else ""
                self.tree_facturas.insert("", "end",
                                          values=(num, pac, f"{float(total):.2f}",
                                                  estado, str(fecha)),
                                          tags=(tag,))
        except Exception as e:
            pass

    # ── Renders ───────────────────────────────────────────────────────────
    def _render_ingresos(self, labels, values):
        for w in self.ingresos_frame.winfo_children():
            w.destroy()
        fig = Figure(figsize=(6, 2.8), dpi=95, facecolor=self.C_WHITE)
        ax  = fig.add_subplot(111)
        bars = ax.bar(labels, values, color="#1565c0", width=0.5)
        ax.set_facecolor(self.C_BG)
        ax.set_ylabel("S/.", fontsize=9)
        ax.grid(axis="y", linestyle="--", alpha=0.4)
        ax.tick_params(labelsize=8)
        for bar, val in zip(bars, values):
            if val > 0:
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
                        f"{val:.0f}", ha="center", va="bottom", fontsize=7)
        fig.tight_layout()
        cv = FigureCanvasTkAgg(fig, master=self.ingresos_frame)
        cv.draw()
        cv.get_tk_widget().pack(fill="both", expand=True)
        self.ingresos_canvas = cv

    def _render_tipo_pago(self, pagos):
        for w in self.tipo_pago_frame.winfo_children():
            w.destroy()
        fig = Figure(figsize=(4, 2.8), dpi=95, facecolor=self.C_WHITE)
        ax  = fig.add_subplot(111)
        labels  = [p[0] for p in pagos]
        valores = [p[1] for p in pagos]
        colors  = ["#1565c0", "#22c55e", "#f59e0b", "#ef4444", "#8b5cf6", "#06b6d4"]
        if valores and sum(valores) > 0:
            ax.pie(valores, labels=labels, autopct="%1.1f%%",
                   startangle=140, colors=colors[:len(pagos)],
                   textprops={"fontsize": 8})
        else:
            ax.text(0.5, 0.5, "Sin datos", ha="center", va="center", fontsize=11)
        fig.tight_layout()
        cv = FigureCanvasTkAgg(fig, master=self.tipo_pago_frame)
        cv.draw()
        cv.get_tk_widget().pack(fill="both", expand=True)
        self.tipo_pago_canvas = cv

    def _chart_error(self, parent, msg):
        for w in parent.winfo_children():
            w.destroy()
        tk.Label(parent, text=f"Sin datos\n{msg[:60]}",
                 bg=self.C_WHITE, fg="#9ca3af",
                 font=("Segoe UI", 9)).pack(expand=True)

    # ── Excel ─────────────────────────────────────────────────────────────
    def _exportar_excel(self):
        try:
            path = self.controller.exportar_excel()
            messagebox.showinfo("Éxito",
                                f"Archivo Excel generado exitosamente:\n{path}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar:\n{str(e)}")


if __name__ == "__main__":
    app = DashboardView()
    app.mainloop()
