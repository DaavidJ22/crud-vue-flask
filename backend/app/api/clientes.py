from flask import jsonify, request
from sqlalchemy.exc import IntegrityError

from ..errors import error, required
from ..extensions import db
from ..models import Cliente
from . import api_bp


@api_bp.get("/clientes")
def listar_clientes():
    clientes = db.session.execute(
        db.select(Cliente).order_by(Cliente.id.desc())
    ).scalars().all()
    return jsonify([cliente.to_dict() for cliente in clientes])


@api_bp.get("/clientes/<int:cliente_id>")
def obtener_cliente(cliente_id):
    cliente = db.get_or_404(Cliente, cliente_id)
    return jsonify(cliente.to_dict())


@api_bp.post("/clientes")
def crear_cliente():
    data = request.get_json(silent=True) or {}
    data["nombre"] = (data.get("nombre") or "").strip()
    data["correo"] = (data.get("correo") or "").strip().lower()

    if required(data, ["nombre", "correo"]):
        return error("Faltan campos obligatorios")

    telefono = data.get("telefono")
    if telefono is not None:
        telefono = telefono.strip() or None

    cliente = Cliente(
        nombre=data["nombre"],
        correo=data["correo"],
        telefono=telefono,
    )
    db.session.add(cliente)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return error("El correo ya está registrado", 409)

    return jsonify(cliente.to_dict()), 201


@api_bp.put("/clientes/<int:cliente_id>")
def actualizar_cliente(cliente_id):
    cliente = db.get_or_404(Cliente, cliente_id)
    data = request.get_json(silent=True) or {}
    data["nombre"] = (data.get("nombre") or "").strip()
    data["correo"] = (data.get("correo") or "").strip().lower()

    if required(data, ["nombre", "correo"]):
        return error("Faltan campos obligatorios")

    telefono = data.get("telefono")
    if telefono is not None:
        telefono = telefono.strip() or None

    cliente.nombre = data["nombre"]
    cliente.correo = data["correo"]
    cliente.telefono = telefono

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return error("El correo ya está registrado", 409)

    return jsonify(cliente.to_dict())


@api_bp.delete("/clientes/<int:cliente_id>")
def eliminar_cliente(cliente_id):
    cliente = db.get_or_404(Cliente, cliente_id)

    if cliente.pedidos:
        return error("No se puede eliminar un cliente con pedidos", 409)

    db.session.delete(cliente)
    db.session.commit()
    return "", 204
