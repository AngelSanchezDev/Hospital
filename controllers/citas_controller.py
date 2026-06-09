import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tkinter import ttk, messagebox
from tkcalendar import DateEntry

from database.conexion import conexion
import session


class CitasController:
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
        self.pacientes_dict = {}
        self.medicos_dict = {}
        self.especialidades_dict = {}
        self.estados_dict = {}
        self.tipos_pago_dict = {}

        self.frame = ttk.Frame(self.root)
        self.frame.pack(padx=10, pady=10, fill="both", expand=True)
        self.frame.columnconfigure(1, weight=1)

        self.btn_volver = ttk.Button(self.frame, text="Volver al Menú", command=self.volver_al_menu)
        self.btn_volver.grid(row=0, column=0, pady=10, sticky="w")

        ttk.Label(self.frame, text=f"Registrado por: {session.get_resumen_usuario()}").grid(row=0, column=1, sticky="w")

        self.label_buscar_pac = ttk.Label(self.frame, text="Buscar Paciente:")
        self.label_buscar_pac.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_buscar_pac = ttk.Entry(self.frame)
        self.entry_buscar_pac.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.entry_buscar_pac.bind("<KeyRelease>", self.filtrar_pacientes)

        self.label_paciente = ttk.Label(self.frame, text="Paciente:")
        self.label_paciente.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.combo_paciente = ttk.Combobox(self.frame, values=self.get_pacientes(), state="readonly")
        self.combo_paciente.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        self.label_especialidad = ttk.Label(self.frame, text="Especialidad:")
        self.label_especialidad.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        especialidades = self.get_especialidades()
        self.combo_especialidad = ttk.Combobox(self.frame, values=["Consulta General"] + especialidades, state="readonly")
        self.combo_especialidad.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
        self.combo_especialidad.bind("<<ComboboxSelected>>", self.on_especialidad_selected)

        self.label_buscar_med = ttk.Label(self.frame, text="Buscar Médico:")
        self.label_buscar_med.grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.entry_buscar_med = ttk.Entry(self.frame)
        self.entry_buscar_med.grid(row=4, column=1, padx=5, pady=5, sticky="ew")
        self.entry_buscar_med.bind("<KeyRelease>", self.filtrar_medicos)

        self.label_medico = ttk.Label(self.frame, text="Médico:")
        self.label_medico.grid(row=5, column=0, padx=5, pady=5, sticky="w")
        self.combo_medico = ttk.Combobox(self.frame, values=self.get_medicos(), state="readonly")
        self.combo_medico.grid(row=5, column=1, padx=5, pady=5, sticky="ew")

        self.label_fecha = ttk.Label(self.frame, text="Fecha:")
        self.label_fecha.grid(row=6, column=0, padx=5, pady=5, sticky="w")
        self.date_entry = DateEntry(self.frame, selectmode="day", date_pattern="yyyy-mm-dd")
        self.date_entry.grid(row=6, column=1, padx=5, pady=5, sticky="w")

        self.label_hora = ttk.Label(self.frame, text="Hora:")
        self.label_hora.grid(row=7, column=0, padx=5, pady=5, sticky="w")
        self.combo_hora = ttk.Combobox(self.frame, values=[f"{i:02d}:00" for i in range(8, 20)], state="readonly", width=10)
        self.combo_hora.grid(row=7, column=1, padx=5, pady=5, sticky="w")

        self.label_estado = ttk.Label(self.frame, text="Estado:")
        self.label_estado.grid(row=8, column=0, padx=5, pady=5, sticky="w")
        self.combo_estado = ttk.Combobox(self.frame, values=self.get_estados(), state="readonly")
        self.combo_estado.grid(row=8, column=1, padx=5, pady=5, sticky="ew")

        self.label_pago = ttk.Label(self.frame, text="Tipo de Pago:")
        self.label_pago.grid(row=9, column=0, padx=5, pady=5, sticky="w")
        self.combo_pago = ttk.Combobox(self.frame, values=self.get_tipos_pago(), state="readonly")
        self.combo_pago.grid(row=9, column=1, padx=5, pady=5, sticky="ew")

        self.label_precio = ttk.Label(self.frame, text="Precio (S/):")
        self.label_precio.grid(row=10, column=0, padx=5, pady=5, sticky="w")
        self.entry_precio = ttk.Entry(self.frame, width=15)
        self.entry_precio.grid(row=10, column=1, padx=5, pady=5, sticky="w")

        self.label_asunto = ttk.Label(self.frame, text="Asunto:")
        self.label_asunto.grid(row=11, column=0, padx=5, pady=5, sticky="w")
        self.entry_asunto = ttk.Entry(self.frame)
        self.entry_asunto.grid(row=11, column=1, padx=5, pady=5, sticky="ew")

        self.label_observaciones = ttk.Label(self.frame, text="Observaciones:")
        self.label_observaciones.grid(row=12, column=0, padx=5, pady=5, sticky="w")
        self.entry_observaciones = ttk.Entry(self.frame)
        self.entry_observaciones.grid(row=12, column=1, padx=5, pady=5, sticky="ew")

        self.label_sintomas = ttk.Label(self.frame, text="Síntoma Significativo:")
        self.label_sintomas.grid(row=13, column=0, padx=5, pady=5, sticky="w")
        self.entry_sintomas = ttk.Entry(self.frame)
        self.entry_sintomas.grid(row=13, column=1, padx=5, pady=5, sticky="ew")

        self.btn_guardar = ttk.Button(self.frame, text="Guardar Cita", command=self.guardar_cita)
        self.btn_guardar.grid(row=14, columnspan=2, pady=15)

    def volver_al_menu(self):
        if hasattr(self.root, "master") and self.root.master:
            self.root.master.deiconify()
        self.root.destroy()

    def get_pacientes(self):
        cursor = self._cursor()
        cursor.execute("SELECT id_paciente, nombres, apellidos FROM Paciente WHERE eliminado = 0")
        rows = cursor.fetchall()
        self.pacientes_dict = {f"{row[1]} {row[2]}": row[0] for row in rows}
        return list(self.pacientes_dict.keys())

    def get_especialidades(self):
        cursor = self._cursor()
        cursor.execute("SELECT id_especialidad, nombre FROM Especialidad WHERE eliminado = 0")
        rows = cursor.fetchall()
        self.especialidades_dict = {row[1]: row[0] for row in rows}
        return list(self.especialidades_dict.keys())

    def get_medicos(self, id_especialidad=None):
        cursor = self._cursor()
        if id_especialidad:
            cursor.execute("""
                SELECT m.id_medico, m.nombres, m.apellidos
                FROM Medico m
                JOIN MedicoEspecialidad me ON m.id_medico = me.id_medico
                WHERE m.eliminado = 0 AND me.id_especialidad = ?
            """, (id_especialidad,))
        else:
            cursor.execute("SELECT id_medico, nombres, apellidos FROM Medico WHERE eliminado = 0")
        rows = cursor.fetchall()
        self.medicos_dict = {f"{row[1]} {row[2]}": row[0] for row in rows}
        return list(self.medicos_dict.keys())

    def get_estados(self):
        cursor = self._cursor()
        cursor.execute("SELECT id_estado, nombre FROM Estado WHERE eliminado = 0")
        rows = cursor.fetchall()
        self.estados_dict = {row[1]: row[0] for row in rows}
        return list(self.estados_dict.keys())

    def get_tipos_pago(self):
        cursor = self._cursor()
        cursor.execute("SELECT id_pago, nombre FROM TipoPago WHERE eliminado = 0")
        rows = cursor.fetchall()
        self.tipos_pago_dict = {row[1]: row[0] for row in rows}
        return list(self.tipos_pago_dict.keys())

    def filtrar_pacientes(self, event):
        termino = self.entry_buscar_pac.get().lower()
        self.combo_paciente["values"] = [p for p in self.pacientes_dict if termino in p.lower()] if termino else list(self.pacientes_dict.keys())

    def filtrar_medicos(self, event):
        termino = self.entry_buscar_med.get().lower()
        self.combo_medico["values"] = [m for m in self.medicos_dict if termino in m.lower()] if termino else list(self.medicos_dict.keys())

    def on_especialidad_selected(self, event):
        especialidad = self.combo_especialidad.get()
        especialidad_upper = especialidad.upper()
        precios = {
            "CONSULTA GENERAL": 80,
            "CARDIOLOGÍA": 150,
            "CARDIOLOGIA": 150,
            "PEDIATRÍA": 100,
            "PEDIATRIA": 100,
            "DERMATOLOGÍA": 120,
            "DERMATOLOGIA": 120
        }
        self.entry_precio.delete(0, "end")
        self.entry_precio.insert(0, str(precios.get(especialidad_upper, 80)))

        if especialidad == "Consulta General":
            medicos = self.get_medicos()
        elif especialidad in self.especialidades_dict:
            medicos = self.get_medicos(self.especialidades_dict[especialidad])
        else:
            medicos = self.get_medicos()
        self.combo_medico["values"] = medicos
        self.combo_medico.set("")

    def _id_estado_seleccionado(self):
        nombre = self.combo_estado.get().strip()
        return self.estados_dict.get(nombre)

    def _id_pago_seleccionado(self):
        nombre = self.combo_pago.get().strip()
        return self.tipos_pago_dict.get(nombre)

    def guardar_cita(self):
        paciente_str = self.combo_paciente.get().strip()
        medico_str = self.combo_medico.get().strip()
        fecha = self.date_entry.get_date()
        hora = self.combo_hora.get().strip()
        especialidad = self.combo_especialidad.get().strip()
        precio = self.entry_precio.get().strip()
        estado_str = self.combo_estado.get().strip()
        pago_str = self.combo_pago.get().strip()
        asunto = self.entry_asunto.get().strip()
        observaciones = self.entry_observaciones.get().strip()
        sintomas = self.entry_sintomas.get().strip()

        if not all([paciente_str, medico_str, hora, especialidad, precio, estado_str, pago_str]):
            messagebox.showerror("Error", "Paciente, médico, fecha, hora, especialidad, estado, tipo de pago y precio son obligatorios.")
            return

        id_paciente = self.pacientes_dict.get(paciente_str)
        id_medico = self.medicos_dict.get(medico_str)
        id_estado = self._id_estado_seleccionado()
        id_pago = self._id_pago_seleccionado()
        id_usuario = session.get_id_usuario()

        if not all([id_paciente, id_medico, id_estado, id_pago, id_usuario]):
            messagebox.showerror("Error", "No se pudieron resolver todos los IDs necesarios para guardar la cita.")
            return

        if not asunto:
            asunto = f"Cita - {especialidad}"

        sql = """
            INSERT INTO Reservacion (
                titulo, nota, mensaje, fecha_cita, hora_cita, sintomas, observaciones,
                precio, id_paciente, id_usuario, id_medico, id_pago, id_estado
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        try:
            cursor = self._cursor()
            cursor.execute(sql, (
                asunto,
                observaciones if observaciones else None,
                None,
                fecha,
                hora,
                sintomas if sintomas else None,
                observaciones if observaciones else None,
                float(precio),
                id_paciente,
                id_usuario,
                id_medico,
                id_pago,
                id_estado,
            ))
            self._conexion.commit()
            messagebox.showinfo("Éxito", "Cita guardada exitosamente.")
            self._limpiar_formulario()
        except Exception as e:
            self._conexion.rollback()
            messagebox.showerror("Error", f"Error al guardar la cita: {str(e)}")

    def _limpiar_formulario(self):
        self.combo_paciente.set("")
        self.combo_medico.set("")
        self.combo_especialidad.set("")
        self.combo_estado.set("")
        self.combo_pago.set("")
        self.entry_precio.delete(0, "end")
        self.entry_buscar_pac.delete(0, "end")
        self.entry_buscar_med.delete(0, "end")
        self.entry_asunto.delete(0, "end")
        self.entry_observaciones.delete(0, "end")
        self.entry_sintomas.delete(0, "end")
