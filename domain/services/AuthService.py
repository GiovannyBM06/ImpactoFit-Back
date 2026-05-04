"""
authService.py
--------------
Implementación del servicio de autenticación.

Responsabilidades:
    - Validar credenciales y generar JWT (login)
    - Cierre de sesión manual (logout)
    - Generar token de recuperación y enviar email (solicitarRecuperacionPassword)
    - Validar token y actualizar contraseña (resetearPassword)
    - Verificar y decodificar JWT (verificarToken)

Dependencias:
    - IAuthRepository : operaciones de BD
    - passlib          : verificación de contraseña hasheada
    - python-jose      : generación y verificación de JWT
    - fastapi-mail     : envío de email con template HTML
    - jinja2           : renderizado del template HTML del email
"""

import secrets
from datetime import datetime, timedelta, timezone
from pathlib import Path

from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from jinja2 import Environment, FileSystemLoader

from core.config import settings
from domain.interfaces.repositories.IAuthRepository import IAuthRepository
from domain.interfaces.services.IAuthService import IAuthService


# ── Configuración de herramientas ─────────────────────────────────────────────

pwdContext = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configuración de FastMail con las variables del .env
mailConfig = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
)

# Configuración de Jinja2 para renderizar el template HTML del email
# La carpeta templates/ debe estar en la raíz del proyecto
templateEnv = Environment(
    loader=FileSystemLoader(
        Path(__file__).resolve().parent.parent.parent / "templates" / "email"
    )
)


class AuthService(IAuthService):

    def __init__(self, repo: IAuthRepository):
        self._repo = repo

    # ── Login ─────────────────────────────────────────────────────────────────

    async def login(self, email: str, password: str) -> dict:
        """
        Valida credenciales y retorna JWT con datos del usuario.
        """

        # Buscar usuario por email
        usuario = await self._repo.obtenerPorEmail(email)

        if usuario is None:
            raise ValueError("Credenciales incorrectas")

        # Verificar contraseña contra el hash almacenado
        if not pwdContext.verify(password, usuario.passwordHash):
            raise ValueError("Credenciales incorrectas")

        # Verificar que el usuario esté activo
        if not usuario.isActive:
            raise ValueError("Tu cuenta está inactiva. Comunícate con el administrador.")

        # Generar JWT
        token = self._generarJWT(
            email=usuario.email,
            rol=usuario.rol.value,
            usuarioId=usuario.id,
        )

        return {
            "accessToken": token,
            "tokenType":   "bearer",
            "rol":         usuario.rol.value,
            "usuarioId":   usuario.id,
            "nombre":      f"{usuario.nombre} {usuario.apellido}",
        }

    # ── Logout ────────────────────────────────────────────────────────────────

    async def logout(self, token: str) -> dict:
        """
        Logout stateless: valida que el token sea válido y retorna confirmación.

        En el MVP el cliente simplemente descarta el token.
        En fases posteriores se puede implementar una blacklist en Redis.
        """
        try:
            self.verificarToken(token)
        except ValueError:
            raise ValueError("Token inválido o ya expirado")

        return {"mensaje": "Sesión cerrada exitosamente"}

    # ── Recuperación de contraseña ────────────────────────────────────────────

    async def solicitarRecuperacionPassword(self, email: str) -> dict:
        """
        Genera token de recuperación y envía email con enlace.

        Retorna el mismo mensaje independientemente de si el email
        existe o no, para no revelar qué usuarios están registrados.
        """
        mensajeSeguro = {
            "mensaje": "Si el email está registrado recibirás un correo con las instrucciones."
        }

        usuario = await self._repo.obtenerPorEmail(email)
        if usuario is None:
            # Retornamos el mensaje seguro sin revelar que el email no existe
            return mensajeSeguro

        # Generar token seguro de 32 bytes
        resetToken = secrets.token_urlsafe(32)

        # Guardar token en BD
        await self._repo.guardarResetToken(usuario.id, resetToken)

        # Construir URL de recuperación para Flutter
        # Flutter manejará esta URL mediante deep linking
        resetUrl = f"{settings.FRONTEND_URL}/reset-password?token={resetToken}"

        # Renderizar template HTML con Jinja2
        template = templateEnv.get_template("recuperarPassword.html")
        htmlContent = template.render(
            nombre=usuario.nombre,
            resetUrl=resetUrl,
        )

        # Enviar email
        mensaje = MessageSchema(
            subject="Recuperación de contraseña - ImpactoFit",
            recipients=[usuario.email],
            body=htmlContent,
            subtype=MessageType.html,
        )

        fm = FastMail(mailConfig)
        await fm.send_message(mensaje)

        return mensajeSeguro

    # ── Resetear contraseña ───────────────────────────────────────────────────

    async def resetearPassword(
        self,
        token: str,
        nuevaPassword: str,
    ) -> dict:
        """
        Valida el token y actualiza la contraseña del usuario.
        Invalida el token después de usarlo para que no pueda reutilizarse.
        """

        usuario = await self._repo.obtenerPorResetToken(token)

        if usuario is None:
            raise ValueError(
                "El enlace de recuperación es inválido o ya fue utilizado."
            )

        # Hashear la nueva contraseña
        nuevaPasswordHash = pwdContext.hash(nuevaPassword)

        # Actualizar contraseña e invalidar token en una secuencia atómica
        await self._repo.actualizarPassword(usuario.id, nuevaPasswordHash)
        await self._repo.invalidarResetToken(usuario.id)

        return {"mensaje": "Contraseña actualizada exitosamente"}

    # ── Verificar JWT ─────────────────────────────────────────────────────────

    def verificarToken(self, token: str) -> dict:
        """
        Decodifica y verifica un JWT.
        Usado por el middleware de autenticación en cada request protegido.

        Returns:
            Payload: { "sub": email, "rol": str, "usuarioId": int }

        Raises:
            ValueError: si el token es inválido o expiró.
        """
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM],
            )
            email: str = payload.get("sub")
            if email is None:
                raise ValueError("Token inválido")
            return payload

        except JWTError:
            raise ValueError("Token inválido o expirado")

    # ── Método auxiliar privado ───────────────────────────────────────────────

    def _generarJWT(
        self,
        email: str,
        rol: str,
        usuarioId: int,
    ) -> str:
        """
        Genera un JWT firmado con los datos del usuario.

        Payload:
            sub       → email (identificador estándar JWT)
            rol       → rol del usuario para autorización en controllers
            usuarioId → id para queries directas sin buscar por email
            exp       → fecha de expiración según ACCESS_TOKEN_EXPIRE_MINUTES
        """
        expiracion = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

        payload = {
            "sub":       email,
            "rol":       rol,
            "usuarioId": usuarioId,
            "exp":       expiracion,
        }

        return jwt.encode(
            payload,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM,
        )