from decimal import Decimal, InvalidOperation

from flask import jsonify, request

from ..errors import error, required
from ..extensions import db
from ..models import Producto
from . import api_bp


def producto_data(data):
    data = data or {}
    data["nombre"] = (data.get("nombre") or "").strip()

    if required(data, ["nombre", "precio", "stock"]):
        return None, error("Faltan campos obligatorios")

    try:
        precio = Decimal(str(data["precio"]))
        stock_decimal = Decimal(str(data["stock"]))

        if not precio.is_finite() or not stock_decimal.is_finite():
            raise ValueError
        if stock_decimal != stock_decimal.to_integral_value():
            raise ValueError

        stock = int(stock_decimal)
    except (InvalidOperation, TypeError, ValueError):
        return None, error("Precio o stock no válidos")

    if precio < 0 or stock < 0:
        return None, error("Precio y stock deben ser mayores o iguales a cero")

    descripcion = data.get("descripcion")
    if descripcion is not None:
        descripcion = descripcion.strip() or None

    activo = data.get("activo", True)
    if not isinstance(activo, bool):
        return None, error("Activo debe ser booleano")

    return {
        "nombre": data["nombre"],
        "descripcion": descripcion,
        "precio": precio,
        "stock": stock,
        "activo": activo,
    }, None


@api_bp.get("/productos")
def listar_productos():
    productos = db.session.execute(
        db.select(Producto).order_by(Producto.id.desc())
    ).scalars().all()
    return jsonify([producto.to_dict() for producto in productos])


@api_bp.get("/productos/<int:producto_id>")
def obtener_producto(producto_id):
    producto = db.get_or_404(Producto, producto_id)
    return jsonify(producto.to_dict())


@api_bp.post("/productos")
def crear_producto():
    data, validation_error = producto_data(request.get_json(silent=True))
    if validation_error:
        return validation_error

    producto = Producto(**data)
    db.session.add(producto)
    db.session.commit()
    return jsonify(producto.to_dict()), 201


@api_bp.put("/productos/<int:producto_id>")
def actualizar_producto(producto_id):
    producto = db.get_or_404(Producto, producto_id)
    data, validation_error = producto_data(request.get_json(silent=True))
    if validation_error:
        return validation_error

    producto.nombre = data["nombre"]
    producto.descripcion = data["descripcion"]
    producto.precio = data["precio"]
    producto.stock = data["stock"]
    producto.activo = data["activo"]
    db.session.commit()
    return jsonify(producto.to_dict())


@api_bp.delete("/productos/<int:producto_id>")
def eliminar_producto(producto_id):
    producto = db.get_or_404(Producto, producto_id)

    if producto.pedidos:
        return error("No se puede eliminar un producto con pedidos", 409)

    db.session.delete(producto)
    db.session.commit()
    return "", 204
