"""
Entidad Usuario. Representa a cualquier persona registrada en el sistema,
independientemente de su rol (cliente, entrenador, administrador).
El rol determina qué funcionalidades tiene disponibles.
"""

from sqlalchemy import Column, String, Boolean, Enum, Date
from sqlalchemy.orm import relationship
from domain.entities.AuditBase import AuditBase
from domain.enums.RolEnum import RolEnum


class Usuario(AuditBase):
    """
    Tabla: usuarios

    Relaciones:
        CLIENTE     → una Membresia, una Rutina asignada, muchas Asistencias,
                      muchas Inscripciones a ClaseGrupal
        ENTRENADOR  → muchas Rutinas creadas, muchas ClasesGrupales dictadas
        ADMIN       → muchos Pagos confirmados
    """

    __tablename__ = "usuarios"


    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    documento  = Column(String(20), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)
    telefono = Column(String(20), nullable=True)
    fechaNacimiento = Column(Date, nullable=False)
    #Autenticacion
    passwordHash = Column(String(255), nullable=False)
    resetToken = Column(String(255), nullable=True)
    # Control de Acceso
    rol = Column(Enum(RolEnum), nullable=False, default=RolEnum.CLIENTE)
    isActive = Column(Boolean, default=True, nullable=False)
    
    
    #Relaciones 

    # CLIENTE: una membresía activa a la vez (RN01)
    membresia = relationship(
        "Membresia",
        back_populates="usuario",
        uselist=False  # one-to-one
    )

    # Un cliente tiene una rutina asignada por su entrenador
    rutina = relationship(
        "Rutina",
        back_populates="cliente",
        foreign_keys="Rutina.clienteId",
        uselist=False
    )

    # Las rutinas que un entrenador ha creado
    rutinasCreadas = relationship(
        "Rutina",
        back_populates="entrenador",
        foreign_keys="Rutina.entrenadorId"
    )

    # CLIENTE: registros de ingreso al gimnasio
    asistencias = relationship(
        "Asistencia",
        back_populates="usuario"
    )

    # CLIENTE: inscripciones a clases grupales
    inscripciones = relationship(
        "Inscripcion",
        back_populates="usuario"
    )

    # ENTRENADOR: clases grupales que dicta
    clasesGrupales = relationship(
        "ClaseGrupal",
        back_populates="entrenador",
        foreign_keys="ClaseGrupal.entrenadorId"
    )

    # ADMIN: pagos que ha confirmado manualmente
    pagosConfirmados = relationship(
        "Pago",
        back_populates="confirmadoPorAdmin",
        foreign_keys="Pago.confirmadoPorId"
    )


    def __repr__(self):
        return f"<Usuario id={self.id} email={self.email} rol={self.rol}>"