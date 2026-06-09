-- Llenar tabla Usuario
INSERT INTO Usuario (username, nombres, apellidos, email, password_hash, telefono, direccion, estado_activo)
VALUES 
('admin_juan', 'Juan', 'Pérez', 'jperez@hospital.com', 'hash_secure_1', '987654321', 'Av. Central 123', 1),
('med_ana', 'Ana', 'García', 'agarcia@hospital.com', 'hash_secure_2', '987654322', 'Calle Los Pinos 456', 1),
('recep_luis', 'Luis', 'Sánchez', 'lsanchez@hospital.com', 'hash_secure_3', '987654323', 'Jr. Unión 789', 1),
('user_marta', 'Marta', 'Díaz', 'mdiaz@hospital.com', 'hash_secure_4', '987654324', 'Av. Larco 321', 1),
('med_carlos', 'Carlos', 'Ruiz', 'cruiz@hospital.com', 'hash_secure_5', '987654325', 'Calle Lima 555', 1);

-- Asignar Roles a Usuarios (UsuarioRol)
INSERT INTO UsuarioRol (id_usuario, id_rol)
VALUES (1, 1), (2, 2), (3, 3), (4, 4), (5, 2);

-- Asignar Permisos a Roles (RolPermiso)
INSERT INTO RolPermiso (id_rol, id_permiso)
VALUES (1, 1), (1, 4), (2, 5), (3, 5), (3, 6);
--select * from UsuarioRol
-- Llenar tabla Especialidad
INSERT INTO Especialidad (nombre, descripcion)
VALUES 
('CARDIOLOGIA', 'Enfermedades del corazón'),
('PEDIATRIA', 'Atención infantil'),
('DERMATOLOGIA', 'Cuidado de la piel'),
('GINECOLOGIA', 'Salud femenina'),
('MEDICINA GENERAL', 'Consulta primaria');

-- Llenar tabla Medico
INSERT INTO Medico (nombres, apellidos, genero, fecha_nacimiento, email, numero_colegiatura)
VALUES 
('Ana', 'García', 'F', '1985-05-20', 'agarcia_med@hospital.com', 'CMP12345'),
('Carlos', 'Ruiz', 'M', '1978-11-10', 'cruiz_med@hospital.com', 'CMP67890'),
('Elena', 'Torres', 'F', '1990-03-15', 'etorres_med@hospital.com', 'CMP11223'),
('Roberto', 'Mendoza', 'M', '1982-07-25', 'rmendoza_med@hospital.com', 'CMP44556'),
('Sofía', 'Castro', 'F', '1988-12-30', 'scastro_med@hospital.com', 'CMP77889');

-- Asignar Especialidades a Médicos
INSERT INTO MedicoEspecialidad (id_medico, id_especialidad)
VALUES (1, 1), (2, 5), (3, 2), (4, 4), (5, 3);

-- Horarios Médicos (Respetando el CHECK de hora_inicio < hora_fin)
INSERT INTO HorarioMedico (id_medico, dia_semana, hora_inicio, hora_fin)
VALUES 
(1, 'LUNES', '08:00', '14:00'),
(2, 'MARTES', '09:00', '13:00'),
(3, 'MIERCOLES', '14:00', '20:00'),
(4, 'JUEVES', '08:00', '16:00'),
(5, 'VIERNES', '10:00', '18:00');

------------------------------------------------
--------------------------------------------------
------------------------------------------------
-- Llenar tabla Paciente
INSERT INTO Paciente (nombres, apellidos, genero, fecha_nacimiento, email, grupo_sanguineo)
VALUES 
('Pedro', 'Alva', 'M', '1995-01-10', 'palva@gmail.com', 'O+'),
('Lucía', 'Fernández', 'F', '2000-06-15', 'lfernandez@gmail.com', 'A+'),
('Jorge', 'Ramírez', 'M', '1980-09-22', 'jramirez@gmail.com', 'B-'),
('María', 'Suárez', 'F', '1992-04-05', 'msuarez@gmail.com', 'O-'),
('Andrés', 'Custodio', 'M', '1987-12-12', 'acustodio@gmail.com', 'AB+');

-- Llenar tabla Reservacion
-- (Relaciona: Paciente, Usuario que registra, Medico, TipoPago, Estado)
INSERT INTO Reservacion (titulo, fecha_cita, hora_cita, precio, id_paciente, id_usuario, id_medico, id_pago, id_estado)
VALUES 
('Consulta Cardiología', '2026-06-10', '09:00', 150.00, 1, 3, 1, 2, 2),
('Control Pediátrico', '2026-06-11', '15:00', 100.00, 2, 3, 3, 1, 1),
('Chequeo General', '2026-06-12', '10:30', 80.00, 3, 3, 2, 4, 4),
('Consulta Ginecología', '2026-06-13', '08:30', 120.00, 4, 3, 4, 5, 2),
('Dermatología Especializada', '2026-06-14', '11:00', 200.00, 5, 3, 5, 3, 1);
----------------------------------------------------
----------------------------------------------------
----------------------------------------------------
-- Llenar HistoriaClinica
INSERT INTO HistoriaClinica (id_paciente, id_medico, id_reserva, motivo_consulta, diagnostico, tratamiento, peso, altura)
VALUES 
(1, 1, 1, 'Dolor en el pecho', 'Arritmia leve', 'Reposo y análisis', 75.5, 1.70),
(3, 2, 3, 'Resfriado común', 'Gripe estacional', 'Paracetamol 500mg', 82.0, 1.75),
(2, 3, 2, 'Fiebre persistente', 'Infección viral', 'Hidratación', 35.0, 1.30),
(4, 4, 4, 'Control anual', 'Salud óptima', 'Ninguno', 60.2, 1.62),
(5, 5, 5, 'Acné severo', 'Acné quístico', 'Cremas tópicas', 70.0, 1.68);

-- Llenar Factura
INSERT INTO Factura (numero_factura, id_paciente, id_reserva, subtotal, igv, total, estado_pago)
VALUES 
('F001-00001', 1, 1, 127.12, 22.88, 150.00, 'PAGADO'),
('F001-00002', 2, 2, 84.75, 15.25, 100.00, 'PENDIENTE'),
('F001-00003', 3, 3, 67.80, 12.20, 80.00, 'PAGADO'),
('F001-00004', 4, 4, 101.69, 18.31, 120.00, 'PAGADO'),
('F001-00005', 5, 5, 169.49, 30.51, 200.00, 'ANULADO');

-- Detalle de Factura
INSERT INTO DetalleFactura (id_factura, descripcion, cantidad, precio_unitario, subtotal)
VALUES 
(1, 'Consulta Médica Especializada', 1, 150.00, 150.00),
(2, 'Atención Pediatría', 1, 100.00, 100.00),
(3, 'Medicina General', 1, 80.00, 80.00),
(4, 'Ginecología', 1, 120.00, 120.00),
(5, 'Dermatología', 1, 200.00, 200.00);


----------------------------------------------------
----------------------------------------------------
----------------------------------------------------
--select * from auditoria