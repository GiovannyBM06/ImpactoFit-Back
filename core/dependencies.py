"""
dependencies.py
---------------
Registro de dependencias para inyección en FastAPI (Depends).

Equivalente al contenedor de DI de .NET (Program.cs).
Centraliza cómo se construye cada servicio y qué implementaciones
concretas se usan para cada interfaz.

Si en el futuro se cambia algún repositorio o servicio por una
implementación distinta (tests, mock, etc.), solo se modifica aquí.
Los controllers no se tocan.

Uso en un router:
    from core.dependencies import getClienteService

    @router.post("/asistencia")
    async def registrarAsistencia(
        body: AsistenciaRequest,
        service: IClienteService = Depends(getClienteService)
    ):
        return await service.registrarAsistencia(...)

Cadenas de construcción por servicio:

    UsuarioService:
        getDb() → AsyncSession → UsuarioRepository → UsuarioService

    ClienteService:
        getDb() → AsyncSession → ClienteService
        (recibe la sesión directamente porque las Templates también la necesitan)

    EntrenadorService:
        getDb() → AsyncSession → EntrenadorRepository → EntrenadorService

    AdminService:
        getDb() → AsyncSession → AdminRepository + AsyncSession → AdminService
        (recibe repo y sesión porque los Observers también necesitan la sesión)
"""
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from dataAccess.context.database import getDb

from dataAccess.repositories.UsuarioRepository import UsuarioRepository
from dataAccess.repositories.EntrenadorRepository import EntrenadorRepository
from dataAccess.repositories.AdminRepository import AdminRepository
from dataAccess.repositories.AuthRepository import AuthRepository

from domain.interfaces.services.IUsuarioService import IUsuarioService
from domain.interfaces.services.IClienteService import IClienteService
from domain.interfaces.services.IEntrenadorService import IEntrenadorService
from domain.interfaces.services.IAdminService import IAdminService
from domain.interfaces.services.IAuthService import IAuthService

from domain.services.UsuarioService import UsuarioService
from domain.services.ClienteService import ClienteService
from domain.services.EntrenadorService import EntrenadorService
from domain.services.AdminService import AdminService
from domain.services.AuthService import AuthService


# ── UsuarioService ────────────────────────────────────────────────────────────

def getUsuarioService(
    db: AsyncSession = Depends(getDb)
) -> IUsuarioService:
    """
    Cadena: AsyncSession → UsuarioRepository → UsuarioService
    """
    repo = UsuarioRepository(db)
    return UsuarioService(repo)


# ── ClienteService ────────────────────────────────────────────────────────────

def getClienteService(
    db: AsyncSession = Depends(getDb)
) -> IClienteService:
    """
    Cadena: AsyncSession → ClienteService

    ClienteService recibe la sesión directamente porque el patrón
    Template Method (RegistroAsistencia, RegistroInscripcion) también
    necesita la sesión para sus operaciones de BD.
    No hay repositorio intermediario en este servicio.
    """
    return ClienteService(db)


# ── EntrenadorService ─────────────────────────────────────────────────────────

def getEntrenadorService(
    db: AsyncSession = Depends(getDb)
) -> IEntrenadorService:
    """
    Cadena: AsyncSession → EntrenadorRepository → EntrenadorService
    """
    repo = EntrenadorRepository(db)
    return EntrenadorService(repo)


# ── AdminService ──────────────────────────────────────────────────────────────

def getAdminService(
    db: AsyncSession = Depends(getDb)
) -> IAdminService:
    """
    Cadena: AsyncSession → AdminRepository + AsyncSession → AdminService

    AdminService recibe tanto el repositorio como la sesión directamente
    porque el patrón Observer (ComprobanteObserver, EstadoUsuarioObserver)
    necesita la sesión para persistir sus cambios dentro de la misma
    transacción del servicio.
    """
    repo = AdminRepository(db)
    return AdminService(repo, db)

# ── AuthService ───────────────────────────────────────────────────────────────
 
def getAuthService(
    db: AsyncSession = Depends(getDb)
) -> IAuthService:
    """
    Cadena: AsyncSession → AuthRepository → AuthService
    """ 
    repo = AuthRepository(db)
    return AuthService(repo)