"""
Módulo: excepciones.py
Descripción: Define la jerarquía de excepciones personalizadas para el Sistema
Integral de Gestión de Clientes, Servicios y Reservas de Software FJ.
"""


class ErrorSoftwareFJ(Exception):
    """Excepción base para todos los errores controlados del sistema Software FJ."""
    pass


class DatosInvalidosError(ErrorSoftwareFJ):
    """Se lanza cuando un dato ingresado no cumple el formato o reglas de validación."""
    pass


class ParametroFaltanteError(ErrorSoftwareFJ):
    """Se lanza cuando falta un parámetro obligatorio para crear o procesar una entidad."""
    pass


class ServicioNoDisponibleError(ErrorSoftwareFJ):
    """Se lanza cuando se intenta reservar o usar un servicio que no está disponible."""
    pass


class ReservaInvalidaError(ErrorSoftwareFJ):
    """Se lanza cuando una operación de reserva (crear, confirmar, cancelar) no es permitida."""
    pass


class CalculoInconsistenteError(ErrorSoftwareFJ):
    """Se lanza cuando el cálculo de tarifas, impuestos o descuentos arroja valores incoherentes."""
    pass