"""
Módulo: main.py
Descripción: Punto de entrada del Sistema Integral de Gestión de Clientes,
Servicios y Reservas de Software FJ. Gestiona colecciones en memoria (listas)
sin base de datos, incluye menú interactivo y ejecuta una simulación de 12
operaciones completas (válidas e inválidas) demostrando estabilidad ante errores.
"""

from typing import List
from entidades import Cliente
from servicios import Servicio, ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from reservas import Reserva
from excepciones import (
    ErrorSoftwareFJ,
    DatosInvalidosError,
    ParametroFaltanteError,
    ServicioNoDisponibleError,
    ReservaInvalidaError,
    CalculoInconsistenteError,
)
from logger import log_sistema


class SistemaGestionFJ:
    """Controlador principal del sistema usando listas en memoria (sin bases de datos)."""

    def __init__(self):
        self.clientes: List[Cliente] = []
        self.servicios: List[Servicio] = []
        self.reservas: List[Reserva] = []
        log_sistema.info("=== INICIO DE SESIÓN DEL SISTEMA SOFTWARE FJ ===")

    def registrar_cliente(self, documento: str, nombre: str, correo: str, telefono: str) -> Cliente:
        for existente in self.clientes:
            if existente.codigo_id == str(documento).strip():
                raise DatosInvalidosError(f"Ya existe un cliente registrado con documento '{documento}'.")
        nuevo_cliente = Cliente(documento, nombre, correo, telefono)
        self.clientes.append(nuevo_cliente)
        return nuevo_cliente

    def registrar_servicio(self, servicio: Servicio) -> Servicio:
        for existente in self.servicios:
            if existente.codigo_id == servicio.codigo_id:
                raise DatosInvalidosError(f"Ya existe un servicio con código '{servicio.codigo_id}'.")
        self.servicios.append(servicio)
        return servicio

    def crear_reserva(self, codigo_reserva: str, documento_cliente: str, codigo_servicio: str,
                      duracion_horas: int, descuento: float = 0.0, iva: float = 0.19) -> Reserva:
        cliente = next((c for c in self.clientes if c.codigo_id == documento_cliente), None)
        if cliente is None:
            raise ParametroFaltanteError(f"No se encontró cliente con documento '{documento_cliente}'.")

        servicio = next((s for s in self.servicios if s.codigo_id == codigo_servicio), None)
        if servicio is None:
            raise ParametroFaltanteError(f"No se encontró servicio con código '{codigo_servicio}'.")

        nueva_reserva = Reserva(codigo_reserva, cliente, servicio, duracion_horas, descuento, iva)
        self.reservas.append(nueva_reserva)
        return nueva_reserva


def ejecutar_simulacion_operaciones(sistema: SistemaGestionFJ) -> None:
    """
    Ejecuta 12 operaciones completas (válidas e inválidas) para validar que
    el sistema registra los errores en sistema_fj.log y continúa operando sin detenerse.
    """
    print("\n" + "=" * 75)
    print("EJECUTANDO SIMULACIÓN DE 12 OPERACIONES COMPLETAS - SOFTWARE FJ")
    print("=" * 75)

    # --- OPERACIÓN 1 (VÁLIDA): Registro correcto de clientes ---
    try:
        print("\n[Operación 1 - Válida] Registrando clientes válidos...")
        c1 = sistema.registrar_cliente("1065890123", "Laura Sofía Mendoza", "laura.mendoza@correo.com", "3104567890")
        c2 = sistema.registrar_cliente("77192834", "Carlos Andrés Bermúdez", "cbermudez@empresa.co", "3009876543")
        print(f"  -> OK: {c1.obtener_detalle()}")
        print(f"  -> OK: {c2.obtener_detalle()}")
    except ErrorSoftwareFJ as err:
        log_sistema.error(f"Operación 1 fallida inesperadamente: {err}")

    # --- OPERACIÓN 2 (INVÁLIDA): Registro de cliente con correo y teléfono erróneos ---
    try:
        print("\n[Operación 2 - Inválida] Intentando registrar cliente con datos inválidos...")
        sistema.registrar_cliente("99887766", "Pedro Pérez", "correo_sin_arroba.com", "123")
    except ErrorSoftwareFJ as err:
        log_sistema.error(f"[Op. 2 Controlada] Registro inválido de cliente: {err}")
        print(f"  -> ERROR CONTROLADO ({type(err).__name__}): {err}")

    # --- OPERACIÓN 3 (INVÁLIDA): Registro de cliente con parámetro faltante ---
    try:
        print("\n[Operación 3 - Inválida] Intentando registrar cliente sin nombre...")
        sistema.registrar_cliente("88776655", "", "ana@correo.com", "3151234567")
    except ErrorSoftwareFJ as err:
        log_sistema.error(f"[Op. 3 Controlada] Parámetro faltante en cliente: {err}")
        print(f"  -> ERROR CONTROLADO ({type(err).__name__}): {err}")

    # --- OPERACIÓN 4 (VÁLIDA): Creación de los 3 servicios especializados ---
    try:
        print("\n[Operación 4 - Válida] Creando catálogo de servicios especializados...")
        s1 = ReservaSala("SRV-01", "Sala Innovación Norte", 80000.0, capacidad_personas=12, tiene_videoconferencia=True)
        s2 = AlquilerEquipo("SRV-02", "Workstation Ryzen 9 RTX", 35000.0, tipo_equipo="Estación Gráfica", serial_inventario="INV-9021")
        s3 = AsesoriaEspecializada("SRV-03", "Arquitectura Cloud & DevOps", 120000.0, especialidad="Cloud Computing", consultor_asignado="Ing. Ricardo Perales")
        s4 = ReservaSala("SRV-04", "Sala Juntas Sur (En Mantenimiento)", 60000.0, capacidad_personas=6, disponible=False)
        for srv in (s1, s2, s3, s4):
            sistema.registrar_servicio(srv)
            print(f"  -> OK: {srv.describir_servicio()}")
    except ErrorSoftwareFJ as err:
        log_sistema.error(f"Operación 4 fallida inesperadamente: {err}")

    # --- OPERACIÓN 5 (INVÁLIDA): Creación incorrecta de servicio (tarifa negativa) ---
    try:
        print("\n[Operación 5 - Inválida] Intentando crear servicio con tarifa base negativa...")
        servicio_malo = AlquilerEquipo("SRV-99", "Portátil Básico", -15000.0, "Laptop", "SN-001")
        sistema.registrar_servicio(servicio_malo)
    except ErrorSoftwareFJ as err:
        log_sistema.error(f"[Op. 5 Controlada] Creación incorrecta de servicio: {err}")
        print(f"  -> ERROR CONTROLADO ({type(err).__name__}): {err}")

    # --- OPERACIÓN 6 (VÁLIDA): Reserva exitosa de Sala + Confirmación + Procesamiento ---
    try:
        print("\n[Operación 6 - Válida] Creando, confirmando y procesando reserva de sala...")
        r1 = sistema.crear_reserva("RES-101", "1065890123", "SRV-01", duracion_horas=3, descuento=0.10)
        r1.confirmar_reserva()
        factura = r1.procesar_reserva()
        print(f"  -> OK: Reserva procesada | Total pagado: ${factura['total_pagado']:,.2f}")
    except ErrorSoftwareFJ as err:
        log_sistema.error(f"Operación 6 fallida inesperadamente: {err}")

    # --- OPERACIÓN 7 (VÁLIDA): Reserva exitosa de Asesoría con descuento automático (>= 4h) ---
    try:
        print("\n[Operación 7 - Válida] Creando y confirmando asesoría especializada de 5 horas...")
        r2 = sistema.crear_reserva("RES-102", "77192834", "SRV-03", duracion_horas=5)
        r2.confirmar_reserva()
        print(f"  -> OK: {r2.obtener_detalle()}")
    except ErrorSoftwareFJ as err:
        log_sistema.error(f"Operación 7 fallida inesperadamente: {err}")

    # --- OPERACIÓN 8 (INVÁLIDA): Intento de reserva sobre servicio no disponible ---
    try:
        print("\n[Operación 8 - Inválida] Intentando reservar sala en mantenimiento (no disponible)...")
        sistema.crear_reserva("RES-103", "1065890123", "SRV-04", duracion_horas=2)
    except ErrorSoftwareFJ as err:
        log_sistema.error(f"[Op. 8 Controlada] Servicio no disponible: {err}")
        print(f"  -> ERROR CONTROLADO ({type(err).__name__}): {err}")

    # --- OPERACIÓN 9 (INVÁLIDA): Reserva con duración inválida y encadenamiento de excepciones ---
    try:
        print("\n[Operación 9 - Inválida] Intentando alquilar equipo por 1 hora (mínimo exigido: 2h)...")
        sistema.crear_reserva("RES-104", "77192834", "SRV-02", duracion_horas=1)
    except ErrorSoftwareFJ as err:
        causa = err.__cause__
        log_sistema.error(f"[Op. 9 Controlada] {err} | Causa encadenada: {causa}")
        print(f"  -> ERROR CONTROLADO ({type(err).__name__}): {err}")
        print(f"     Causa encadenada: {type(causa).__name__} -> {causa}")

    # --- OPERACIÓN 10 (INVÁLIDA): Cálculo inconsistente (descuento mayor al 100%) ---
    try:
        print("\n[Operación 10 - Inválida] Intentando calcular costo con descuento inconsistente (150%)...")
        sistema.crear_reserva("RES-105", "1065890123", "SRV-02", duracion_horas=4, descuento=1.5)
    except ErrorSoftwareFJ as err:
        causa = err.__cause__
        log_sistema.error(f"[Op. 10 Controlada] {err} | Causa encadenada: {causa}")
        print(f"  -> ERROR CONTROLADO ({type(err).__name__}): {err}")

    # --- OPERACIÓN 11 (VÁLIDA): Cancelación controlada de una reserva confirmada ---
    try:
        print("\n[Operación 11 - Válida] Cancelando reserva RES-102 y liberando servicio...")
        r2.cancelar_reserva("Reprogramación solicitada por el cliente")
        print(f"  -> OK: Estado actual -> {r2.estado} | Servicio disponible -> {r2.servicio.disponible}")
    except ErrorSoftwareFJ as err:
        log_sistema.error(f"Operación 11 fallida inesperadamente: {err}")

    # --- OPERACIÓN 12 (INVÁLIDA): Operación no permitida (confirmar reserva ya cancelada) ---
    try:
        print("\n[Operación 12 - Inválida] Intentando confirmar nuevamente la reserva ya cancelada RES-102...")
        r2.confirmar_reserva()
    except ErrorSoftwareFJ as err:
        print(f"  -> ERROR CONTROLADO ({type(err).__name__}): {err}")

    print("\n" + "=" * 75)
    print("SIMULACIÓN FINALIZADA SIN INTERRUPCIONES.")
    print("Todos los eventos y errores quedaron registrados en 'sistema_fj.log'.")
    print("=" * 75 + "\n")


def menu_interactivo():
    """Menú principal de consola para operar el sistema o lanzar las pruebas simuladas."""
    sistema = SistemaGestionFJ()

    while True:
        print("\n--- SISTEMA INTEGRAL SOFTWARE FJ (POO & EXCEPCIONES) ---")
        print("1. Ejecutar simulación completa de 12 operaciones (Válidas e Inválidas)")
        print("2. Registrar nuevo cliente")
        print("3. Listar clientes y servicios registrados")
        print("4. Crear y confirmar reserva")
        print("5. Salir")

        opcion = input("Seleccione una opción (1-5): ").strip()

        try:
            if opcion == "1":
                ejecutar_simulacion_operaciones(sistema)
            elif opcion == "2":
                doc = input("Documento de identidad: ")
                nom = input("Nombre completo: ")
                cor = input("Correo electrónico: ")
                tel = input("Teléfono: ")
                cliente = sistema.registrar_cliente(doc, nom, cor, tel)
                print(f"Cliente registrado: {cliente.obtener_detalle()}")
            elif opcion == "3":
                print("\nClientes en memoria:")
                for c in sistema.clientes:
                    print(" -", c.obtener_detalle())
                print("\nServicios en memoria:")
                for s in sistema.servicios:
                    print(" -", s.obtener_detalle())
            elif opcion == "4":
                cod = input("Código de reserva (ej. RES-201): ")
                doc = input("Documento del cliente: ")
                srv = input("Código del servicio (ej. SRV-01): ")
                hrs = int(input("Duración en horas: "))
                reserva = sistema.crear_reserva(cod, doc, srv, hrs)
                reserva.confirmar_reserva()
                print(f"Reserva confirmada: {reserva.obtener_detalle()}")
            elif opcion == "5":
                log_sistema.info("=== CIERRE NORMAL DEL SISTEMA SOFTWARE FJ ===")
                print("Saliendo del sistema Software FJ...")
                break
            else:
                print("Opción no válida. Ingrese un número entre 1 y 5.")
        except ValueError as err_val:
            log_sistema.error(f"Error de conversión de entrada en menú: {err_val}")
            print(f"Error de entrada: debe ingresar un valor numérico válido ({err_val}).")
        except ErrorSoftwareFJ as err_sys:
            log_sistema.error(f"Error controlado en menú interactivo: {err_sys}")
            print(f"Operación rechazada [{type(err_sys).__name__}]: {err_sys}")


if __name__ == "__main__":
    menu_interactivo()