"""
usuario.py
----------
Entidad Usuario. Representa a cualquier persona registrada en el sistema,
independientemente de su rol (cliente, entrenador, administrador).
El rol determina qué funcionalidades tiene disponibles.
"""

from sqlalchemy import Column, String, Boolean, Enum
from sqlalchemy.orm import relationship
from domain.entities.AuditBase import AuditBase
from domain.enums.rolEnum import RolEnum


class Usuario(AuditBase):
    """
    Tabla: usuarios

    Relaciones:
        - Un Usuario CLIENTE tiene una Membresía y una Rutina asignada
        - Un Usuario ENTRENADOR tiene múltiples clientes asignados
        - Un Usuario puede registrar múltiples Asistencias
        - Un Usuario puede inscribirse a múltiples ClasesGrupales
    """

    __tablename__ = "usuarios"

    # Datos personales
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)
    telefono = Column(String(20), nullable=True)

    # Autenticación
    password_hash = Column(String(255), nullable=False)

    # Control de acceso
    rol = Column(Enum(RolEnum), nullable=False, default=RolEnum.CLIENTE)
    is_active = Column(Boolean, default=True, nullable=False)

    # Token para recuperación de contraseña (se genera al solicitarla)
    reset_token = Column(String(255), nullable=True)

    # ── Relaciones ──────────────────────────────────────────────────────────

    # Un cliente tiene una sola membresía activa a la vez (RN01)
    membresia = relationship(
        "Membresia",
        back_populates="usuario",
        uselist=False  # one-to-one
    )

    # Un cliente tiene una rutina asignada por su entrenador
    rutina = relationship(
        "Rutina",
        back_populates="cliente",
        foreign_keys="Rutina.cliente_id",
        uselist=False
    )

    # Las rutinas que un entrenador ha creado
    rutinas_asignadas = relationship(
        "Rutina",
        back_populates="entrenador",
        foreign_keys="Rutina.entrenador_id"
    )

    # Registros de asistencia del usuario
    asistencias = relationship(
        "Asistencia",
        back_populates="usuario"
    )

    # Inscripciones a clases grupales
    inscripciones = relationship(
        "Inscripcion",
        back_populates="usuario"
    )

    def __repr__(self):
        return f"<Usuario id={self.id} email={self.email} rol={self.rol}>"