import tkinter as tk
from tkinter import messagebox
from database.conexion import conexion

class CxcController:
    def __init__(self, view):
        self.view = view
        self._conexion = conexion
        
        self.view.btn_actualizar.config(command=self.cargar_datos)
        self.view.btn_pagar.config(command=self.marcar_como_pagado)
        
        self.cargar_datos()

    def _cursor(self):
        return self._conexion.cursor()

    def cargar_datos(self):
        """Carga las facturas pendientes."""
        for row in self.view.tree.get_children():
            self.view.tree.delete(row)
            
        try:
            cursor = self._cursor()
            # Seleccionar facturas PENDIENTES
            sql = """
                SELECT f.id_factura, f.numero_factura, p.nombres, p.apellidos, f.fecha_factura, f.total
                FROM Factura f
                JOIN Paciente p ON f.id_paciente = p.id_paciente
                WHERE f.estado_pago = 'PENDIENTE' 
                  AND f.eliminado = 0
                ORDER BY f.fecha_factura ASC
            """
            cursor.execute(sql)
            rows = cursor.fetchall()
            
            total_deuda = 0.0
            
            for r in rows:
                id_factura = r[0]
                numero = r[1]
                paciente = f"{r[2]} {r[3]}"
                fecha = r[4].strftime("%Y-%m-%d") if r[4] else ""
                total = float(r[5])
                
                total_deuda += total
                
                self.view.tree.insert("", "end", values=(
                    id_factura,
                    numero,
                    paciente,
                    fecha,
                    f"S/ {total:.2f}"
                ))
            
            # Actualizar etiqueta de total adeudado
            self.view.var_total.set(f"S/ {total_deuda:.2f}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar cuentas por cobrar: {str(e)}")

    def marcar_como_pagado(self):
        seleccion = self.view.tree.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Seleccione una factura pendiente de la lista.")
            return
            
        item = self.view.tree.item(seleccion[0])
        valores = item['values']
        id_factura = valores[0]
        numero_factura = valores[1]
        
        respuesta = messagebox.askyesno("Confirmar Pago", f"¿Confirmar el pago de la factura {numero_factura}?")
        if respuesta:
            try:
                cursor = self._cursor()
                sql = "UPDATE Factura SET estado_pago = 'PAGADO' WHERE id_factura = ?"
                cursor.execute(sql, (id_factura,))
                self._conexion.commit()
                messagebox.showinfo("Éxito", "Factura marcada como pagada.")
                self.cargar_datos()
            except Exception as e:
                self._conexion.rollback()
                messagebox.showerror("Error", f"Error al actualizar factura: {str(e)}")
