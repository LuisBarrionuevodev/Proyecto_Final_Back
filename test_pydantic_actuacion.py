# test_pydantic_actuacion.py

from pydantic import ValidationError

from app.schemas.actuacion import ActuacionBatch, ActuacionItem


def probar_item_valido():
    data = {
        "orden_trabajo_numero": " 123 ",
        "fecha_actuacion": "2025-11-16",
        "inspectores": ["perez", "gomez"],
        "calle": "alem",
        "numero": "477",
        "rubro_nombre": "almacen",
        "tipo_actuacion": "inspeccion",
        "contraproducencia": None,
        "doc_tipo_codigo": "dni",
        "doc_nro": "12345678",
        "contrib_apellido": "lopez",
        "contrib_nombre": "juan",
        "acta_inspeccion_num": "123",
        "acta_notificacion_num": "456",
        "notificacion_motivo_1": "FALTA HABILITACION",
        "notificacion_motivo_2": None,
        "notificacion_motivo_3": None,
        "acta_comprobacion_num": "789",
        "comprobacion_motivo": "INCUMPLIMIENTO PLAZO",
        "acta_clausura_num": None,
        "clausura_motivo": None,
        "acta_decomiso_num": None,
        "decomiso_kilos_total": None,
        "expediente_numero": "1234",
        "expediente_anio": 25,
        "oficio_numero": "567",
        "oficio_anio": 25,
        "oficio_causa": 12345,
        "notificacion_previa_num": None,
        "comprobacion_previa_num": None,
    }

    item = ActuacionItem(**data)
    print("✅ ITEM VÁLIDO")
    print(item)
    print("acta_inspeccion_num normalizada:", item.acta_inspeccion_num)
    print("acta_notificacion_num normalizada:", item.acta_notificacion_num)
    print("inspectores:", item.inspectores)


def probar_item_invalido():
    """
    Acá forzamos errores para ver cómo responde Pydantic.
    """
    data_mala = {
        # Falta orden_trabajo_numero
        "fecha_actuacion": "2025-11-16",
        "inspectores": [],
        "calle": "   ",
        "numero": "477",
        "rubro_nombre": "almacen",
        "tipo_actuacion": "cualquier cosa",  # no es un tipo válido
        "doc_tipo_codigo": "dni",
        "doc_nro": "",
        "contrib_apellido": "",
    }

    try:
        ActuacionItem(**data_mala)
    except ValidationError as e:
        print("\n❌ ITEM INVÁLIDO (como era de esperar)")
        print(e)


def probar_batch():
    """
    Probar el modelo ActuacionBatch con 2 filas.
    """
    data_batch = {
        "items": [
            {
                "orden_trabajo_numero": "111",
                "fecha_actuacion": "2025-11-16",
                "inspectores": ["perez"],
                "calle": "alem",
                "numero": "100",
                "rubro_nombre": "almacen",
                "tipo_actuacion": "inspeccion",
                "doc_tipo_codigo": "dni",
                "doc_nro": "12345678",
                "contrib_apellido": "lopez",
            },
            {
                "orden_trabajo_numero": "222",
                "fecha_actuacion": "2025-11-16",
                "inspectores": ["gomez"],
                "calle": "sarmiento",
                "numero": "200",
                "rubro_nombre": "bar",
                "tipo_actuacion": "reinspeccion",
                "doc_tipo_codigo": "dni",
                "doc_nro": "87654321",
                "contrib_apellido": "perez",
            },
        ]
    }

    batch = ActuacionBatch(**data_batch)
    print("\n✅ BATCH VÁLIDO, cantidad de items:", len(batch.items))


if __name__ == "__main__":
    probar_item_valido()
    probar_item_invalido()
    probar_batch()
