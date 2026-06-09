import os
import sys
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.conexion import conexion
from database.consultas import HospitalQueries
from models.paciente import Paciente


class PacienteController:
    """Controlador para la gestión de pacientes"""
    
    def __init__(self):
        self._conexion = conexion
        self.queries = HospitalQueries()
        self._validar_conexion()
    
    def _validar_conexion(self):
        """Validar que la conexión a la BD sea válida"""
        try:
            if not self._conexion:
                raise Exception("Conexión no disponible")
            cursor = self._conexion.cursor()
            cursor.execute("SELECT 1")
        except Exception as e:
            raise Exception(f"Error validando conexión: {str(e)}")
    
    def listar_todos(self):
        """
        Obtener lista de todos los pacientes activos.
        
        Returns:
            list: Lista de pacientes
        """
        try:
            return self.queries.get_todos_pacientes()
        except Exception as e:
            raise Exception(f"Error listando pacientes: {str(e)}")
    
    def obtener_paciente(self, id_paciente):
        """
        Obtener un paciente específico por ID.
        
        Args:
            id_paciente (int): ID del paciente
        
        Returns:
            Paciente: Objeto Paciente o None si no existe
        """
        try:
            datos = self.queries.get_paciente_por_id(id_paciente)
            if datos:
                return self._dict_a_paciente(datos)
            return None
        except Exception as e:
            raise Exception(f"Error obteniendo paciente: {str(e)}")
    
    def buscar(self, termino):
        """
        Buscar pacientes por varios criterios.
        
        Args:
            termino (str): Término de búsqueda
        
        Returns:
            list: Lista de pacientes encontrados
        """
        try:
            return self.queries.buscar_pacientes(termino)
        except Exception as e:
            raise Exception(f"Error buscando pacientes: {str(e)}")
    
    def guardar_paciente(self, paciente):
        """
        Guardar un paciente nuevo o actualizar uno existente.
        
        Args:
            paciente (Paciente): Objeto Paciente a guardar
        
        Returns:
            int: ID del paciente guardado
        """
        try:
            # Validar datos
            es_valido, mensaje = paciente.es_valido()
            if not es_valido:
                raise Exception(f"Datos inválidos: {mensaje}")
            
            # Convertir a diccionario
            datos = paciente.to_dict()
            
            # Crear o actualizar
            if paciente.id_paciente:
                # Actualizar
                self.queries.actualizar_paciente(paciente.id_paciente, datos)
                return paciente.id_paciente
            else:
                # Crear
                nuevo_id = self.queries.crear_paciente(datos)
                return nuevo_id
        except Exception as e:
            raise Exception(f"Error guardando paciente: {str(e)}")
    
    def eliminar_logico(self, id_paciente):
        """
        Eliminar un paciente de forma lógica.
        
        Args:
            id_paciente (int): ID del paciente a eliminar
        
        Returns:
            bool: True si se eliminó correctamente
        """
        try:
            return self.queries.eliminar_paciente_logico(id_paciente)
        except Exception as e:
            raise Exception(f"Error eliminando paciente: {str(e)}")
    
    def _dict_a_paciente(self, datos):
        """Convertir diccionario a objeto Paciente"""
        return Paciente(
            nombres=datos.get('nombres'),
            apellidos=datos.get('apellidos'),
            genero=datos.get('genero'),
            fecha_nacimiento=datos.get('fecha_nacimiento'),
            email=datos.get('email'),
            telefono=datos.get('telefono'),
            direccion=datos.get('direccion'),
            grupo_sanguineo=datos.get('grupo_sanguineo'),
            contacto_emergencia=datos.get('contacto_emergencia'),
            telefono_emergencia=datos.get('telefono_emergencia'),
            alergias=datos.get('alergias'),
            enfermedades_cronicas=datos.get('enfermedades_cronicas'),
            observaciones=datos.get('observaciones'),
            id_paciente=datos.get('id_paciente'),
            estado=datos.get('estado', True),
            eliminado=datos.get('eliminado', False),
            fecha_creacion=datos.get('fecha_creacion'),
            fecha_actualizacion=datos.get('fecha_actualizacion')
        )
