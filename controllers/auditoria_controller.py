import tkinter as tk
from tkinter import messagebox
from database.conexion import conexion

class AuditoriaController:
    def __init__(self, view):
        self.view = view
        self._conexion = conexion
        
        self.view.btn_actualizar.config(command=self.cargar_datos)
        
        self.cargar_datos()

    def _cursor(self):
        return self._conexion.cursor()

    def cargar_datos(self):
        """Carga el registro de auditoría."""
        for row in self.view.tree.get_children():
            self.view.tree.delete(row)
            
        try:
            cursor = self._cursor()
            sql = "SELECT id_auditoria, fecha, accion, tabla, usuario_bd, datos_anteriores, datos_nuevos FROM Auditoria ORDER BY fecha DESC"
            cursor.execute(sql)
            rows = cursor.fetchall()
            
            for r in rows:
                self.view.tree.insert("", "end", values=(
                    r[0],
                    r[1].strftime('%Y-%m-%d %H:%M:%S'),
                    r[2],
                    r[3],
                    r[4],
                    r[5] or "",
                    r[6] or ""
                ))
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar auditoría: {str(e)}")
