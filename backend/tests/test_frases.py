"""
Tests del endpoint de frases.

Endpoints:
  - GET /api/v1/frases
  - GET /api/v1/frases/{id}
"""

import pytest
from httpx import AsyncClient


class TestListarFrases:
    """Suite para GET /api/v1/frases."""

    LIST_URL = "/api/v1/frases"

    @pytest.mark.asyncio
    async def test_listar_frases(
        self, async_client: AsyncClient, seed_test_data: dict
    ):
        """GET /api/v1/frases -> 200 + lista paginada."""
        response = await async_client.get(self.LIST_URL)

        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "paginacion" in data
        assert len(data["data"]) >= 3

    @pytest.mark.asyncio
    async def test_listar_frases_por_escenario(
        self, async_client: AsyncClient, seed_test_data: dict
    ):
        """GET /api/v1/frases?escenario_id=X -> 200 + filtrado."""
        escenario_id = seed_test_data["escenario_1"].id
        response = await async_client.get(
            self.LIST_URL, params={"escenario_id": escenario_id}
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]) > 0
        for frase in data["data"]:
            assert frase["escenario"] is not None
            assert frase["escenario"]["id"] == escenario_id

    @pytest.mark.asyncio
    async def test_listar_frases_por_tono(
        self, async_client: AsyncClient, seed_test_data: dict
    ):
        """GET /api/v1/frases?tono=informal -> 200 + filtrado por tono."""
        response = await async_client.get(
            self.LIST_URL, params={"tono": "informal"}
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]) > 0
        for frase in data["data"]:
            assert frase["tono"] == "informal"

    @pytest.mark.asyncio
    async def test_listar_frases_por_busqueda(
        self, async_client: AsyncClient, seed_test_data: dict
    ):
        """GET /api/v1/frases?buscar=cachai -> 200 + resultados ILIKE."""
        response = await async_client.get(
            self.LIST_URL, params={"buscar": "cachai"}
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]) > 0

    @pytest.mark.asyncio
    async def test_listar_frases_con_nivel_formalidad(
        self, async_client: AsyncClient, seed_test_data: dict
    ):
        """GET /api/v1/frases?nivel_formalidad_min=3 -> 200 + filtrado."""
        response = await async_client.get(
            self.LIST_URL, params={"nivel_formalidad_min": 3.0}
        )

        assert response.status_code == 200
        data = response.json()
        for frase in data["data"]:
            assert frase["nivel_formalidad"] >= 3.0

    @pytest.mark.asyncio
    async def test_listar_frases_sin_resultados(
        self, async_client: AsyncClient, seed_test_data: dict
    ):
        """GET /api/v1/frases?buscar=xxxxx -> 200 + lista vacia."""
        response = await async_client.get(
            self.LIST_URL, params={"buscar": "zzzzzznoexiste"}
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]) == 0
        assert data["paginacion"]["total_elementos"] == 0


class TestObtenerFrase:
    """Suite para GET /api/v1/frases/{id}."""

    @pytest.mark.asyncio
    async def test_obtener_frase_existente(
        self, async_client: AsyncClient, seed_test_data: dict
    ):
        """GET /api/v1/frases/{id} con ID existente -> 200 + detalle."""
        frase_id = seed_test_data["frase_1"].id
        response = await async_client.get(f"/api/v1/frases/{frase_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == frase_id
        assert data["frase_original"] == "¿Cachai weon?"
        assert data["tono"] == "informal"
        assert "traduccion" in data
        assert "significado_literal" in data
        assert "explicacion" in data
        assert "intencion_real" in data
        assert "nivel_formalidad" in data
        assert "nivel_ironia" in data
        assert "nivel_sarcasmo" in data
        assert "escenario" in data
        assert data["escenario"]["nombre"] == "En la calle"

    @pytest.mark.asyncio
    async def test_obtener_frase_inexistente(
        self, async_client: AsyncClient, seed_test_data: dict
    ):
        """GET /api/v1/frases/9999 -> 404."""
        response = await async_client.get("/api/v1/frases/9999")

        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_obtener_frase_id_invalido(
        self, async_client: AsyncClient, seed_test_data: dict
    ):
        """GET /api/v1/frases/abc -> 422."""
        response = await async_client.get("/api/v1/frases/abc")

        assert response.status_code == 422
