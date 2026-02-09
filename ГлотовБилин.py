from datetime import datetime
import uuid
def add_client(name, **kwargs):
    new_id = str(uuid.uuid4())
    client_doc = {
        "name": name,
        **kwargs
    }
    print(f" Новый документ клиента создан: {client_doc}")
    return client_doc
add_client("Филиция", sketch_url="filicia_flower.jpg")
add_client("Абдул", appointment="2026-02-15", master="Иван")
add_client("Антонина", allergies=["latex", "red_ink"], emergency_contact="+79991234567")

