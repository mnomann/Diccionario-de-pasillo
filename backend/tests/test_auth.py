"""
Tests de autenticacion (registro y login).

Endpoints:
  - POST /api/v1/auth/registro
  - POST /api/v1/auth/login
"""

import pytest
from httpx import AsyncClient


class TestRegistro:
    """Suite de pruebas para el registro de usuarios."""

    REGISTRO_URL = "/api/v1/auth/registro"

    @pytest.mark.asyncio
    async def test_registro_exitoso(self, async_client: AsyncClient):
        """POST /api/v1/auth/registro con datos validos -> 201."""
        payload = {
            "nombre": "Nuevo Usuario",
            "email": "nuevo@example.com",
            "contrasena": "Password123!",
        }
        response = await async_client.post(self.REGISTRO_URL, json=payload)

        assert response.status_code == 201
        data = response.json()
        assert data["id"] is not None
        assert data["nombre"] == "Nuevo Usuario"
        assert data["email"] == "nuevo@example.com"
        assert "fecha_registro" in data
        # Asegurar que la contrasena no se devuelve
        assert "contrasena" not in data
        assert "contrasena_hash" not in data

    @pytest.mark.asyncio
    async def test_registro_email_duplicado(
        self, async_client: AsyncClient, test_user
    ):
        """POST /api/v1/auth/registro con email existente -> 409."""
        payload = {
            "nombre": "Otro Usuario",
            "email": "test@example.com",  # email del fixture test_user
            "contrasena": "Password123!",
        }
        response = await async_client.post(self.REGISTRO_URL, json=payload)

        assert response.status_code == 409
        data = response.json()
        assert "detail" in data or "detalle" in data

    @pytest.mark.asyncio
    async def test_registro_contrasena_corta(self, async_client: AsyncClient):
        """POST /api/v1/auth/registro con contrasena < 6 chars -> 422."""
        payload = {
            "nombre": "Usuario Invalido",
            "email": "invalido@example.com",
            "contrasena": "123",  # menos de 6 caracteres
        }
        response = await async_client.post(self.REGISTRO_URL, json=payload)

        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_registro_email_invalido(self, async_client: AsyncClient):
        """POST /api/v1/auth/registro con email mal formado -> 422."""
        payload = {
            "nombre": "Usuario Invalido",
            "email": "no-es-un-email",
            "contrasena": "Password123!",
        }
        response = await async_client.post(self.REGISTRO_URL, json=payload)

        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_registro_nombre_vacio(self, async_client: AsyncClient):
        """POST /api/v1/auth/registro con nombre vacio -> 422."""
        payload = {
            "nombre": "",
            "email": "vacio@example.com",
            "contrasena": "Password123!",
        }
        response = await async_client.post(self.REGISTRO_URL, json=payload)

        assert response.status_code == 422


class TestLogin:
    """Suite de pruebas para el inicio de sesion."""

    LOGIN_URL = "/api/v1/auth/login"

    @pytest.mark.asyncio
    async def test_login_exitoso(
        self, async_client: AsyncClient, test_user
    ):
        """POST /api/v1/auth/login con credenciales validas -> 200 + token."""
        payload = {
            "email": "test@example.com",
            "contrasena": "TestPass123!",
        }
        response = await async_client.post(self.LOGIN_URL, json=payload)

        assert response.status_code == 200
        data = response.json()
        assert "token" in data
        assert data["token_type"] == "bearer"
        assert "expira_en" in data
        assert data["expira_en"] > 0
        assert data["usuario"]["email"] == "test@example.com"
        assert data["usuario"]["nombre"] == "Usuario Test"

    @pytest.mark.asyncio
    async def test_login_credenciales_invalidas(self, async_client: AsyncClient):
        """POST /api/v1/auth/login con credenciales incorrectas -> 401."""
        payload = {
            "email": "noexiste@example.com",
            "contrasena": "WrongPassword!",
        }
        response = await async_client.post(self.LOGIN_URL, json=payload)

        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_login_contrasena_incorrecta(
        self, async_client: AsyncClient, test_user
    ):
        """POST /api/v1/auth/login con contrasena incorrecta -> 401."""
        payload = {
            "email": "test@example.com",
            "contrasena": "WrongPassword!",
        }
        response = await async_client.post(self.LOGIN_URL, json=payload)

        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_login_email_vacio(self, async_client: AsyncClient):
        """POST /api/v1/auth/login con email vacio -> 422."""
        payload = {
            "email": "",
            "contrasena": "TestPass123!",
        }
        response = await async_client.post(self.LOGIN_URL, json=payload)

        assert response.status_code == 422
