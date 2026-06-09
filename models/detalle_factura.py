class DetalleFactura:
    def __init__(self, id_factura=None, descripcion=None, cantidad=1, precio_unitario=0, subtotal=0):
        self.id_factura = id_factura
        self.descripcion = descripcion
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario
        self.subtotal = subtotal

    def save(self, cursor):
        sql = """
        INSERT INTO DetalleFactura (id_factura, descripcion, cantidad, precio_unitario, subtotal)
        VALUES (?, ?, ?, ?, ?)
        """
        cursor.execute(sql, (
            self.id_factura,
            self.descripcion,
            self.cantidad,
            self.precio_unitario,
            self.subtotal
        ))
