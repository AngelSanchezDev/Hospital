import os
from pathlib import Path
from tkinter import messagebox
from fpdf import FPDF
from database.conexion import conexion
from datetime import datetime

class ReporteController:
    def __init__(self, view):
        self.view = view
        self._conexion = conexion
        
        self.view.btn_pacientes.config(command=self.reporte_pacientes)
        self.view.btn_ingresos.config(command=self.reporte_ingresos)
        self.view.btn_auditoria.config(command=self.reporte_auditoria)
        self.view.btn_personal.config(command=self.reporte_personal)

    def _cursor(self):
        return self._conexion.cursor()
        
    def _get_reports_dir(self):
        base_dir = Path(__file__).resolve().parent.parent / "reports" / "reports"
        base_dir.mkdir(parents=True, exist_ok=True)
        return base_dir
        
    def _crear_pdf(self, titulo, headers, data, filename):
        try:
            pdf = FPDF(orientation="L") # Horizontal
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()
            
            # Titulo
            pdf.set_font("Helvetica", "B", 16)
            pdf.cell(0, 10, titulo, ln=True, align="C")
            pdf.ln(5)
            
            pdf.set_font("Helvetica", "", 10)
            fecha_str = datetime.now().strftime("%Y-%m-%d %H:%M")
            pdf.cell(0, 10, f"Fecha de generacion: {fecha_str}", ln=True, align="R")
            
            # Tabla (Headers)
            pdf.set_font("Helvetica", "B", 10)
            col_widths = [270 / len(headers)] * len(headers) # Aproximadamente para A4 horizontal
            
            for i, header in enumerate(headers):
                pdf.cell(col_widths[i], 10, header, border=1, align="C")
            pdf.ln()
            
            # Tabla (Datos)
            pdf.set_font("Helvetica", "", 9)
            for row in data:
                for i, col in enumerate(row):
                    pdf.cell(col_widths[i], 10, str(col)[:30], border=1) # Truncar largos
                pdf.ln()
            
            save_path = self._get_reports_dir() / filename
            pdf.output(str(save_path))
            
            messagebox.showinfo("Éxito", f"Reporte generado exitosamente:\n{save_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar reporte: {str(e)}")

    def reporte_pacientes(self):
        try:
            cursor = self._cursor()
            cursor.execute("SELECT nombres, apellidos, telefono, email, genero, estado FROM Paciente WHERE eliminado=0")
            rows = cursor.fetchall()
            
            data = [[r[0], r[1], r[2] or "N/A", r[3] or "N/A", r[4], "Activo" if r[5] else "Inactivo"] for r in rows]
            headers = ["Nombres", "Apellidos", "Teléfono", "Email", "Género", "Estado"]
            filename = f"Reporte_Pacientes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            
            self._crear_pdf("Directorio de Pacientes", headers, data, filename)
        except Exception as e:
            messagebox.showerror("Error", f"Error de BD: {str(e)}")

    def reporte_ingresos(self):
        try:
            cursor = self._cursor()
            cursor.execute("SELECT numero_factura, fecha_factura, total, estado_pago FROM Factura WHERE eliminado=0 ORDER BY fecha_factura DESC")
            rows = cursor.fetchall()
            
            data = [[r[0], r[1].strftime('%Y-%m-%d %H:%M'), f"S/ {float(r[2]):.2f}", r[3]] for r in rows]
            headers = ["N° Factura", "Fecha Emisión", "Monto Total", "Estado"]
            filename = f"Reporte_Ingresos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            
            self._crear_pdf("Historial de Ingresos", headers, data, filename)
        except Exception as e:
            messagebox.showerror("Error", f"Error de BD: {str(e)}")
            
    def reporte_auditoria(self):
        try:
            cursor = self._cursor()
            cursor.execute("SELECT TOP 50 fecha, accion, tabla, usuario_bd FROM Auditoria ORDER BY fecha DESC")
            rows = cursor.fetchall()
            
            data = [[r[0].strftime('%Y-%m-%d %H:%M'), r[1], r[2], r[3]] for r in rows]
            headers = ["Fecha", "Acción", "Tabla Afectada", "Usuario BD"]
            filename = f"Reporte_AuditoriaReciente_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            
            self._crear_pdf("Reporte de Auditoría Reciente (Últimos 50)", headers, data, filename)
        except Exception as e:
            messagebox.showerror("Error", f"Error de BD: {str(e)}")
            
    def reporte_personal(self):
        try:
            cursor = self._cursor()
            cursor.execute("SELECT username, nombres, apellidos, email, estado_activo FROM Usuario WHERE eliminado=0")
            rows = cursor.fetchall()
            
            data = [[r[0], r[1], r[2], r[3] or "N/A", "Activo" if r[4] else "Inactivo"] for r in rows]
            headers = ["Username", "Nombres", "Apellidos", "Email", "Estado"]
            filename = f"Reporte_Personal_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            
            self._crear_pdf("Directorio del Personal (Usuarios)", headers, data, filename)
        except Exception as e:
            messagebox.showerror("Error", f"Error de BD: {str(e)}")
