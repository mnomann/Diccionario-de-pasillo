"""
Tests del endpoint de usuarios.

Endpoints:
  - GET /api/v1/usuarios/me
"""

import pytest
from httpx import AsyncClient


class TestObtenerPerfil:
    """Suite para GET /api/v1/usuarios/me."""

    URL = "/api/v1/usuarios/me"

    @pytest.mark.asyncio
    async def test_obtener_perfil_sin_auth(self, async_client: AsyncClient):
        """GET /api/v1/usuarios/me sin token -> 401."""
        response = await async_client.get(self.URL)

        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_obtener_perfil_con_auth(
        self, async_client: AsyncClient, auth_headers: dict, test_user
    ):
        """GET /api/v1/usuarios/me con token valido -> 200 + datos."""
        response = await async_client.get(self.URL, headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_user.id
        assert data["nombre"] == "Usuario Test"
        assert data["email"] == "test@example.com"
        assert "fecha_registro" in data
        assert "preferencias" in data
        assert data["preferencias"] == {"tema": "claro"}
        assert "estadisticas" in data
        assert "total_sugerencias" in data["estadisticas"]
        assert data["estadisticas"]["total_sugerencias"] == 0

    @pytest.mark.asyncio
    async def test_obtener_perfil_con_sugerencias(
        self, async_client: AsyncClient, auth_headers: dict, test_user
    ):
        """Perfil con sugerencias existentes -> estadisticas actualizadas."""
        # Crear algunas sugerencias
        for i in range(2):
            payload = {
                "tipo": "nueva_palabra",
                "contenido": {"palabra": f"Test{i}"},
            }
            await async_client.post(
                "/api/v1/sugerencias", json=payload, headers=auth_headers
            )

        response = await async_client.get(self.URL, headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["estadisticas"]["total_sugerencias"] >= 2

    @pytest.mark.asyncio
    async def test_obtener_perfil_token_invalido(self, async_client: AsyncClient):
        """GET /api/v1/usuarios/me con token invalido -> 401."""
        headers = {"Authorization": "Bearer token_invalido_12345"}
        response = await async_client.get(self.URL, headers=headers)

        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_obtener_perfil_sin_header_auth(
        self, async_client: AsyncClient
    ):
        """GET /api/v1/usuarios/me sin header Authorization -> 401."""
        headers = {"Content-Type": "application/json"}
        response = await async_client.get(self.URL, headers=headers)

        assert response.status_code == 401
