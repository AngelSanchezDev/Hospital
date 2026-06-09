import tkinter as tk
from tkinter import messagebox
from models.pago import Pago
from database.conexion import conexion

class PagoController:
    def __init__(self, view):
        self.view = view
        self._conexion = conexion
        
        # Vincular botones a métodos
        self.view.btn_guardar.config(command=self.guardar_pago)
        self.view.btn_editar.config(command=self.cargar_para_editar)
        self.view.btn_eliminar.config(command=self.eliminar_pago)
        self.view.btn_limpiar.config(command=self.limpiar_formulario)
        
        # Estado inicial
        self.pago_actual_id = None
        self.cargar_pagos()

    def _cursor(self):
        return self._conexion.cursor()

    def cargar_pagos(self):
        """Carga los tipos de pago en el Treeview"""
        # Limpiar tabla
        for row in self.view.tree.get_children():
            self.view.tree.delete(row)
            
        try:
            cursor = self._cursor()
            pagos = Pago.obtener_todos(cursor, incluir_inactivos=True)
            for p in pagos:
                estado_texto = "Activo" if p.estado else "Inactivo"
                self.view.tree.insert("", "end", values=(
                    p.id_pago,
                    p.nombre,
                    p.descripcion if p.descripcion else "",
                    estado_texto,
                    p.fecha_creacion.strftime("%Y-%m-%d") if p.fecha_creacion else ""
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar los pagos: {str(e)}")

    def guardar_pago(self):
        """Guarda un nuevo pago o actualiza uno existente"""
        nombre = self.view.var_nombre.get()
        descripcion = self.view.var_descripcion.get()
        estado_texto = self.view.var_estado.get()
        estado = True if estado_texto == "Activo" else False

        pago = Pago(nombre=nombre, descripcion=descripcion, estado=estado, id_pago=self.pago_actual_id)
        
        valido, mensaje = pago.es_valido()
        if not valido:
            messagebox.showwarning("Validación", mensaje)
            return

        try:
            cursor = self._cursor()
            if self.pago_actual_id is None:
                # Nuevo registro
                try:
                    pago.guardar(cursor)
                    self._conexion.commit()
                    messagebox.showinfo("Éxito", "Tipo de pago registrado correctamente.")
                except Exception as e:
                    if "UNIQUE" in str(e).upper():
                        messagebox.showerror("Error", "Ya existe un tipo de pago con ese nombre.")
                    else:
                        raise e
            else:
                # Actualizar
                try:
                    pago.actualizar(cursor)
                    self._conexion.commit()
                    messagebox.showinfo("Éxito", "Tipo de pago actualizado correctamente.")
                except Exception as e:
                    if "UNIQUE" in str(e).upper():
                        messagebox.showerror("Error", "Ya existe un tipo de pago con ese nombre.")
                    else:
                        raise e
            
            self.limpiar_formulario()
            self.cargar_pagos()

        except Exception as e:
            self._conexion.rollback()
            messagebox.showerror("Error", f"Error de base de datos: {str(e)}")

    def cargar_para_editar(self):
        """Carga los datos del pago seleccionado en el formulario para editarlo"""
        seleccion = self.view.tree.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Seleccione un tipo de pago de la lista para editar.")
            return
            
        item = self.view.tree.item(seleccion[0])
        valores = item['values']
        
        self.pago_actual_id = valores[0]
        self.view.var_nombre.set(valores[1])
        self.view.var_descripcion.set(valores[2])
        self.view.var_estado.set(valores[3])
        
        self.view.btn_guardar.config(text="Actualizar")

    def eliminar_pago(self):
        """Realiza la eliminación lógica de un tipo de pago"""
        seleccion = self.view.tree.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Seleccione un tipo de pago de la lista para eliminar.")
            return
            
        item = self.view.tree.item(seleccion[0])
        valores = item['values']
        id_pago = valores[0]
        nombre_pago = valores[1]
        
        respuesta = messagebox.askyesno("Confirmar Eliminación", f"¿Está seguro que desea eliminar '{nombre_pago}'?")
        if respuesta:
            try:
                cursor = self._cursor()
                pago = Pago(nombre="", id_pago=id_pago)
                pago.eliminar(cursor)
                self._conexion.commit()
                messagebox.showinfo("Éxito", "Tipo de pago eliminado correctamente.")
                self.limpiar_formulario()
                self.cargar_pagos()
            except Exception as e:
                self._conexion.rollback()
                messagebox.showerror("Error", f"Error al eliminar: {str(e)}")

    def limpiar_formulario(self):
        """Limpia los campos del formulario"""
        self.pago_actual_id = None
        self.view.var_nombre.set("")
        self.view.var_descripcion.set("")
        self.view.var_estado.set("Activo")
        self.view.btn_guardar.config(text="Guardar")
