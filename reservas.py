"""
Módulo: reservas.py
Descripción: Implementa la clase Reserva que integra Cliente, Servicio, duración
y estado, aplicando confirmación, cancelación, procesamiento con bloques
try/except/else/finally y encadenamiento de excepciones.
"""

from entidades import EntidadSistema, Cliente
from servicios import Servicio
from excepciones import (
    ErrorSoftwareFJ,
    DatosInvalidosError,
    ParametroFaltanteError,
    ServicioNoDisponibleError,
    ReservaInvalidaError,
    CalculoInconsistenteError,
)
from logger import log_sistema


class Reserva(EntidadSistema):
    """
    Gestiona el ciclo de vida de una reserva en Software FJ:
    Estados posibles: 'PENDIENTE', 'CONFIRMADA', 'PROCESADA', 'CANCELADA'.
    """

    def __init__(self, codigo_reserva: str, cliente: Cliente, servicio: Servicio,
                 duracion_horas: int, descuento: float = 0.0, iva: float = 0.19):
        super().__init__(codigo_reserva)

        if not isinstance(cliente, Cliente):
            raise ParametroFaltanteError("Se requiere una instancia válida de Cliente para crear la reserva.")
        if not isinstance(servicio, Servicio):
            raise ParametroFaltanteError("Se requiere una instancia válida de Servicio para crear la reserva.")
        if not servicio.disponible:
            raise ServicioNoDisponibleError(
                f"El servicio '{servicio.nombre_servicio}' [{servicio.codigo_id}] no se encuentra disponible."
            )

        self._cliente = cliente
        self._servicio = servicio
        self._duracion_horas = duracion_horas
        self._descuento = descuento
        self._iva = iva
        self._estado = "PENDIENTE"
        self._costo_total = 0.0

        # Validación y cálculo inicial con encadenamiento de excepciones
        try:
            self.validar_datos()
            self._costo_total = self._servicio.calcular_costo(
                self._duracion_horas, self._descuento, self._iva
            )
        except (DatosInvalidosError, CalculoInconsistenteError) as error_origen:
            raise ReservaInvalidaError(
                f"Fallo al inicializar la reserva [{self._codigo_id}] por parámetros inválidos."
            ) from error_origen

        log_sistema.info(
            f"Reserva creada en estado PENDIENTE: [{self._codigo_id}] | "
            f"Cliente: {self._cliente.nombre} | Servicio: {self._servicio.nombre_servicio} | "
            f"Total estimado: ${self._costo_total:,.2f}"
        )

    @property
    def estado(self) -> str:
        return self._estado

    @property
    def costo_total(self) -> float:
        return self._costo_total

    @property
    def cliente(self) -> Cliente:
        return self._cliente

    @property
    def servicio(self) -> Servicio:
        return self._servicio

    def validar_datos(self) -> bool:
        if not isinstance(self._duracion_horas, int) or self._duracion_horas <= 0:
            raise DatosInvalidosError(
                f"La duración de la reserva debe ser un entero positivo (recibido: {self._duracion_horas})."
            )
        return self._servicio.validar_parametros_servicio(self._duracion_horas)

    def confirmar_reserva(self) -> bool:
        """
        Confirma una reserva pendiente utilizando estructura try / except / else.
        Marca el servicio como ocupado temporalmente.
        """
        try:
            if self._estado != "PENDIENTE":
                raise ReservaInvalidaError(
                    f"No se puede confirmar la reserva [{self._codigo_id}] porque su estado es '{self._estado}'."
                )
            if not self._servicio.disponible:
                raise ServicioNoDisponibleError(
                    f"El servicio '{self._servicio.nombre_servicio}' ya fue ocupado por otra reserva."
                )
        except ErrorSoftwareFJ as err:
            log_sistema.error(f"Error al confirmar reserva [{self._codigo_id}]: {err}")
            raise
        else:
            self._estado = "CONFIRMADA"
            self._servicio.disponible = False
            log_sistema.info(f"Reserva CONFIRMADA: [{self._codigo_id}] para {self._cliente.nombre}.")
            return True

    def cancelar_reserva(self, motivo: str = "Solicitud del cliente") -> bool:
        """
        Cancela una reserva activa (PENDIENTE o CONFIRMADA) y libera el servicio.
        """
        try:
            if self._estado in ("CANCELADA", "PROCESADA"):
                raise ReservaInvalidaError(
                    f"Operación no permitida: la reserva [{self._codigo_id}] ya está '{self._estado}'."
                )
        except ReservaInvalidaError as err:
            log_sistema.error(f"Error al cancelar reserva [{self._codigo_id}]: {err}")
            raise
        else:
            estado_anterior = self._estado
            self._estado = "CANCELADA"
            if estado_anterior == "CONFIRMADA":
                self._servicio.disponible = True
            log_sistema.info(
                f"Reserva CANCELADA: [{self._codigo_id}] (antes {estado_anterior}). Motivo: {motivo}"
            )
            return True

    def procesar_reserva(self) -> dict:
        """
        Procesa el cierre y facturación de una reserva confirmada.
        Implementa el bloque completo try / except / else / finally y
        encadenamiento de excepciones.
        """
        auditoria_cerrada = False
        try:
            if self._estado != "CONFIRMADA":
                raise ReservaInvalidaError(
                    f"Solo se pueden procesar reservas CONFIRMADAS (estado actual: '{self._estado}')."
                )
            # Recalcula para verificar consistencia financiera antes de facturar
            valor_final = self._servicio.calcular_costo(
                self._duracion_horas, self._descuento, self._iva
            )
            if valor_final != self._costo_total:
                raise CalculoInconsistenteError(
                    f"Discrepancia en el valor facturado: esperado ${self._costo_total}, calculado ${valor_final}."
                )
        except (DatosInvalidosError, CalculoInconsistenteError) as err_calculo:
            log_sistema.error(f"Fallo de cálculo procesando reserva [{self._codigo_id}]: {err_calculo}")
            raise ReservaInvalidaError(
                f"Error crítico de facturación en reserva [{self._codigo_id}]."
            ) from err_calculo
        except ReservaInvalidaError as err_estado:
            log_sistema.error(f"Fallo de estado procesando reserva [{self._codigo_id}]: {err_estado}")
            raise
        else:
            self._estado = "PROCESADA"
            self._servicio.disponible = True
            log_sistema.info(
                f"Reserva PROCESADA y facturada: [{self._codigo_id}] | Total: ${self._costo_total:,.2f}"
            )
            return {
                "codigo_reserva": self._codigo_id,
                "cliente": self._cliente.nombre,
                "servicio": self._servicio.nombre_servicio,
                "horas": self._duracion_horas,
                "total_pagado": self._costo_total,
                "estado": self._estado,
            }
        finally:
            auditoria_cerrada = True
            log_sistema.info(
                f"Auditoría de procesamiento finalizada para reserva [{self._codigo_id}] "
                f"(auditoria_cerrada={auditoria_cerrada})."
            )

    def obtener_detalle(self) -> str:
        return (
            f"Reserva [{self._codigo_id}] | Estado: {self._estado} | "
            f"Cliente: {self._cliente.nombre} | Servicio: {self._servicio.nombre_servicio} | "
            f"Duración: {self._duracion_horas}h | Total: ${self._costo_total:,.2f}"
        )