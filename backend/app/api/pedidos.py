from flask import jsonify, request

from ..errors import error, required
from ..extensions import db
from ..models import Cliente, Pedido, Producto
from . import api_bp


ESTADOS_PERMITIDOS = ["pendiente", "pagado", "enviado", "cancelado"]


def pedido_data(data):
    data = data or {}

    if required(data, ["cliente_id", "producto_id", "cantidad"]):
        return None, error("Faltan campos obligatorios")

    try:
        values = (data["cliente_id"], data["producto_id"], data["cantidad"])
        if any(isinstance(value, bool) for value in values):
            raise ValueError
        if any(isinstance(value, float) and not value.is_integer() for value in values):
            raise ValueError

        cliente_id = int(data["cliente_id"])
        producto_id = int(data["producto_id"])
        cantidad = int(data["cantidad"])
    except (TypeError, ValueError):
        return None, error("Los identificadores y la cantidad deben ser enteros")

    if cantidad <= 0:
        return None, error("La cantidad debe ser mayor que cero")

    cliente = db.session.get(Cliente, cliente_id)
    producto = db.session.get(Producto, producto_id)

    if cliente is None or producto is None:
        return None, error("Cliente o producto no encontrado", 404)

    if producto.stock < cantidad:
        return None, error("Stock insuficiente", 409)

    return {
        "cliente": cliente,
        "producto": producto,
        "cantidad": cantidad,
    }, None


@api_bp.get("/pedidos")
def listar_pedidos():
    pedidos = db.session.execute(
        db.select(Pedido).order_by(Pedido.id.desc())
    ).scalars().all()
    return jsonify([pedido.to_dict() for pedido in pedidos])


@api_bp.get("/pedidos/<int:pedido_id>")
def obtener_pedido(pedido_id):
    pedido = db.get_or_404(Pedido, pedido_id)
    return jsonify(pedido.to_dict())


@api_bp.post("/pedidos")
def crear_pedido():
    data, validation_error = pedido_data(request.get_json(silent=True))
    if validation_error:
        return validation_error

    data["producto"].stock -= data["cantidad"]
    pedido = Pedido(
        cliente=data["cliente"],
        producto=data["producto"],
        cantidad=data["cantidad"],
        estado="pendiente",
    )
    db.session.add(pedido)
    db.session.commit()
    return jsonify(pedido.to_dict()), 201


@api_bp.put("/pedidos/<int:pedido_id>")
def actualizar_pedido(pedido_id):
    pedido = db.get_or_404(Pedido, pedido_id)
    data = request.get_json(silent=True) or {}
    estado = (data.get("estado") or "").strip().lower()

    if estado not in ESTADOS_PERMITIDOS:
        return error("Estado no válido", details=ESTADOS_PERMITIDOS)

    pedido.estado = estado
    db.session.commit()
    return jsonify(pedido.to_dict())


@api_bp.delete("/pedidos/<int:pedido_id>")
def eliminar_pedido(pedido_id):
    pedido = db.get_or_404(Pedido, pedido_id)

    if pedido.estado != "cancelado":
        return error("Solo se pueden eliminar pedidos cancelados", 409)

    db.session.delete(pedido)
    db.session.commit()
    return "", 204
