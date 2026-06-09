import os
import sys
from pathlib import Path

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import tkinter as tk
from tkinter import ttk, messagebox
from fpdf import FPDF

from database.conexion import conexion
from models.factura import Factura
from models.detalle_factura import DetalleFactura
import session


class FacturacionController:
    def __init__(self, root):
        self.root = root
        self._conexion = conexion
        self._validar_conexion()
        self.setup_ui()

    def _validar_conexion(self):
        cursor = self._conexion.cursor()
        cursor.execute("SELECT 1")
        cursor.close()

    def _cursor(self):
        return self._conexion.cursor()

    def setup_ui(self):
        self.citas_dict = {}
        self.facturas_dict = {}
        self.facturas_all_dict = {}

        self.frame = ttk.Frame(self.root)
        self.frame.pack(padx=10, pady=10, fill="both", expand=True)
        self.frame.columnconfigure(1, weight=1)
        self.frame.columnconfigure(2, weight=1)
        self.frame.columnconfigure(3, weight=1)

        self.btn_volver = ttk.Button(self.frame, text="Volver al Menú", command=self.volver_al_menu)
        self.btn_volver.grid(row=0, column=0, pady=10, sticky="w")
        ttk.Label(self.frame, text=f"Registrado por: {session.get_resumen_usuario()}").grid(row=0, column=1, sticky="w")

        self.label_buscar_cita = ttk.Label(self.frame, text="Buscar Cita:")
        self.label_buscar_cita.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_buscar_cita = ttk.Entry(self.frame)
        self.entry_buscar_cita.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.entry_buscar_cita.bind("<KeyRelease>", self.filtrar_citas)

        self.label_cita = ttk.Label(self.frame, text="Cita:")
        self.label_cita.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.combo_cita = ttk.Combobox(self.frame, state="readonly")
        self.combo_cita.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        self.combo_cita.bind("<<ComboboxSelected>>", self._cargar_datos_cita)

        self.label_paciente = ttk.Label(self.frame, text="Paciente:")
        self.label_paciente.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.entry_paciente = ttk.Entry(self.frame, state="readonly")
        self.entry_paciente.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        self.label_servicio = ttk.Label(self.frame, text="Servicio/Consulta:")
        self.label_servicio.grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.entry_servicio = ttk.Entry(self.frame, state="readonly")
        self.entry_servicio.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

        self.label_costo = ttk.Label(self.frame, text="Costo (S/):")
        self.label_costo.grid(row=5, column=0, padx=5, pady=5, sticky="w")
        self.entry_costo = ttk.Entry(self.frame, state="readonly")
        self.entry_costo.grid(row=5, column=1, padx=5, pady=5, sticky="ew")

        self.label_subtotal = ttk.Label(self.frame, text="Subtotal (S/):")
        self.label_subtotal.grid(row=6, column=0, padx=5, pady=5, sticky="w")
        self.entry_subtotal = ttk.Entry(self.frame, state="readonly")
        self.entry_subtotal.grid(row=6, column=1, padx=5, pady=5, sticky="ew")

        self.label_igv = ttk.Label(self.frame, text="IGV (S/):")
        self.label_igv.grid(row=7, column=0, padx=5, pady=5, sticky="w")
        self.entry_igv = ttk.Entry(self.frame, state="readonly")
        self.entry_igv.grid(row=7, column=1, padx=5, pady=5, sticky="ew")

        self.label_total = ttk.Label(self.frame, text="Total (S/):")
        self.label_total.grid(row=8, column=0, padx=5, pady=5, sticky="w")
        self.entry_total = ttk.Entry(self.frame, state="readonly")
        self.entry_total.grid(row=8, column=1, padx=5, pady=5, sticky="ew")

        self.label_estado = ttk.Label(self.frame, text="Estado Pago:")
        self.label_estado.grid(row=9, column=0, padx=5, pady=5, sticky="w")
        self.combo_estado_pago = ttk.Combobox(self.frame, values=["PENDIENTE", "PAGADO", "ANULADO"], state="readonly")
        self.combo_estado_pago.grid(row=9, column=1, padx=5, pady=5, sticky="ew")

        self.btn_emitir = tk.Button(self.frame, text="Emitir factura", command=self.emitir_factura, bg="#3182ce", fg="white", activebackground="#2563eb", activeforeground="white", relief="raised", bd=2)
        self.btn_emitir.grid(row=10, column=0, pady=15, sticky="ew")

        self.btn_editar = tk.Button(self.frame, text="Editar", command=self.editar_factura, bg="#3182ce", fg="white", activebackground="#2563eb", activeforeground="white", relief="raised", bd=2)
        self.btn_editar.grid(row=10, column=1, pady=15, sticky="ew")

        self.btn_anular = tk.Button(self.frame, text="Anular", command=self.anular_factura, bg="#3182ce", fg="white", activebackground="#2563eb", activeforeground="white", relief="raised", bd=2)
        self.btn_anular.grid(row=10, column=2, pady=15, sticky="ew")

        self.btn_pdf = tk.Button(self.frame, text="Generar PDF", command=self.generar_pdf, bg="#3182ce", fg="white", activebackground="#2563eb", activeforeground="white", relief="raised", bd=2)
        self.btn_pdf.grid(row=10, column=3, pady=15, sticky="ew")

        self.label_facturas = ttk.Label(self.frame, text="Facturas anteriores:")
        self.label_facturas.grid(row=11, column=0, padx=5, pady=(15, 5), sticky="w")
        self.entry_buscar_factura = ttk.Entry(self.frame)
        self.entry_buscar_factura.grid(row=11, column=1, padx=5, pady=(15, 5), sticky="ew")
        self.entry_buscar_factura.bind("<KeyRelease>", self.filtrar_facturas)

        self.combo_facturas = ttk.Combobox(self.frame, state="readonly")
        self.combo_facturas.grid(row=12, column=0, columnspan=2, padx=5, pady=(5, 5), sticky="ew")
        self.combo_facturas.bind("<<ComboboxSelected>>", self._cargar_factura_existente)

        self.tree_detalle = ttk.Treeview(
            self.frame,
            columns=("campo", "valor"),
            show="headings",
            height=8
        )
        self.tree_detalle.heading("campo", text="Campo")
        self.tree_detalle.heading("valor", text="Valor")
        self.tree_detalle.column("campo", width=180, anchor="w")
        self.tree_detalle.column("valor", width=420, anchor="w")
        self.tree_detalle.grid(row=13, column=0, columnspan=3, padx=5, pady=(10, 5), sticky="nsew")
        self.frame.rowconfigure(13, weight=1)

        self._cargar_citas()
        self._cargar_facturas()
        self._set_modo_nuevo()

    def volver_al_menu(self):
        if hasattr(self.root, "master") and self.root.master:
            self.root.master.deiconify()
        self.root.destroy()

    def _cursor(self):
        return self._conexion.cursor()

    def filtrar_citas(self, event):
        self._cargar_citas(self.entry_buscar_cita.get().lower())

    def filtrar_facturas(self, event):
        self._cargar_facturas(self.entry_buscar_factura.get().lower())

    def _obtener_citas(self, termino=""):
        cursor = self._cursor()
        sql = """
        SELECT r.id_reserva, r.id_paciente, p.nombres, p.apellidos, r.titulo, r.precio
        FROM Reservacion r
        JOIN Paciente p ON r.id_paciente = p.id_paciente
        LEFT JOIN Factura f ON f.id_reserva = r.id_reserva AND f.eliminado = 0
        WHERE r.eliminado = 0
          AND f.id_factura IS NULL
          AND (
                p.nombres LIKE ? OR
                p.apellidos LIKE ? OR
                r.titulo LIKE ? OR
                CAST(r.id_reserva AS VARCHAR(20)) LIKE ?
          )
        ORDER BY r.id_reserva DESC
        """
        param = f"%{termino}%"
        cursor.execute(sql, (param, param, param, param))
        rows = cursor.fetchall()
        return {f"Cita #{row[0]} - {row[2]} {row[3]} - {row[4]}": row for row in rows}

    def _cargar_citas(self, termino=""):
        self.citas_dict = self._obtener_citas(termino)
        self.combo_cita["values"] = list(self.citas_dict.keys())
        self.combo_cita.set("")

    def _obtener_facturas(self, termino=""):
        cursor = self._cursor()
        sql = """
        SELECT f.id_factura, f.numero_factura, p.nombres, p.apellidos, r.titulo, f.total, f.estado_pago
        FROM Factura f
        JOIN Paciente p ON p.id_paciente = f.id_paciente
        LEFT JOIN Reservacion r ON r.id_reserva = f.id_reserva
        WHERE f.eliminado = 0
          AND (
                f.numero_factura LIKE ? OR
                p.nombres LIKE ? OR
                p.apellidos LIKE ? OR
                ISNULL(r.titulo, '') LIKE ? OR
                CAST(f.id_factura AS VARCHAR(20)) LIKE ?
          )
        ORDER BY f.id_factura DESC
        """
        param = f"%{termino}%"
        cursor.execute(sql, (param, param, param, param, param))
        rows = cursor.fetchall()
        return {
            f"Factura #{row[0]} - {row[1]} - {row[2]} {row[3]} - {row[4] or 'Sin servicio'} - S/ {float(row[5]):.2f} - {row[6]}": row
            for row in rows
        }

    def _cargar_facturas(self, termino=""):
        self.facturas_dict = self._obtener_facturas(termino)
        self.facturas_all_dict = dict(self.facturas_dict)
        self.combo_facturas["values"] = list(self.facturas_dict.keys())
        self.combo_facturas.set("")

    def _set_modo_nuevo(self):
        for entry in (self.entry_paciente, self.entry_servicio, self.entry_costo, self.entry_subtotal, self.entry_igv, self.entry_total):
            entry.config(state="readonly")
        self.combo_estado_pago.config(state="readonly")

    def _set_modo_edicion(self):
        for entry in (self.entry_paciente, self.entry_servicio, self.entry_costo, self.entry_subtotal, self.entry_igv, self.entry_total):
            entry.config(state="readonly")
        self.combo_estado_pago.config(state="readonly")

    def _cargar_datos_cita(self, event=None):
        cita_seleccionada = self.combo_cita.get()
        if not cita_seleccionada:
            return
        cita_data = self.citas_dict[cita_seleccionada]
        self._limpiar_campos()
        self._llenar_campos(
            paciente=f"{cita_data[2]} {cita_data[3]}",
            servicio=cita_data[4],
            costo=float(cita_data[5]),
            estado_pago="PENDIENTE"
        )
        self._set_modo_nuevo()

    def _cargar_factura_existente(self, event=None):
        factura_seleccionada = self.combo_facturas.get()
        if not factura_seleccionada:
            return
        factura_data = self.facturas_dict[factura_seleccionada]
        cursor = self._cursor()
        cursor.execute("""
            SELECT f.id_factura, f.numero_factura, p.nombres, p.apellidos, r.titulo, f.subtotal, f.igv, f.total, f.estado_pago
            FROM Factura f
            JOIN Paciente p ON p.id_paciente = f.id_paciente
            LEFT JOIN Reservacion r ON r.id_reserva = f.id_reserva
            WHERE f.id_factura = ?
        """, (factura_data[0],))
        row = cursor.fetchone()
        if not row:
            return
        self._limpiar_campos()
        self._llenar_detalle_factura(row)
        self._llenar_campos(
            paciente=f"{row[2]} {row[3]}",
            servicio=row[4] or "",
            costo=float(row[5]),
            subtotal=float(row[5]),
            igv=float(row[6]),
            total=float(row[7]),
            estado_pago=row[8]
        )
        self.combo_estado_pago.set(row[8])
        self._set_modo_edicion()

    def _llenar_detalle_factura(self, row):
        for item in self.tree_detalle.get_children():
            self.tree_detalle.delete(item)
        detalles = [
            ("ID Factura", row[0]),
            ("Número", row[1]),
            ("Paciente", f"{row[2]} {row[3]}"),
            ("Servicio", row[4] or "Sin servicio"),
            ("Subtotal", f"S/ {float(row[5]):.2f}"),
            ("IGV", f"S/ {float(row[6]):.2f}"),
            ("Total", f"S/ {float(row[7]):.2f}"),
            ("Estado pago", row[8]),
        ]
        for campo, valor in detalles:
            self.tree_detalle.insert("", "end", values=(campo, valor))

    def _limpiar_campos(self):
        for entry in (self.entry_paciente, self.entry_servicio, self.entry_costo, self.entry_subtotal, self.entry_igv, self.entry_total):
            entry.config(state="normal")
            entry.delete(0, "end")
            entry.config(state="readonly")
        self.combo_estado_pago.set("")

    def _llenar_campos(self, paciente="", servicio="", costo=0, subtotal=None, igv=None, total=None, estado_pago="PENDIENTE"):
        if subtotal is None:
            subtotal = costo
        if igv is None:
            igv = round(float(subtotal) * 0.18, 2)
        if total is None:
            total = round(float(subtotal) + float(igv), 2)

        values = {
            self.entry_paciente: paciente,
            self.entry_servicio: servicio,
            self.entry_costo: f"{float(costo):.2f}",
            self.entry_subtotal: f"{float(subtotal):.2f}",
            self.entry_igv: f"{float(igv):.2f}",
            self.entry_total: f"{float(total):.2f}",
        }
        for entry, value in values.items():
            entry.config(state="normal")
            entry.delete(0, "end")
            entry.insert(0, value)
            entry.config(state="readonly")
        self.combo_estado_pago.set(estado_pago)

    def emitir_factura(self):
        cita_seleccionada = self.combo_cita.get()
        if not cita_seleccionada:
            messagebox.showerror("Error", "Debe seleccionar una cita.")
            return

        cita_data = self.citas_dict[cita_seleccionada]
        id_reservacion = cita_data[0]
        id_paciente = cita_data[1]

        cursor = self._cursor()
        try:
            cursor.execute("SELECT TOP 1 id_factura FROM Factura WHERE id_reserva = ? AND eliminado = 0", (id_reservacion,))
            if cursor.fetchone():
                messagebox.showerror("Error", "Esta cita ya fue facturada. No se puede emitir dos veces.")
                return

            try:
                subtotal = float(self.entry_subtotal.get())
                igv = float(self.entry_igv.get())
                total = float(self.entry_total.get())
            except ValueError:
                messagebox.showerror("Error", "Subtotal, IGV y Total deben ser numéricos.")
                return

            estado_pago = self.combo_estado_pago.get().strip()
            if estado_pago not in ("PENDIENTE", "PAGADO", "ANULADO"):
                messagebox.showerror("Error", "Debe seleccionar el estado de pago.")
                return

            cursor.execute("SELECT COUNT(*) FROM Factura")
            count = cursor.fetchone()[0] + 1
            numero_factura = f"FAC-2026-{count:05d}"

            factura = Factura(
                numero_factura=numero_factura,
                id_paciente=id_paciente,
                id_reserva=id_reservacion,
                fecha_factura=self._fecha_actual(),
                subtotal=subtotal,
                igv=igv,
                total=total,
                estado_pago=estado_pago
            )
            id_factura = factura.save(cursor)
            if not id_factura:
                raise Exception("No se pudo recuperar el ID de la factura creada.")

            detalle_factura = DetalleFactura(
                id_factura=id_factura,
                descripcion=cita_data[4],
                cantidad=1,
                precio_unitario=float(cita_data[5]),
                subtotal=float(cita_data[5])
            )
            detalle_factura.save(cursor)

            cursor.execute("UPDATE Reservacion SET id_estado = 2 WHERE id_reserva = ?", (id_reservacion,))
            self._conexion.commit()
            self._cargar_facturas()
            self._cargar_citas(self.entry_buscar_cita.get().lower())
            messagebox.showinfo("Éxito", "Factura emitida exitosamente.")
        except Exception as e:
            self._conexion.rollback()
            messagebox.showerror("Error", f"Error al guardar la factura: {str(e)}")

    def editar_factura(self):
        factura_seleccionada = self.combo_facturas.get()
        if not factura_seleccionada:
            messagebox.showerror("Error", "Debe seleccionar una factura anterior para editar.")
            return

        factura_data = self.facturas_dict[factura_seleccionada]
        id_factura = factura_data[0]

        estado_pago = self.combo_estado_pago.get().strip()
        if estado_pago not in ("PENDIENTE", "PAGADO"):
            messagebox.showerror("Error", "Debe seleccionar el estado de pago.")
            return

        try:
            cursor = self._cursor()
            cursor.execute("""
                UPDATE Factura
                SET estado_pago = ?
                WHERE id_factura = ? AND eliminado = 0
            """, (estado_pago, id_factura))
            self._conexion.commit()
            self._cargar_facturas(self.entry_buscar_factura.get().lower())
            messagebox.showinfo("Éxito", "Estado de factura actualizado exitosamente.")
        except Exception as e:
            self._conexion.rollback()
            messagebox.showerror("Error", f"Error al editar la factura: {str(e)}")

    def anular_factura(self):
        factura_seleccionada = self.combo_facturas.get()
        if not factura_seleccionada:
            messagebox.showerror("Error", "Debe seleccionar una factura anterior para anular.")
            return

        factura_data = self.facturas_dict[factura_seleccionada]
        id_factura = factura_data[0]

        if messagebox.askyesno("Confirmar", "¿Deseas marcar esta factura como ANULADA?"):
            try:
                cursor = self._cursor()
                cursor.execute("""
                    UPDATE Factura
                    SET estado_pago = 'ANULADO'
                    WHERE id_factura = ? AND eliminado = 0
                """, (id_factura,))
                self._conexion.commit()
                self._cargar_facturas(self.entry_buscar_factura.get().lower())
                self.combo_estado_pago.set("ANULADO")
                messagebox.showinfo("Éxito", "Factura anulada exitosamente.")
            except Exception as e:
                self._conexion.rollback()
                messagebox.showerror("Error", f"Error al anular la factura: {str(e)}")

    def generar_pdf(self):
        factura_seleccionada = self.combo_facturas.get()
        if not factura_seleccionada:
            messagebox.showerror("Error", "Debe seleccionar una factura para generar el PDF.")
            return

        factura_data = self.facturas_dict.get(factura_seleccionada)
        if not factura_data:
            messagebox.showerror("Error", "No se encontró la factura seleccionada.")
            return

        try:
            cursor = self._cursor()
            cursor.execute("""
                SELECT f.id_factura, f.numero_factura, f.fecha_factura, f.subtotal, f.igv, f.total, f.estado_pago,
                       p.nombres, p.apellidos, p.email, p.telefono,
                       r.titulo, r.fecha_cita, r.hora_cita
                FROM Factura f
                JOIN Paciente p ON p.id_paciente = f.id_paciente
                LEFT JOIN Reservacion r ON r.id_reserva = f.id_reserva
                WHERE f.id_factura = ?
            """, (factura_data[0],))
            header = cursor.fetchone()
            if not header:
                messagebox.showerror("Error", "No se pudo obtener la información de la factura.")
                return

            cursor.execute("""
                SELECT descripcion, cantidad, precio_unitario, subtotal
                FROM DetalleFactura
                WHERE id_factura = ?
            """, (factura_data[0],))
            detalles = cursor.fetchall()

            reports_dir = Path(__file__).resolve().parent.parent / "reports" / "pdf"
            reports_dir.mkdir(parents=True, exist_ok=True)
            pdf_path = reports_dir / f"Factura_{header[1]}.pdf"

            pdf = FPDF()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()
            pdf.set_font("Helvetica", "B", 16)
            pdf.cell(0, 10, "FACTURA", ln=True, align="C")
            pdf.ln(4)

            pdf.set_font("Helvetica", "", 11)
            pdf.cell(0, 8, f"Numero: {header[1]}", ln=True)
            pdf.cell(0, 8, f"Fecha: {header[2]}", ln=True)
            pdf.cell(0, 8, f"Estado de pago: {header[6]}", ln=True)
            pdf.cell(0, 8, f"Paciente: {header[7]} {header[8]}", ln=True)
            pdf.cell(0, 8, f"Email: {header[9] or ''}", ln=True)
            pdf.cell(0, 8, f"Telefono: {header[10] or ''}", ln=True)
            pdf.cell(0, 8, f"Servicio: {header[11] or ''}", ln=True)
            pdf.cell(0, 8, f"Fecha cita: {header[12] or ''}", ln=True)
            pdf.cell(0, 8, f"Hora cita: {header[13] or ''}", ln=True)
            pdf.ln(4)

            pdf.set_font("Helvetica", "B", 11)
            pdf.cell(90, 8, "Descripcion", border=1)
            pdf.cell(20, 8, "Cant.", border=1, align="C")
            pdf.cell(40, 8, "P.Unit.", border=1, align="R")
            pdf.cell(40, 8, "Subtotal", border=1, ln=True, align="R")
            pdf.set_font("Helvetica", "", 11)
            for desc, cantidad, precio_unitario, subtotal in detalles:
                pdf.cell(90, 8, str(desc)[:45], border=1)
                pdf.cell(20, 8, str(cantidad), border=1, align="C")
                pdf.cell(40, 8, f"S/ {float(precio_unitario):.2f}", border=1, align="R")
                pdf.cell(40, 8, f"S/ {float(subtotal):.2f}", border=1, ln=True, align="R")

            pdf.ln(5)
            pdf.set_font("Helvetica", "B", 11)
            pdf.cell(0, 8, f"Subtotal: S/ {float(header[3]):.2f}", ln=True, align="R")
            pdf.cell(0, 8, f"IGV: S/ {float(header[4]):.2f}", ln=True, align="R")
            pdf.cell(0, 8, f"Total: S/ {float(header[5]):.2f}", ln=True, align="R")

            pdf.output(str(pdf_path))
            messagebox.showinfo("Éxito", f"PDF generado correctamente:\n{pdf_path}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el PDF: {str(e)}")

    def _fecha_actual(self):
        from datetime import date
        return date.today().isoformat()
