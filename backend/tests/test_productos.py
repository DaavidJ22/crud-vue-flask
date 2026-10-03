def crear_producto(client, **overrides):
    data = {
        "nombre": "Teclado",
        "descripcion": "Teclado mecánico",
        "precio": "125.50",
        "stock": 8,
        "activo": True,
        **overrides,
    }
    return client.post("/api/productos", json=data)


def test_crear_producto(client):
    response = crear_producto(client)

    assert response.status_code == 201
    assert response.get_json() == {
        "id": 1,
        "nombre": "Teclado",
        "descripcion": "Teclado mecánico",
        "precio": 125.5,
        "stock": 8,
        "activo": True,
    }


def test_listar_productos(client):
    primero = crear_producto(client).get_json()
    segundo = crear_producto(
        client,
        nombre="Monitor",
        descripcion=None,
        precio="900.00",
        stock=3,
    ).get_json()

    response = client.get("/api/productos")

    assert response.status_code == 200
    assert [producto["id"] for producto in response.get_json()] == [
        segundo["id"],
        primero["id"],
    ]


def test_actualizar_producto(client):
    producto = crear_producto(client).get_json()

    response = client.put(
        f"/api/productos/{producto['id']}",
        json={
            "nombre": "Teclado actualizado",
            "descripcion": None,
            "precio": "100.25",
            "stock": 4,
            "activo": False,
        },
    )

    assert response.status_code == 200
    assert response.get_json() == {
        "id": producto["id"],
        "nombre": "Teclado actualizado",
        "descripcion": None,
        "precio": 100.25,
        "stock": 4,
        "activo": False,
    }


def test_eliminar_producto(client):
    producto = crear_producto(client).get_json()

    response = client.delete(f"/api/productos/{producto['id']}")

    assert response.status_code == 204
    assert response.data == b""
    assert client.get("/api/productos").get_json() == []


def test_precio_negativo_es_invalido(client):
    response = crear_producto(client, precio="-0.01")

    assert response.status_code == 400
    assert response.get_json() == {
        "error": "Precio y stock deben ser mayores o iguales a cero"
    }


def test_stock_negativo_es_invalido(client):
    response = crear_producto(client, stock=-1)

    assert response.status_code == 400
    assert response.get_json() == {
        "error": "Precio y stock deben ser mayores o iguales a cero"
    }


def test_faltan_campos_obligatorios_en_producto(client):
    response = client.post(
        "/api/productos",
        json={"nombre": "Incompleto"},
    )

    assert response.status_code == 400
    assert response.get_json() == {"error": "Faltan campos obligatorios"}
