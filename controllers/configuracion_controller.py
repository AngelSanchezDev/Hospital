import tkinter as tk
from tkinter import messagebox
from database.conexion import conexion
import session

class ConfiguracionController:
    def __init__(self, view):
        self.view = view
        self._conexion = conexion
        
        self.view.btn_guardar.config(command=self.guardar_cambios)
        
        self.cargar_datos_usuario()

    def _cursor(self):
        return self._conexion.cursor()

    def cargar_datos_usuario(self):
        usuario_actual = session.get_usuario_actual()
        if not usuario_actual:
            messagebox.showerror("Error", "No hay sesión activa.")
            return
            
        id_usuario = usuario_actual.get("id_usuario")
        
        try:
            cursor = self._cursor()
            cursor.execute("SELECT nombres, apellidos, email, telefono, direccion FROM Usuario WHERE id_usuario = ?", (id_usuario,))
            row = cursor.fetchone()
            
            if row:
                self.view.var_nombres.set(row[0])
                self.view.var_apellidos.set(row[1])
                self.view.var_email.set(row[2])
                self.view.var_telefono.set(row[3] or "")
                self.view.var_direccion.set(row[4] or "")
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar datos: {str(e)}")

    def guardar_cambios(self):
        usuario_actual = session.get_usuario_actual()
        if not usuario_actual:
            return
            
        id_usuario = usuario_actual.get("id_usuario")
        nombres = self.view.var_nombres.get().strip()
        apellidos = self.view.var_apellidos.get().strip()
        email = self.view.var_email.get().strip()
        telefono = self.view.var_telefono.get().strip()
        direccion = self.view.var_direccion.get().strip()
        pw = self.view.var_password.get().strip()
        
        if not nombres or not apellidos or not email:
            messagebox.showwarning("Validación", "Nombres, apellidos y email son obligatorios.")
            return
            
        try:
            cursor = self._cursor()
            
            if pw:
                # Si hay contraseña, actualizarla también
                sql = "UPDATE Usuario SET nombres=?, apellidos=?, email=?, telefono=?, direccion=?, password_hash=? WHERE id_usuario=?"
                cursor.execute(sql, (nombres, apellidos, email, telefono, direccion, pw, id_usuario))
            else:
                # Actualizar sin tocar la contraseña
                sql = "UPDATE Usuario SET nombres=?, apellidos=?, email=?, telefono=?, direccion=? WHERE id_usuario=?"
                cursor.execute(sql, (nombres, apellidos, email, telefono, direccion, id_usuario))
                
            self._conexion.commit()
            
            # Actualizar session en memoria
            usuario_actual["nombres"] = nombres
            usuario_actual["apellidos"] = apellidos
            usuario_actual["email"] = email
            
            messagebox.showinfo("Éxito", "Datos de perfil actualizados correctamente.")
            self.view.var_password.set("") # Limpiar campo
            
        except Exception as e:
            self._conexion.rollback()
            if "UNIQUE" in str(e).upper():
                messagebox.showerror("Error", "El email ya está en uso por otro usuario.")
            else:
                messagebox.showerror("Error", f"Error al actualizar: {str(e)}")
