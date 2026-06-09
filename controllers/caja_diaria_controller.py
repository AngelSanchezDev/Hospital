import tkinter as tk
from tkinter import messagebox
from database.conexion import conexion

class CajaDiariaController:
    def __init__(self, view):
        self.view = view
        self._conexion = conexion
        
        self.view.btn_actualizar.config(command=self.cargar_datos)
        
        self.cargar_datos()

    def _cursor(self):
        return self._conexion.cursor()

    def cargar_datos(self):
        """Carga los ingresos pagados en el día actual."""
        for row in self.view.tree.get_children():
            self.view.tree.delete(row)
            
        try:
            cursor = self._cursor()
            # Seleccionar facturas PAGADAS del día de hoy
            sql = """
                SELECT f.numero_factura, p.nombres, p.apellidos, f.fecha_factura, f.total
                FROM Factura f
                JOIN Paciente p ON f.id_paciente = p.id_paciente
                WHERE f.estado_pago = 'PAGADO' 
                  AND CAST(f.fecha_factura AS DATE) = CAST(GETDATE() AS DATE)
                  AND f.eliminado = 0
                ORDER BY f.id_factura DESC
            """
            cursor.execute(sql)
            rows = cursor.fetchall()
            
            total_dia = 0.0
            
            for r in rows:
                numero = r[0]
                paciente = f"{r[1]} {r[2]}"
                fecha = r[3].strftime("%Y-%m-%d %H:%M") if r[3] else ""
                total = float(r[4])
                
                total_dia += total
                
                self.view.tree.insert("", "end", values=(
                    numero,
                    paciente,
                    fecha,
                    f"S/ {total:.2f}"
                ))
            
            # Actualizar etiqueta de total
            self.view.var_total.set(f"S/ {total_dia:.2f}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar la caja diaria: {str(e)}")
