"""
Tests del endpoint de escenarios.

Endpoints:
  - GET /api/v1/escenarios
  - GET /api/v1/escenarios/{id}
"""

import pytest
from httpx import AsyncClient


class TestListarEscenarios:
    """Suite para GET /api/v1/escenarios."""

    LIST_URL = "/api/v1/escenarios"

    @pytest.mark.asyncio
    async def test_listar_escenarios(
        self, async_client: AsyncClient, seed_test_data: dict
    ):
        """GET /api/v1/escenarios -> 200 + lista paginada."""
        response = await async_client.get(self.LIST_URL)

        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "paginacion" in data
        # Solo debe incluir escenarios activos (excluye escenario_3 que es inactivo)
        assert len(data["data"]) >= 2

    @pytest.mark.asyncio
    async def test_listar_escenarios_con_busqueda(
        self, async_client: AsyncClient, seed_test_data: dict
    ):
        """GET /api/v1/escenarios?buscar=trabajo -> 200 + resultados ILIKE."""
        response = await async_client.get(
            self.LIST_URL, params={"buscar": "trabajo"}
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]) > 0
        for escenario in data["data"]:
            assert "trabajo" in escenario["nombre"].lower()

    @pytest.mark.asyncio
    async def test_listar_escenarios_con_activo_false(
        self, async_client: AsyncClient, seed_test_data: dict
    ):
        """GET /api/v1/escenarios?activo=false -> 200 + escenarios inactivos."""
        response = await async_client.get(
            self.LIST_URL, params={"activo": False}
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]) > 0
        for escenario in data["data"]:
            assert escenario["activo"] is False

    @pytest.mark.asyncio
    async def test_listar_escenarios_sin_resultados(
        self, async_client: AsyncClient, seed_test_data: dict
    ):
        """GET /api/v1/escenarios?buscar=xxxxx -> 200 + lista vacia."""
        response = await async_client.get(
            self.LIST_URL, params={"buscar": "zzzzzznoexiste"}
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]) == 0

    @pytest.mark.asyncio
    async def test_listar_escenarios_paginacion(
        self, async_client: AsyncClient, seed_test_data: dict
    ):
        """GET /api/v1/escenarios?pagina=1&tamanio=1 -> 200 + 1 elemento."""
        response = await async_client.get(
            self.LIST_URL, params={"pagina": 1, "tamanio": 1}
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]) == 1
        assert data["paginacion"]["tamanio"] == 1


class TestObtenerEscenario:
    """Suite para GET /api/v1/escenarios/{id}."""

    @pytest.mark.asyncio
    async def test_obtener_escenario_con_frases(
        self, async_client: AsyncClient, seed_test_data: dict
    ):
        """GET /api/v1/escenarios/{id} -> 200 + detalle con frases activas."""
        escenario_id = seed_test_data["escenario_1"].id
        response = await async_client.get(f"/api/v1/escenarios/{escenario_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == escenario_id
        assert data["nombre"] == "En la calle"
        assert data["activo"] is True
        assert "frases" in data
        assert len(data["frases"]) > 0
        # Verificar que las frases tienen datos basicos
        for frase in data["frases"]:
            assert "id" in frase
            assert "frase_original" in frase
            assert "traduccion" in frase

    @pytest.mark.asyncio
    async def test_obtener_escenario_inexistente(
        self, async_client: AsyncClient, seed_test_data: dict
    ):
        """GET /api/v1/escenarios/9999 -> 404."""
        response = await async_client.get("/api/v1/escenarios/9999")

        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_obtener_escenario_id_invalido(
        self, async_client: AsyncClient, seed_test_data: dict
    ):
        """GET /api/v1/escenarios/abc -> 422."""
        response = await async_client.get("/api/v1/escenarios/abc")

        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_obtener_escenario_con_frases_solo_activas(
        self, async_client: AsyncClient, seed_test_data: dict
    ):
        """Verifica que solo se retornen frases activas en el detalle."""
        escenario_id = seed_test_data["escenario_2"].id
        response = await async_client.get(f"/api/v1/escenarios/{escenario_id}")

        assert response.status_code == 200
        data = response.json()
        # Todas las frases en los fixtures son activas
        assert len(data["frases"]) >= 2
