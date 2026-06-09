import tkinter as tk
from tkinter import messagebox
from models.usuario import Usuario
from database.conexion import conexion

class UsuarioController:
    def __init__(self, view):
        self.view = view
        self._conexion = conexion
        
        self.view.btn_guardar.config(command=self.guardar_usuario)
        self.view.btn_editar.config(command=self.cargar_para_editar)
        self.view.btn_eliminar.config(command=self.eliminar_usuario)
        self.view.btn_limpiar.config(command=self.limpiar_formulario)
        
        self.usuario_actual_id = None
        self.cargar_usuarios()

    def _cursor(self):
        return self._conexion.cursor()

    def cargar_usuarios(self):
        for row in self.view.tree.get_children():
            self.view.tree.delete(row)
            
        try:
            cursor = self._cursor()
            usuarios = Usuario.obtener_todos(cursor)
            for u in usuarios:
                estado_texto = "Activo" if u.estado_activo else "Inactivo"
                self.view.tree.insert("", "end", values=(
                    u.id_usuario,
                    u.username,
                    f"{u.nombres} {u.apellidos}",
                    u.email,
                    estado_texto,
                    u.telefono or "",
                    u.direccion or "",
                    u.nombres,
                    u.apellidos
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar los usuarios: {str(e)}")

    def guardar_usuario(self):
        username = self.view.var_username.get()
        nombres = self.view.var_nombres.get()
        apellidos = self.view.var_apellidos.get()
        email = self.view.var_email.get()
        telefono = self.view.var_telefono.get()
        direccion = self.view.var_direccion.get()
        password = self.view.var_password.get()
        estado = True if self.view.var_estado.get() == "Activo" else False

        usuario = Usuario(
            username=username, nombres=nombres, apellidos=apellidos, email=email,
            password_hash=password if password else None,
            telefono=telefono, direccion=direccion, estado_activo=estado,
            id_usuario=self.usuario_actual_id
        )
        
        valido, mensaje = usuario.es_valido()
        if not valido:
            messagebox.showwarning("Validación", mensaje)
            return

        try:
            cursor = self._cursor()
            if self.usuario_actual_id is None:
                usuario.guardar(cursor)
                self._conexion.commit()
                messagebox.showinfo("Éxito", "Usuario registrado correctamente.")
            else:
                usuario.actualizar(cursor)
                self._conexion.commit()
                messagebox.showinfo("Éxito", "Usuario actualizado correctamente.")
            
            self.limpiar_formulario()
            self.cargar_usuarios()

        except Exception as e:
            self._conexion.rollback()
            if "UNIQUE" in str(e).upper():
                messagebox.showerror("Error", "El Username o Email ya está en uso.")
            else:
                messagebox.showerror("Error", f"Error de base de datos: {str(e)}")

    def cargar_para_editar(self):
        seleccion = self.view.tree.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Seleccione un usuario de la lista.")
            return
            
        item = self.view.tree.item(seleccion[0])
        valores = item['values']
        
        self.usuario_actual_id = valores[0]
        self.view.var_username.set(valores[1])
        # valores[2] is full name, but we stored names individually in 7 and 8
        self.view.var_nombres.set(valores[7])
        self.view.var_apellidos.set(valores[8])
        self.view.var_email.set(valores[3])
        self.view.var_estado.set(valores[4])
        self.view.var_telefono.set(valores[5])
        self.view.var_direccion.set(valores[6])
        self.view.var_password.set("") # Blank password when editing
        
        self.view.btn_guardar.config(text="Actualizar")

    def eliminar_usuario(self):
        seleccion = self.view.tree.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Seleccione un usuario de la lista.")
            return
            
        item = self.view.tree.item(seleccion[0])
        valores = item['values']
        id_user = valores[0]
        username = valores[1]
        
        if messagebox.askyesno("Confirmar", f"¿Está seguro que desea eliminar a '{username}'?"):
            try:
                cursor = self._cursor()
                usuario = Usuario(username="", nombres="", apellidos="", email="", id_usuario=id_user)
                usuario.eliminar(cursor)
                self._conexion.commit()
                messagebox.showinfo("Éxito", "Usuario eliminado correctamente.")
                self.limpiar_formulario()
                self.cargar_usuarios()
            except Exception as e:
                self._conexion.rollback()
                messagebox.showerror("Error", f"Error al eliminar: {str(e)}")

    def limpiar_formulario(self):
        self.usuario_actual_id = None
        self.view.var_username.set("")
        self.view.var_nombres.set("")
        self.view.var_apellidos.set("")
        self.view.var_email.set("")
        self.view.var_telefono.set("")
        self.view.var_direccion.set("")
        self.view.var_password.set("")
        self.view.var_estado.set("Activo")
        self.view.btn_guardar.config(text="Guardar")
