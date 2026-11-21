"""
Módulo: servicios.py
Descripción: Define la clase abstracta Servicio y los tres servicios especializados
de Software FJ (ReservaSala, AlquilerEquipo y AsesoriaEspecializada), aplicando
herencia, polimorfismo, sobrescritura y sobrecarga de métodos de cálculo.
"""

from abc import abstractmethod
from entidades import EntidadSistema
from excepciones import (
    DatosInvalidosError,
    ParametroFaltanteError,
    CalculoInconsistenteError,
)
from logger import log_sistema


class Servicio(EntidadSistema):
    """
    Clase abstracta que modela un servicio ofrecido por Software FJ.
    """

    def __init__(self, codigo_servicio: str, nombre_servicio: str, tarifa_base: float, disponible: bool = True):
        super().__init__(codigo_servicio)
        if not nombre_servicio or not str(nombre_servicio).strip():
            raise ParametroFaltanteError("El nombre del servicio es obligatorio.")
        if tarifa_base is None or tarifa_base <= 0:
            raise DatosInvalidosError(f"La tarifa base debe ser mayor a cero (valor recibido: {tarifa_base}).")

        self._nombre_servicio = str(nombre_servicio).strip()
        self._tarifa_base = float(tarifa_base)
        self._disponible = bool(disponible)

    @property
    def nombre_servicio(self) -> str:
        return self._nombre_servicio

    @property
    def tarifa_base(self) -> float:
        return self._tarifa_base

    @property
    def disponible(self) -> bool:
        return self._disponible

    @disponible.setter
    def disponible(self, estado: bool):
        self._disponible = bool(estado)

    @abstractmethod
    def validar_parametros_servicio(self, horas: int) -> bool:
        """Valida las reglas específicas de duración o uso según el tipo de servicio."""
        pass

    @abstractmethod
    def describir_servicio(self) -> str:
        """Retorna la ficha técnica y características específicas del servicio."""
        pass

    def calcular_costo(self, horas: int, descuento: float = 0.0, iva: float = 0.19) -> float:
        """
        Método sobrecargado mediante parámetros opcionales:
        Permite calcular el costo total solo con horas, aplicando descuento opcional,
        o personalizando el porcentaje de impuesto (IVA).
        """
        if horas <= 0:
            raise CalculoInconsistenteError(f"Las horas reservadas deben ser positivas (recibido: {horas}).")
        if not (0.0 <= descuento < 1.0):
            raise CalculoInconsistenteError(
                f"Descuento fuera de rango permitido [0.0 - 0.99]: {descuento}."
            )
        if iva < 0:
            raise CalculoInconsistenteError(f"El porcentaje de impuesto no puede ser negativo: {iva}.")

        subtotal = self._tarifa_base * horas
        valor_descuento = subtotal * descuento
        base_gravable = subtotal - valor_descuento
        total = base_gravable * (1 + iva)

        if total <= 0:
            raise CalculoInconsistenteError("El cálculo arrojó un valor total nulo o negativo.")

        return round(total, 2)

    def validar_datos(self) -> bool:
        return self._tarifa_base > 0 and len(self._nombre_servicio) > 0

    def obtener_detalle(self) -> str:
        estado = "Disponible" if self._disponible else "No disponible"
        return f"[{self._codigo_id}] {self._nombre_servicio} - ${self._tarifa_base:,.2f}/hora ({estado})"


class ReservaSala(Servicio):
    """Servicio especializado 1: Reserva de salas tecnológicas y salas de juntas."""

    def __init__(self, codigo_servicio: str, nombre_servicio: str, tarifa_base: float,
                 capacidad_personas: int, tiene_videoconferencia: bool = True, disponible: bool = True):
        super().__init__(codigo_servicio, nombre_servicio, tarifa_base, disponible)
        if capacidad_personas is None or capacidad_personas <= 0:
            raise DatosInvalidosError("La capacidad de la sala debe ser mayor a cero.")
        self._capacidad_personas = int(capacidad_personas)
        self._tiene_videoconferencia = bool(tiene_videoconferencia)
        log_sistema.info(f"Servicio de Sala creado: {self.obtener_detalle()}")

    def validar_parametros_servicio(