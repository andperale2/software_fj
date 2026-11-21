"""
Módulo: logger.py
Descripción: Configura y gestiona el archivo de logs (sistema_fj.log) para registrar
eventos relevantes y errores controlados del sistema Software FJ.
"""

import logging


def configurar_logger(nombre_archivo: str = "sistema_fj.log") -> logging.Logger:
    """
    Inicializa el registrador de eventos en archivo plano UTF-8.
    Cada registro incluye fecha/hora, nivel (INFO/ERROR) y descripción del suceso.
    """
    logger = logging.getLogger("SoftwareFJ")
    logger.setLevel(logging.INFO)

    # Evita duplicar manejadores si se importa varias veces
    if not logger.handlers:
        archivo_handler = logging.FileHandler(nombre_archivo, mode="a", encoding="utf-8")
        formato = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-7s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        archivo_handler.setFormatter(formato)
        logger.addHandler(archivo_handler)

    return logger


# Instancia global compartida por todos los módulos del sistema
log_sistema = configurar_logger()