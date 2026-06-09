from datetime import datetime


class Paciente:
    """Modelo de datos para Paciente"""
    
    def __init__(self, 
                 nombres,
                 apellidos,
                 genero,
                 fecha_nacimiento,
                 email=None,
                 telefono=None,
                 direccion=None,
                 grupo_sanguineo=None,
                 contacto_emergencia=None,
                 telefono_emergencia=None,
                 alergias=None,
                 enfermedades_cronicas=None,
                 observaciones=None,
                 id_paciente=None,
                 estado=True,
                 eliminado=False,
                 fecha_creacion=None,
                 fecha_actualizacion=None):
        """
        Inicializar un paciente.
        
        Args:
            nombres (str): Nombres del paciente
            apellidos (str): Apellidos del paciente
            genero (str): 'M' o 'F'
            fecha_nacimiento (date): Fecha de nacimiento
            email (str): Email del paciente
            telefono (str): Teléfono principal
            direccion (str): Dirección
            grupo_sanguineo (str): Tipo de sangre
            contacto_emergencia (str): Nombre del contacto de emergencia
            telefono_emergencia (str): Teléfono de emergencia
            alergias (str): Alergias conocidas
            enfermedades_cronicas (str): Enfermedades crónicas
            observaciones (str): Observaciones adicionales
            id_paciente (int): ID del paciente (si existe en BD)
            estado (bool): Estado activo/inactivo
            eliminado (bool): Eliminado lógicamente
            fecha_creacion (datetime): Fecha de creación
            fecha_actualizacion (datetime): Fecha de última actualización
        """
        self.id_paciente = id_paciente
        self.nombres = nombres.strip() if nombres else ""
        self.apellidos = apellidos.strip() if apellidos else ""
        self.genero = genero.upper() if genero else "M"
        self.fecha_nacimiento = fecha_nacimiento
        self.email = email.strip() if email else None
        self.telefono = telefono.strip() if telefono else None
        self.direccion = direccion.strip() if direccion else None
        self.grupo_sanguineo = grupo_sanguineo.strip() if grupo_sanguineo else None
        self.contacto_emergencia = contacto_emergencia.strip() if contacto_emergencia else None
        self.telefono_emergencia = telefono_emergencia.strip() if telefono_emergencia else None
        self.alergias = alergias.strip() if alergias else None
        self.enfermedades_cronicas = enfermedades_cronicas.strip() if enfermedades_cronicas else None
        self.observaciones = observaciones.strip() if observaciones else None
        self.estado = estado
        self.eliminado = eliminado
        self.fecha_creacion = fecha_creacion or datetime.now()
        self.fecha_actualizacion = fecha_actualizacion
    
    def es_valido(self):
        """Validar que los datos requeridos estén presentes"""
        if not self.nombres or len(self.nombres) < 2:
            return False, "El nombre debe tener al menos 2 caracteres"
        if not self.apellidos or len(self.apellidos) < 2:
            return False, "El apellido debe tener al menos 2 caracteres"
        if self.genero not in ['M', 'F']:
            return False, "El género debe ser 'M' o 'F'"
        if not self.fecha_nacimiento:
            return False, "La fecha de nacimiento es requerida"
        if self.email and '@' not in self.email:
            return False, "Email inválido"
        return True, "OK"
    
    def nombre_completo(self):
        """Retornar nombre completo"""
        return f"{self.nombres} {self.apellidos}"
    
    def to_dict(self):
        """Convertir a diccionario para almacenar en BD"""
        return {
            'id_paciente': self.id_paciente,
            'nombres': self.nombres,
            'apellidos': self.apellidos,
            'genero': self.genero,
            'fecha_nacimiento': self.fecha_nacimiento,
            'email': self.email,
            'telefono': self.telefono,
            'direccion': self.direccion,
            'grupo_sanguineo': self.grupo_sanguineo,
            'contacto_emergencia': self.contacto_emergencia,
            'telefono_emergencia': self.telefono_emergencia,
            'alergias': self.alergias,
            'enfermedades_cronicas': self.enfermedades_cronicas,
            'observaciones': self.observaciones,
            'estado': self.estado,
            'eliminado': self.eliminado,
            'fecha_creacion': self.fecha_creacion,
            'fecha_actualizacion': self.fecha_actualizacion
        }
    
    def __repr__(self):
        return f"Paciente(id={self.id_paciente}, nombre='{self.nombre_completo()}')"
