"""
IAuthService.py
---------------
Interfaz del servicio de autenticación.

Cubre los casos de uso del MVP relacionados con identidad:
    - Login con email y contraseña → retorna JWT
    - Logout manual
    - Solicitar recuperación de contraseña → envía email
    - Resetear contraseña con token
    - Verificar validez de un JWT
"""

from abc import ABC, abstractmethod


class IAuthService(ABC):

    @abstractmethod
    async def login(
        self,
        email: str,
        password: str
    ) -> dict:
        """
        Valida las credenciales y retorna el token JWT.

        Returns:
            {
                "accessToken": str,
                "tokenType": "bearer",
                "rol": str,
                "usuarioId": int,
                "nombre": str
            }

        Raises:
            ValueError: si el email no existe, la contraseña es incorrecta
                        o el usuario está inactivo.
        """
        pass

    @abstractmethod
    async def logout(self, token: str) -> dict:
        """
        Cierre de sesión manual.

        En una implementación stateless con JWT puro el logout
        se maneja en el cliente (descartando el token).
        Este método existe para el MVP y puede extenderse
        a una blacklist de tokens en fases posteriores.

        Returns:
            { "mensaje": "Sesión cerrada exitosamente" }
        """
        pass

    @abstractmethod
    async def solicitarRecuperacionPassword(self, email: str) -> dict:
        """
        Genera un token de recuperación y envía el email al usuario.

        Por seguridad retorna el mismo mensaje tanto si el email
        existe como si no, para no revelar qué usuarios están registrados.

        Returns:
            { "mensaje": "Si el email está registrado recibirás un correo" }
        """
        pass

    @abstractmethod
    async def resetearPassword(
        self,
        token: str,
        nuevaPassword: str
    ) -> dict:
        """
        Valida el token y actualiza la contraseña del usuario.

        Returns:
            { "mensaje": "Contraseña actualizada exitosamente" }

        Raises:
            ValueError: si el token no existe, es inválido o expiró.
        """
        pass

    @abstractmethod
    def verificarToken(self, token: str) -> dict:
        """
        Verifica y decodifica un JWT.

        Returns:
            El payload del token: { "sub": email, "rol": str, "usuarioId": int }

        Raises:
            ValueError: si el token es inválido o expiró.
        """
        pass