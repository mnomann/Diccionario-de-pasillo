"""
Tests del endpoint de palabras.

Endpoints:
  - GET /api/v1/palabras
  - GET /api/v1/palabras/{id}
"""

import pytest
from httpx import AsyncClient


class TestListarPalabras:
    """Suite para GET /api/v1/palabras."""

    LIST_URL = "/api/v1/palabras"

    @pytest.mark.asyncio
    async def test_listar_palabras(
        self, async_client: AsyncClient, seed_test_data: dict
    ):
        """GET /api/v1/palabras -> 200 + lista paginada."""
        response = await async_client.get(self.LIST_URL)

        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "paginacion" in data
        assert len(data["data"]) >= 3
        assert data["paginacion"]["pagina"] == 1
        assert data["paginacion"]["total_elementos"] >= 3

    @pytest.mark.asyncio
    async def test_listar_palabras_con_filtro_categoria(
        self, async_client: AsyncClient, seed_test_data: dict
    ):
        """GET /api/v1/palabras?categoria=jerga -> 200 + filtrado."""
        response = await async_client.get(self.LIST_URL, params={"categoria": "jerga"})

        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]) > 0
        for palabra in data["data"]:
            assert palabra["categoria"] == "jerga"

    @pytest.mark.asyncio
    async def test_listar_palabras_con_busqueda(
        self, async_client: AsyncClient, seed_test_data: dict
    ):
        """GET /api/v1/palabras?buscar=weon -> 200 + resultados ILIKE."""
        response = await async_client.get(self.LIST_URL, params={"buscar": "weon"})

        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]) > 0
        # Verificar que al menos un resultado contiene el termino buscado
        palabras_encontradas = [p["palabra"].lower() for p in data["data"]]
        assert any("weon" in p for p in palabras_encontradas)

    @pytest.mark.asyncio
    async def test_listar_palabras_sin_resultados(
        self, async_client: AsyncClient, seed_test_data: dict
    ):
        """GET /api/v1/palabras?buscar=xxxxx -> 200 + lista vacia."""
        response = await async_client.get(
            self.LIST_URL, params={"buscar": "zzzzzznoexiste"}
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]) == 0
        assert data["paginacion"]["total_elementos"] == 0

    @pytest.mark.asyncio
    async def test_listar_palabras_paginacion(
        self, async_client: AsyncClient, seed_test_data: dict
    ):
        """GET /api/v1/palabras?pagina=1&tamanio=2 -> 200 + paginacion correcta."""
        response = await async_client.get(
            self.LIST_URL, params={"pagina": 1, "tamanio": 2}
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]) <= 2
        assert data["paginacion"]["tamanio"] == 2


class TestObtenerPalabra:
    """Suite para GET /api/v1/palabras/{id}."""

    @pytest.mark.asyncio
    async def test_obtener_palabra_existente(
        self, async_client: AsyncClient, seed_test_data: dict
    ):
        """GET /api/v1/palabras/{id} con ID existente -> 200 + detalle."""
        palabra_id = seed_test_data["palabra_1"].id
        response = await async_client.get(f"/api/v1/palabras/{palabra_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == palabra_id
        assert data["palabra"] == "Weon"
        assert data["categoria"] == "modismo"
        assert "traduccion" in data
        assert "nivel_formalidad" in data
        assert "nivel_ironia" in data
        assert "nivel_sarcasmo" in data
        assert "fecha_creacion" in data

    @pytest.mark.asyncio
    async def test_obtener_palabra_inexistente(
        self, async_client: AsyncClient, seed_test_data: dict
    ):
        """GET /api/v1/palabras/9999 -> 404."""
        response = await async_client.get("/api/v1/palabras/9999")

        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_obtener_palabra_id_invalido(
        self, async_client: AsyncClient, seed_test_data: dict
    ):
        """GET /api/v1/palabras/abc -> 422."""
        response = await async_client.get("/api/v1/palabras/abc")

        assert response.status_code == 422
