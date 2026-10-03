def crear_cliente(client, **overrides):
    data = {
        "nombre": "Ana López",
        "correo": "ana@example.com",
        "telefono": "5555-0101",
        **overrides,
    }
    return client.post("/api/clientes", json=data)


def test_crear_cliente(client):
    response = crear_cliente(client)

    assert response.status_code == 201
    assert response.get_json() == {
        "id": 1,
        "nombre": "Ana López",
        "correo": "ana@example.com",
        "telefono": "5555-0101",
    }


def test_listar_clientes(client):
    primero = crear_cliente(client).get_json()
    segundo = crear_cliente(
        client,
        nombre="Luis Pérez",
        correo="luis@example.com",
        telefono=None,
    ).get_json()

    response = client.get("/api/clientes")

    assert response.status_code == 200
    assert [cliente["id"] for cliente in response.get_json()] == [
        segundo["id"],
        primero["id"],
    ]


def test_actualizar_cliente(client):
    cliente = crear_cliente(client).get_json()

    response = client.put(
        f"/api/clientes/{cliente['id']}",
        json={
            "nombre": "Ana Pérez",
            "correo": "ana.perez@example.com",
            "telefono": "5555-9999",
        },
    )

    assert response.status_code == 200
    assert response.get_json() == {
        "id": cliente["id"],
        "nombre": "Ana Pérez",
        "correo": "ana.perez@example.com",
        "telefono": "5555-9999",
    }


def test_eliminar_cliente(client):
    cliente = crear_cliente(client).get_json()

    response = client.delete(f"/api/clientes/{cliente['id']}")

    assert response.status_code == 204
    assert response.data == b""
    assert client.get("/api/clientes").get_json() == []


def test_correo_duplicado_devuelve_409(client):
    crear_cliente(client)

    response = crear_cliente(client, nombre="Otra persona")

    assert response.status_code == 409
    assert response.get_json() == {"error": "El correo ya está registrado"}


def test_faltan_campos_obligatorios_en_cliente(client):
    response = client.post(
        "/api/clientes",
        json={"nombre": "", "correo": ""},
    )

    assert response.status_code == 400
    assert response.get_json() == {"error": "Faltan campos obligatorios"}
