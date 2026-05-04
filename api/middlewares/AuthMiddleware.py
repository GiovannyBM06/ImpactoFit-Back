"""
authMiddleware.py
-----------------
Middleware de autenticación JWT para proteger los endpoints.

Provee dos dependencias inyectables:

    getCurrentUsuario()
        Verifica el JWT y retorna el usuario activo.
        Usado en cualquier endpoint que requiera autenticación.

    requireRol(*roles)
        Fábrica de dependencias que verifica el rol del usuario.
        Usado en endpoints que requieren un rol específico.

Uso en controllers:

    # Solo requiere autenticación
    @router.get("/mi-rutina")
    async def verRutina(
        usuario: Usuario = Depends(getCurrentUsuario)
    ):
        ...

    # Requiere rol específico
    @router.post("/clases")
    async def crearClase(
        usuario: Usuario = Depends(requireRol(RolEnum.ADMINISTRADOR))
    ):
        ...

    # Múltiples roles permitidos
    @router.get("/usuarios")
    async def listarUsuarios(
        usuario: Usuario = Depends(requireRol(RolEnum.ADMINISTRADOR, RolEnum.ENTRENADOR))
    ):
        ...
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from dataAccess.context.database import getDb
from domain.entities.Usuario import Usuario
from domain.enums.RolEnum import RolEnum
from core.config import settings
from jose import JWTError, jwt

# FastAPI extrae automáticamente el token del header:
# Authorization: Bearer <token>
oauth2Scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def getCurrentUsuario(
    token: str = Depends(oauth2Scheme),
    db: AsyncSession = Depends(getDb),
) -> Usuario:
    """
    Dependencia base: verifica el JWT y retorna el usuario activo.

    Raises:
        401: si el token es inválido, expiró o el usuario no existe.
        403: si el usuario está inactivo.
    """
    credencialesException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        email: str = payload.get("sub")
        if email is None:
            raise credencialesException

    except JWTError:
        raise credencialesException

    # Buscar usuario en BD
    resultado = await db.execute(
        select(Usuario).where(Usuario.email == email)
    )
    usuario = resultado.scalar_one_or_none()

    if usuario is None:
        raise credencialesException

    if not usuario.isActive:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Tu cuenta está inactiva. Comunícate con el administrador.",
        )

    return usuario


def requireRol(*roles: RolEnum):
    """
    Fábrica de dependencias para control de acceso por rol.

    Args:
        *roles: uno o más RolEnum permitidos para el endpoint

    Returns:
        Dependencia que verifica el rol del usuario autenticado.

    Raises:
        403: si el usuario no tiene ninguno de los roles requeridos.
    """
    async def verificarRol(
        usuario: Usuario = Depends(getCurrentUsuario)
    ) -> Usuario:
        if usuario.rol not in roles:
            rolesPermitidos = [r.value for r in roles]
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=(
                    f"Acceso denegado. "
                    f"Se requiere uno de los siguientes roles: {rolesPermitidos}"
                ),
            )
        return usuario

    return verificarRol