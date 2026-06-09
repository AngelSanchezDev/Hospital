class Cita:
    def __init__(self, id_cita=None, titulo=None, nota=None, mensaje=None, fecha_cita=None,
                 hora_cita=None, sintomas=None, observaciones=None, precio=None,
                 id_paciente=None, id_usuario=None, id_medico=None, id_pago=None, id_estado=None):
        self.id_cita = id_cita
        self.titulo = titulo
        self.nota = nota
        self.mensaje = mensaje
        self.id_paciente = id_paciente
        self.id_usuario = id_usuario
        self.id_medico = id_medico
        self.fecha_cita = fecha_cita
        self.hora_cita = hora_cita
        self.sintomas = sintomas
        self.observaciones = observaciones
        self.precio = precio
        self.id_pago = id_pago
        self.id_estado = id_estado

    def save(self, cursor):
        sql = """
        INSERT INTO Reservacion (
            titulo, nota, mensaje, fecha_cita, hora_cita, sintomas, observaciones,
            precio, id_paciente, id_usuario, id_medico, id_pago, id_estado
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(sql, (
            self.titulo,
            self.nota,
            self.mensaje,
            self.fecha_cita,
            self.hora_cita,
            self.sintomas,
            self.observaciones,
            self.precio,
            self.id_paciente,
            self.id_usuario,
            self.id_medico,
            self.id_pago,
            self.id_estado
        ))
