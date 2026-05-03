"""
usuarioRepository.py
--------------------
Implementación concreta del repositorio de usuarios.

Hereda el CRUD base de GenericRepository e implementa los métodos
específicos definidos en IUsuarioRepository.

Responsabilidad clave:
    Este repositorio es el único lugar del sistema donde aparece
    el filtro por rol. Los servicios especializados (ClienteService,
    EntrenadorService, AdminService) llaman a los métodos de este
    repositorio sin preocuparse por los detalles de la query.

    Ejemplo:
        # En ClienteService (sin saber cómo se filtra en BD):
        clientes = self._repo.obtenerPorRol(RolEnum.CLIENTE)

        # Aquí adentro (encapsulado):
        WHERE rol = 'cliente'
"""

from sqlalchemy.orm import Session
from domain.entities.Usuario import Usuario
from domain.enums.RolEnum import RolEnum
from domain.interfaces.repositories.IUsuarioRepository import IUsuarioRepository
from dataAccess.repositories.GenericRepository import GenericRepository


class UsuarioRepository(GenericRepository[Usuario], IUsuarioRepository):
    """
    Repositorio concreto de usuarios.

    Hereda CRUD de GenericRepository[Usuario].
    Implementa métodos específicos de IUsuarioRepository.
    """

    def __init__(self, db: Session):
        # Le indica al GenericRepository qué modelo gestiona
        super().__init__(db, Usuario)

    # ── IUsuarioRepository implementation ────────────────────────────────────

    async def obtenerPorEmail(self, email: str) -> Usuario | None:
        """
        Búsqueda por email sin filtro de rol.
        Usada en el login: en ese momento no se sabe aún qué rol tiene el usuario.
        """
        return await self._db.query(Usuario).filter(
            Usuario.email == email
        ).first()

    async def existeEmail(self, email: str) -> bool:
        """
        Verificación de unicidad de email.
        Más eficiente que obtenerPorEmail porque solo hace COUNT en BD.
        """
        return await self._db.query(Usuario).filter(
            Usuario.email == email
        ).count() > 0

    async def obtenerPorRol(self, rol: RolEnum) -> list[Usuario]:
        """
        Lista usuarios filtrando por rol.
        El filtro está encapsulado aquí: ningún servicio escribe
        'WHERE rol = X' directamente.
        """
        return await self._db.query(Usuario).filter(
            Usuario.rol == rol
        ).all()

    async def actualizarResetToken(self, usuarioId: int, token: str | None) -> bool:
        """
        Actualiza el token de recuperación de contraseña.
        Recibe None para invalidarlo después de ser usado.
        """
        usuario = await self.obtenerPorId(usuarioId)
        if usuario is None:
            return False

        usuario.resetToken = token
        await self._db.commit()
        return True