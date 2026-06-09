import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date
from tkcalendar import DateEntry

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from controllers.paciente_controller import PacienteController
from models.paciente import Paciente
from views.menu_principal import MenuPrincipal


class PacientesView(tk.Tk):
    """Vista para la gestión de pacientes"""
    
    def __init__(self):
        super().__init__()
        self.title('Gestión de Pacientes')
        self.geometry('1600x800')
        self.configure(bg='#f4f6f8')
        
        # Colores del sistema
        self.COLOR_CELESTE = '#3182ce'
        self.COLOR_CELESTE_OSCURO = '#2c5aa0'
        self.COLOR_FONDO = '#f4f6f8'
        self.COLOR_BLANCO = '#ffffff'
        self.COLOR_VERDE = '#2ecc71'
        self.COLOR_ROJO = '#e74c3c'
        self.COLOR_TEXTO = '#2c3e50'
        
        self.controller = None
        self.paciente_seleccionado = None
        self.tree = None
        
        self._init_controller()
        if self.controller:
            self._build_interface()
            self.cargar_pacientes()
    
    def _init_controller(self):
        """Inicializar el controlador"""
        try:
            self.controller = PacienteController()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo conectar con la base de datos:\n{str(e)}")
            self.controller = None
    
    def _build_interface(self):
        """Construir la interfaz completa"""
        
        # Header
        self._build_header()
        
        # Contenedor principal
        main_frame = ttk.Frame(self)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Panel izquierdo (lista de pacientes)
        self._build_lista_pacientes(main_frame)
        
        # Panel derecho (formulario)
        self._build_formulario(main_frame)
    
    def _build_header(self):
        """Construir el header con título y botones de navegación"""
        header_frame = tk.Frame(self, bg=self.COLOR_CELESTE, height=60)
        header_frame.pack(fill='x', padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        # Título
        titulo = tk.Label(header_frame, 
                         text='Gestión de Pacientes',
                         font=('Segoe UI', 22, 'bold'),
                         bg=self.COLOR_CELESTE,
                         fg=self.COLOR_BLANCO)
        titulo.pack(side='left', padx=20, pady=15)
        
        # Botón de regreso
        btn_regresar = tk.Button(header_frame, text='← Volver al Menú',
                                command=self.regreso_menu,
                                bg=self.COLOR_CELESTE_OSCURO,
                                fg=self.COLOR_BLANCO,
                                font=('Segoe UI', 10, 'bold'),
                                activebackground='#1e4d8b',
                                activeforeground=self.COLOR_BLANCO,
                                relief=tk.RAISED, bd=2, cursor='hand2',
                                padx=15, pady=8)
        btn_regresar.pack(side='right', padx=20, pady=15)
    
    def _build_lista_pacientes(self, parent):
        """Construir el panel con la lista de pacientes"""
        lista_frame = ttk.Frame(parent)
        lista_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # Búsqueda
        search_frame = ttk.Frame(lista_frame)
        search_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(search_frame, text='Buscar:').pack(side='left', padx=5)
        
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self._on_search_change)
        
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=40)
        search_entry.pack(side='left', padx=5, fill='x', expand=True)
        
        btn_limpiar = tk.Button(search_frame, text='Limpiar',
                               command=self._limpiar_busqueda,
                               bg=self.COLOR_CELESTE,
                               fg=self.COLOR_BLANCO,
                               font=('Segoe UI', 9, 'bold'),
                               padx=10, pady=5)
        btn_limpiar.pack(side='left', padx=5)
        
        # Treeview
        tree_frame = ttk.Frame(lista_frame)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        columns = ('ID', 'Nombres', 'Apellidos', 'Teléfono', 'Email', 'Grupo Sanguíneo')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=20)
        
        # Configurar columnas
        widths = [40, 120, 120, 100, 150, 100]
        for col, width in zip(columns, widths):
            self.tree.heading(col, text=col)
            if col == 'ID':
                self.tree.column(col, width=width, minwidth=35, stretch=False, anchor='center')
            elif col == 'Grupo Sanguíneo':
                self.tree.column(col, width=width, minwidth=100, stretch=False, anchor='center')
            else:
                self.tree.column(col, width=width, anchor='w')
        
        # Barra de desplazamiento
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Bindings
        self.tree.bind('<<TreeviewSelect>>', self._on_select_paciente)
        
        # Botones de acciones
        buttons_frame = ttk.Frame(lista_frame)
        buttons_frame.pack(fill='x', padx=10, pady=10)
        
        btn_nuevo = tk.Button(buttons_frame, text='+ Nuevo Paciente',
                             command=self._nuevo_paciente,
                             bg=self.COLOR_VERDE,
                             fg=self.COLOR_BLANCO,
                             font=('Segoe UI', 10, 'bold'),
                             padx=15, pady=8)
        btn_nuevo.pack(side='left', padx=5)
        
        btn_eliminar = tk.Button(buttons_frame, text='🗑 Eliminar',
                                command=self._eliminar_paciente,
                                bg=self.COLOR_ROJO,
                                fg=self.COLOR_BLANCO,
                                font=('Segoe UI', 10, 'bold'),
                                padx=15, pady=8)
        btn_eliminar.pack(side='left', padx=5)
    
    def _build_formulario(self, parent):
        """Construir el formulario lateral para editar pacientes"""
        form_frame = ttk.LabelFrame(parent, text='Información del Paciente', padding=15)
        form_frame.pack(side='right', fill='both', expand=True, padx=10, pady=10)
        
        # Crear un canvas con scrollbar para el formulario
        canvas = tk.Canvas(form_frame, bg=self.COLOR_BLANCO, highlightthickness=0)
        scrollbar = ttk.Scrollbar(form_frame, orient='vertical', command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            '<Configure>',
            lambda e: canvas.configure(scrollregion=canvas.bbox('all'))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Campos del formulario
        self.form_fields = {}
        
        campos = [
            ('nombres', 'Nombres:', 'text', ''),
            ('apellidos', 'Apellidos:', 'text', ''),
            ('genero', 'Género:', 'combo', ''),
            ('fecha_nacimiento', 'Fecha de Nacimiento:', 'date', '(AAAA-MM-DD)'),
            ('email', 'Email:', 'text', ''),
            ('telefono', 'Teléfono:', 'text', ''),
            ('direccion', 'Dirección:', 'text', ''),
            ('grupo_sanguineo', 'Grupo Sanguíneo:', 'combo_sangre', ''),
            ('contacto_emergencia', 'Contacto de Emergencia:', 'text', ''),
            ('telefono_emergencia', 'Teléfono de Emergencia:', 'text', ''),
            ('alergias', 'Alergias:', 'textarea', ''),
            ('enfermedades_cronicas', 'Enfermedades Crónicas:', 'textarea', ''),
            ('observaciones', 'Observaciones:', 'textarea', ''),
        ]
        
        row = 0
        for campo, label, tipo, ayuda in campos:
            lbl = ttk.Label(scrollable_frame, text=label, font=('Segoe UI', 10))
            lbl.grid(row=row, column=0, sticky='w', padx=5, pady=5)
            
            if tipo == 'text':
                widget = ttk.Entry(scrollable_frame, width=35)
                widget.grid(row=row, column=1, sticky='ew', padx=5, pady=5)
            elif tipo == 'date':
                widget = DateEntry(scrollable_frame, width=33, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
                widget.grid(row=row, column=1, sticky='ew', padx=5, pady=5)
            elif tipo == 'combo':
                widget = ttk.Combobox(scrollable_frame, values=['M', 'F'], state='readonly', width=32)
                widget.grid(row=row, column=1, sticky='ew', padx=5, pady=5)
            elif tipo == 'combo_sangre':
                valores = ['O+', 'O-', 'A+', 'A-', 'B+', 'B-', 'AB+', 'AB-']
                widget = ttk.Combobox(scrollable_frame, values=valores, state='readonly', width=32)
                widget.grid(row=row, column=1, sticky='ew', padx=5, pady=5)
            elif tipo == 'textarea':
                widget = tk.Text(scrollable_frame, width=35, height=4, font=('Segoe UI', 9))
                widget.grid(row=row, column=1, sticky='ew', padx=5, pady=5)
            
            # Mostrar ayuda si existe
            if ayuda:
                lbl_ayuda = ttk.Label(scrollable_frame, text=ayuda, font=('Segoe UI', 8), foreground='gray')
                lbl_ayuda.grid(row=row, column=2, sticky='w', padx=5)
            
            self.form_fields[campo] = widget
            row += 1
        
        scrollable_frame.columnconfigure(1, weight=1)
        # Botones de guardar/cancelar (se empacan primero abajo para no exprimir el canvas)
        buttons_frame = ttk.Frame(form_frame)
        buttons_frame.pack(side='bottom', fill='x', padx=5, pady=10)
        
        btn_guardar = tk.Button(buttons_frame, text='💾 Guardar',
                               command=self._guardar_paciente,
                               bg=self.COLOR_VERDE,
                               fg=self.COLOR_BLANCO,
                               font=('Segoe UI', 11, 'bold'),
                               padx=20, pady=10)
        btn_guardar.pack(side='left', padx=5, expand=True, fill='x')
        
        btn_cancelar = tk.Button(buttons_frame, text='✕ Cancelar',
                                command=self._cancelar_edicion,
                                bg='#95a5a6',
                                fg=self.COLOR_BLANCO,
                                font=('Segoe UI', 11, 'bold'),
                                padx=20, pady=10)
        btn_cancelar.pack(side='left', padx=5, expand=True, fill='x')

        # Ahora empacamos la scrollbar y el canvas en el espacio restante
        scrollbar.pack(side='right', fill='y')
        canvas.pack(side='left', fill='both', expand=True)
        try:
            self.resizable(True, True)
            self.minsize(1280, 720)
        except Exception:
            pass

    
    # ==================== MÉTODOS DE EVENTOS ====================
    
    def regreso_menu(self):
        """Regresar al menú principal"""
        self.destroy()
        menu = MenuPrincipal()
        menu.mainloop()
    
    def cargar_pacientes(self):
        """Cargar y mostrar todos los pacientes"""
        try:
            if self.tree:
                for item in self.tree.get_children():
                    self.tree.delete(item)
            
            pacientes = self.controller.listar_todos()
            for paciente in pacientes:
                self.tree.insert('', 'end', values=(
                    paciente.get('id_paciente'),
                    paciente.get('nombres', ''),
                    paciente.get('apellidos', ''),
                    paciente.get('telefono', ''),
                    paciente.get('email', ''),
                    paciente.get('grupo_sanguineo', '')
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Error cargando pacientes:\n{str(e)}")
    
    def _on_select_paciente(self, event):
        """Cuando se selecciona un paciente en la tabla"""
        try:
            selection = self.tree.selection()
            if selection:
                item = selection[0]
                valores = self.tree.item(item)['values']
                id_paciente = valores[0]
                
                # Obtener datos completos del paciente
                paciente = self.controller.obtener_paciente(id_paciente)
                if paciente:
                    self.paciente_seleccionado = paciente
                    self._cargar_formulario(paciente)
        except Exception as e:
            messagebox.showerror("Error", f"Error seleccionando paciente:\n{str(e)}")
    
    def _cargar_formulario(self, paciente):
        """Cargar los datos del paciente en el formulario"""
        self.form_fields['nombres'].delete(0, tk.END)
        self.form_fields['nombres'].insert(0, paciente.nombres)
        
        self.form_fields['apellidos'].delete(0, tk.END)
        self.form_fields['apellidos'].insert(0, paciente.apellidos)
        
        self.form_fields['genero'].set(paciente.genero)
        
        self.form_fields['fecha_nacimiento'].delete(0, tk.END)
        if paciente.fecha_nacimiento:
            fecha_str = paciente.fecha_nacimiento.strftime('%Y-%m-%d') if isinstance(paciente.fecha_nacimiento, date) else str(paciente.fecha_nacimiento)
            self.form_fields['fecha_nacimiento'].insert(0, fecha_str)
        
        self.form_fields['email'].delete(0, tk.END)
        self.form_fields['email'].insert(0, paciente.email or '')
        
        self.form_fields['telefono'].delete(0, tk.END)
        self.form_fields['telefono'].insert(0, paciente.telefono or '')
        
        self.form_fields['direccion'].delete(0, tk.END)
        self.form_fields['direccion'].insert(0, paciente.direccion or '')
        
        self.form_fields['grupo_sanguineo'].set(paciente.grupo_sanguineo or '')
        
        self.form_fields['contacto_emergencia'].delete(0, tk.END)
        self.form_fields['contacto_emergencia'].insert(0, paciente.contacto_emergencia or '')
        
        self.form_fields['telefono_emergencia'].delete(0, tk.END)
        self.form_fields['telefono_emergencia'].insert(0, paciente.telefono_emergencia or '')
        
        for campo_text in ['alergias', 'enfermedades_cronicas', 'observaciones']:
            self.form_fields[campo_text].delete('1.0', tk.END)
            valor = getattr(paciente, campo_text, '')
            self.form_fields[campo_text].insert('1.0', valor or '')
    
    def _nuevo_paciente(self):
        """Limpiar el formulario para crear un nuevo paciente"""
        self.paciente_seleccionado = None
        self._limpiar_formulario()
    
    def _limpiar_formulario(self):
        """Limpiar todos los campos del formulario"""
        for widget in self.form_fields.values():
            if isinstance(widget, tk.Text):
                widget.delete('1.0', tk.END)
            elif isinstance(widget, ttk.Combobox):
                widget.set('')
            else:
                widget.delete(0, tk.END)
        
        if self.tree:
            for item in self.tree.selection():
                self.tree.selection_remove(item)
    
    def _guardar_paciente(self):
        """Guardar el paciente actual"""
        try:
            # Validar que los campos requeridos estén llenos
            nombres = self.form_fields['nombres'].get().strip()
            apellidos = self.form_fields['apellidos'].get().strip()
            genero = self.form_fields['genero'].get()
            fecha_nacimiento_str = self.form_fields['fecha_nacimiento'].get().strip()
            
            if not nombres or not apellidos or not genero or not fecha_nacimiento_str:
                messagebox.showwarning("Validación", 
                                     "Por favor complete los campos requeridos:\n"
                                     "- Nombres\n- Apellidos\n- Género\n- Fecha de Nacimiento")
                return
            
            # Parsear fecha
            try:
                fecha_nacimiento = datetime.strptime(fecha_nacimiento_str, '%Y-%m-%d').date()
            except ValueError:
                messagebox.showerror("Error", "Formato de fecha inválido. Use YYYY-MM-DD")
                return
            
            # Crear objeto Paciente
            paciente = Paciente(
                nombres=nombres,
                apellidos=apellidos,
                genero=genero,
                fecha_nacimiento=fecha_nacimiento,
                email=self.form_fields['email'].get().strip() or None,
                telefono=self.form_fields['telefono'].get().strip() or None,
                direccion=self.form_fields['direccion'].get().strip() or None,
                grupo_sanguineo=self.form_fields['grupo_sanguineo'].get().strip() or None,
                contacto_emergencia=self.form_fields['contacto_emergencia'].get().strip() or None,
                telefono_emergencia=self.form_fields['telefono_emergencia'].get().strip() or None,
                alergias=self.form_fields['alergias'].get('1.0', tk.END).strip() or None,
                enfermedades_cronicas=self.form_fields['enfermedades_cronicas'].get('1.0', tk.END).strip() or None,
                observaciones=self.form_fields['observaciones'].get('1.0', tk.END).strip() or None,
                id_paciente=self.paciente_seleccionado.id_paciente if self.paciente_seleccionado else None
            )
            
            # Guardar
            id_guardado = self.controller.guardar_paciente(paciente)
            messagebox.showinfo("Éxito", f"Paciente guardado exitosamente (ID: {id_guardado})")
            
            # Recargar la lista
            self.cargar_pacientes()
            self._limpiar_formulario()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error guardando paciente:\n{str(e)}")
    
    def _eliminar_paciente(self):
        """Eliminar el paciente seleccionado"""
        try:
            if not self.paciente_seleccionado:
                messagebox.showwarning("Advertencia", "Por favor seleccione un paciente para eliminar")
                return
            
            if messagebox.askyesno("Confirmar", 
                                  f"¿Eliminar a {self.paciente_seleccionado.nombre_completo()}?\n\nEsta acción no se puede deshacer."):
                self.controller.eliminar_logico(self.paciente_seleccionado.id_paciente)
                messagebox.showinfo("Éxito", "Paciente eliminado correctamente")
                self.cargar_pacientes()
                self._limpiar_formulario()
        except Exception as e:
            messagebox.showerror("Error", f"Error eliminando paciente:\n{str(e)}")
    
    def _cancelar_edicion(self):
        """Cancelar la edición actual"""
        self._limpiar_formulario()
        self.paciente_seleccionado = None
    
    def _on_search_change(self, *args):
        """Cuando cambia el texto de búsqueda"""
        termino = self.search_var.get().strip()
        
        try:
            if self.tree:
                for item in self.tree.get_children():
                    self.tree.delete(item)
            
            if termino:
                pacientes = self.controller.buscar(termino)
            else:
                pacientes = self.controller.listar_todos()
            
            for paciente in pacientes:
                self.tree.insert('', 'end', values=(
                    paciente.get('id_paciente'),
                    paciente.get('nombres', ''),
                    paciente.get('apellidos', ''),
                    paciente.get('telefono', ''),
                    paciente.get('email', ''),
                    paciente.get('grupo_sanguineo', '')
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Error buscando pacientes:\n{str(e)}")
    
    def _limpiar_busqueda(self):
        """Limpiar el campo de búsqueda"""
        self.search_var.set('')


if __name__ == '__main__':
    app = PacientesView()
    app.mainloop()
