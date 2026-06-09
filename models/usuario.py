class Usuario:
    def __init__(self, username, nombres, apellidos, email, password_hash=None, telefono=None, direccion=None, foto=None, estado_activo=True, eliminado=False, id_usuario=None):
        self.id_usuario = id_usuario
        self.username = username.strip() if username else ""
        self.nombres = nombres.strip() if nombres else ""
        self.apellidos = apellidos.strip() if apellidos else ""
        self.email = email.strip() if email else ""
        self.password_hash = password_hash
        self.telefono = telefono.strip() if telefono else None
        self.direccion = direccion.strip() if direccion else None
        self.foto = foto
        self.estado_activo = estado_activo
        self.eliminado = eliminado
        
    def es_valido(self):
        if not self.username or not self.nombres or not self.apellidos or not self.email:
            return False, "Username, nombres, apellidos y email son obligatorios."
        if not self.id_usuario and not self.password_hash:
            return False, "La contraseña es obligatoria para nuevos usuarios."
        return True, "OK"
        
    def guardar(self, cursor):
        sql = """
        INSERT INTO Usuario (username, nombres, apellidos, email, password_hash, telefono, direccion, estado_activo, eliminado)
        OUTPUT INSERTED.id_usuario
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(sql, (
            self.username, self.nombres, self.apellidos, self.email, self.password_hash, self.telefono, self.direccion, self.estado_activo, self.eliminado
        ))
        row = cursor.fetchone()
        if row:
            self.id_usuario = int(row[0])
            return self.id_usuario
        return None
        
    def actualizar(self, cursor):
        if self.password_hash:
            sql = """
            UPDATE Usuario SET username=?, nombres=?, apellidos=?, email=?, password_hash=?, telefono=?, direccion=?, estado_activo=?
            WHERE id_usuario=?
            """
            cursor.execute(sql, (self.username, self.nombres, self.apellidos, self.email, self.password_hash, self.telefono, self.direccion, self.estado_activo, self.id_usuario))
        else:
            sql = """
            UPDATE Usuario SET username=?, nombres=?, apellidos=?, email=?, telefono=?, direccion=?, estado_activo=?
            WHERE id_usuario=?
            """
            cursor.execute(sql, (self.username, self.nombres, self.apellidos, self.email, self.telefono, self.direccion, self.estado_activo, self.id_usuario))
        return cursor.rowcount > 0
        
    def eliminar(self, cursor):
        sql = "UPDATE Usuario SET eliminado = 1 WHERE id_usuario = ?"
        cursor.execute(sql, (self.id_usuario,))
        return cursor.rowcount > 0
        
    @staticmethod
    def obtener_todos(cursor):
        sql = "SELECT id_usuario, username, nombres, apellidos, email, telefono, direccion, estado_activo FROM Usuario WHERE eliminado = 0"
        cursor.execute(sql)
        rows = cursor.fetchall()
        
        usuarios = []
        for r in rows:
            u = Usuario(
                id_usuario=r[0],
                username=r[1],
                nombres=r[2],
                apellidos=r[3],
                email=r[4],
                telefono=r[5],
                direccion=r[6],
                estado_activo=r[7]
            )
            usuarios.append(u)
        return usuarios
