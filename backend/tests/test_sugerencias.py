"""
Tests del endpoint de sugerencias.

Endpoints:
  - POST /api/v1/sugerencias
  - GET /api/v1/sugerencias
"""

import pytest
from httpx import AsyncClient


class TestEnviarSugerencia:
    """Suite para POST /api/v1/sugerencias."""

    URL = "/api/v1/sugerencias"

    @pytest.mark.asyncio
    async def test_enviar_sugerencia_sin_auth(self, async_client: AsyncClient):
        """POST /api/v1/sugerencias sin token -> 401."""
        payload = {
            "tipo": "nueva_palabra",
            "contenido": {"palabra": "Test", "significado": "Prueba"},
        }
        response = await async_client.post(self.URL, json=payload)

        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_enviar_sugerencia_con_auth(
        self, async_client: AsyncClient, auth_headers: dict
    ):
        """POST /api/v1/sugerencias con token valido -> 201."""
        payload = {
            "tipo": "nueva_palabra",
            "contenido": {"palabra": "Choro", "significado": "Persona astuta"},
        }
        response = await async_client.post(
            self.URL, json=payload, headers=auth_headers
        )

        assert response.status_code == 201
        data = response.json()
        assert data["tipo"] == "nueva_palabra"
        assert data["estado"] == "pendiente"
        assert "id" in data
        assert "fecha_creacion" in data

    @pytest.mark.asyncio
    async def test_enviar_sugerencia_correccion(
        self, async_client: AsyncClient, auth_headers: dict
    ):
        """POST /api/v1/sugerencias tipo correccion -> 201."""
        payload = {
            "tipo": "correccion",
            "contenido": {
                "referencia": "Weon",
                "correccion": "La traduccion deberia ser...",
            },
        }
        response = await async_client.post(
            self.URL, json=payload, headers=auth_headers
        )

        assert response.status_code == 201
        data = response.json()
        assert data["tipo"] == "correccion"
        assert data["estado"] == "pendiente"

    @pytest.mark.asyncio
    async def test_enviar_sugerencia_contenido_invalido(
        self, async_client: AsyncClient, auth_headers: dict
    ):
        """POST /api/v1/sugerencias con contenido no dict -> 422."""
        payload = {
            "tipo": "nueva_palabra",
            "contenido": "string_invalido_en_lugar_de_dict",
        }
        response = await async_client.post(
            self.URL, json=payload, headers=auth_headers
        )

        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_enviar_sugerencia_sin_contenido(
        self, async_client: AsyncClient, auth_headers: dict
    ):
        """POST /api/v1/sugerencias sin campo contenido -> 422."""
        payload = {"tipo": "nueva_palabra"}
        response = await async_client.post(
            self.URL, json=payload, headers=auth_headers
        )

        assert response.status_code == 422


class TestListarSugerencias:
    """Suite para GET /api/v1/sugerencias."""

    URL = "/api/v1/sugerencias"

    @pytest.mark.asyncio
    async def test_listar_sugerencias_sin_auth(self, async_client: AsyncClient):
        """GET /api/v1/sugerencias sin token -> 401."""
        response = await async_client.get(self.URL)

        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_listar_sugerencias_con_auth(
        self, async_client: AsyncClient, auth_headers: dict
    ):
        """GET /api/v1/sugerencias con token -> 200."""
        # Primero crear algunas sugerencias para que la lista no este vacia
        for i in range(3):
            payload = {
                "tipo": "nueva_palabra",
                "contenido": {"palabra": f"Test{i}", "significado": "Prueba"},
            }
            await async_client.post(self.URL, json=payload, headers=auth_headers)

        response = await async_client.get(self.URL, headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "paginacion" in data
        assert len(data["data"]) == 3
        for s in data["data"]:
            assert "id" in s
            assert "tipo" in s
            assert "estado" in s
            assert "contenido_resumen" in s

    @pytest.mark.asyncio
    async def test_listar_sugerencias_vacio(
        self, async_client: AsyncClient, auth_headers: dict
    ):
        """GET /api/v1/sugerencias sin datos -> 200 + lista vacia."""
        response = await async_client.get(self.URL, headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]) == 0
        assert data["paginacion"]["total_elementos"] == 0

    @pytest.mark.asyncio
    async def test_listar_sugerencias_paginacion(
        self, async_client: AsyncClient, auth_headers: dict
    ):
        """GET /api/v1/sugerencias con paginacion -> 200."""
        # Crear 5 sugerencias
        for i in range(5):
            payload = {
                "tipo": "nueva_palabra",
                "contenido": {"palabra": f"Test{i}", "significado": "Prueba"},
            }
            await async_client.post(self.URL, json=payload, headers=auth_headers)

        response = await async_client.get(
            self.URL, params={"pagina": 1, "tamanio": 2}, headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]) == 2
        assert data["paginacion"]["total_elementos"] == 5
        assert data["paginacion"]["total_paginas"] == 3
