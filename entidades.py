"""
Módulo: entidades.py
Descripción: Define la clase abstracta general del sistema (EntidadSistema)
y la clase Cliente con encapsulación estricta y validaciones robustas.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from excepciones import DatosInvalidosError, ParametroFaltanteError
from logger import log_sistema


class EntidadSistema(ABC):
    """
    Clase abstracta base que representa cualquier entidad general del sistema Software FJ.
    Obliga a las subclases a implementar validación e información resumida.
    """

    def __init__(self, codigo_id: str):
        if not codigo_id or not str(codigo_id).strip():
            raise ParametroFaltanteError("El identificador (ID) de la entidad es obligatorio.")
        self._codigo_id = str(codigo_id).strip()
        self._fecha_creacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @property
    def codigo_id(self) -> str:
        """Retorna el identificador único encapsulado."""
        return self._codigo_id

    @property
    def fecha_creacion(self) -> str:
        """Retorna la fecha y hora de registro de la entidad."""
        return self._fecha_creacion

    @abstractmethod
    def validar_datos(self) -> bool:
        """Método abstracto que valida la integridad de los atributos de la entidad."""
        pass

    @abstractmethod
    def obtener_detalle(self) -> str:
        """Método abstracto que devuelve una descripción formateada de la entidad."""
        pass


class Cliente(EntidadSistema):
    """
    Representa a un cliente de Software FJ.
    Aplica encapsulación mediante atributos privados y propiedades con validación estricta.
    """

    def __init__(self, documento: str, nombre: str, correo: str, telefono: str):
        super().__init__(documento)
        # Se asignan a través de los setters para ejecutar las validaciones desde la creación
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono
        self.validar_datos()
        log_sistema.info(f"Cliente registrado exitosamente: [{self._codigo_id}] {self._nombre}")

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str):
        if not valor or not str(valor).strip():
            raise ParametroFaltanteError("El nombre del cliente no puede estar vacío.")
        if len(str(valor).strip()) < 3:
            raise DatosInvalidosError(f"El nombre '{valor}' es demasiado corto (mínimo 3 caracteres).")
        self._nombre = str(valor).strip()

    @property
    def correo(self) -> str:
        return self._correo

    @correo.setter
    def correo(self, valor: str):
        if not valor or not str(valor).strip():
            raise ParametroFaltanteError("El correo electrónico del cliente es obligatorio.")
        correo_limpio = str(valor).strip()
        if "@" not in correo_limpio or "." not in correo_limpio.split("@")[-1]:
            raise DatosInvalidosError(f"Formato de correo electrónico inválido: '{correo_limpio}'.")
        self._correo = correo_limpio

    @property
    def telefono(self) -> str:
        return self._telefono

    @telefono.setter
    def telefono(self, valor: str):
        if not valor or not str(valor).strip():
            raise ParametroFaltanteError("El teléfono del cliente es obligatorio.")
        tel_limpio = str(valor).strip()
        if not tel_limpio.isdigit() or len(tel_limpio) < 7:
            raise DatosInvalidosError(f"Teléfono inválido '{tel_limpio}': debe contener al menos 7 dígitos numéricos.")
        self._telefono = tel_limpio

    def validar_datos(self) -> bool:
        """Verifica que el documento tenga formato numérico válido y todos los campos estén completos."""
        if not self._codigo_id.isdigit() or len(self._codigo_id) < 5:
            raise DatosInvalidosError(
                f"Documento de identidad inválido '{self._codigo_id}': debe ser numérico de al menos 5 dígitos."
            )
        return True

    def obtener_detalle(self) -> str:
        return (
            f"Cliente [ID: {self._codigo_id}] | Nombre: {self._nombre} | "
            f"Correo: {self._correo} | Tel: {self._telefono}"
        )