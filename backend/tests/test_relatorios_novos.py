"""
Test suite for new Reports endpoints:
- GET /api/relatorios/manutencoes - Equipment and vehicles in maintenance
- GET /api/relatorios/alertas - Documents expiring in next 30 days
- GET /api/relatorios/utilizacao - Usage report with filters
"""
import pytest
import requests
import os

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', '').rstrip('/')

class TestRelatoriosNovos:
    """Test new report endpoints for Reports page improvements"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Get auth token before each test"""
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": "test@test.com",
            "password": "test123"
        })
        if response.status_code == 200:
            self.token = response.json().get("access_token")
            self.headers = {"Authorization": f"Bearer {self.token}"}
        else:
            pytest.skip("Authentication failed - skipping tests")
    
    # ==================== RELATÓRIO MANUTENÇÕES ====================
    
    def test_relatorio_manutencoes_returns_200(self):
        """GET /api/relatorios/manutencoes should return 200"""
        response = requests.get(f"{BASE_URL}/api/relatorios/manutencoes", headers=self.headers)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
    
    def test_relatorio_manutencoes_structure(self):
        """GET /api/relatorios/manutencoes should return correct structure"""
        response = requests.get(f"{BASE_URL}/api/relatorios/manutencoes", headers=self.headers)
        assert response.status_code == 200
        
        data = response.json()
        # Check required fields
        assert "equipamentos" in data, "Missing 'equipamentos' field"
        assert "viaturas" in data, "Missing 'viaturas' field"
        assert "estatisticas" in data, "Missing 'estatisticas' field"
        
        # Check statistics structure
        stats = data["estatisticas"]
        assert "total_equipamentos" in stats, "Missing 'total_equipamentos' in statistics"
        assert "total_viaturas" in stats, "Missing 'total_viaturas' in statistics"
        assert "total_geral" in stats, "Missing 'total_geral' in statistics"
        
        # Verify total_geral calculation
        assert stats["total_geral"] == stats["total_equipamentos"] + stats["total_viaturas"]
    
    def test_relatorio_manutencoes_filter_equipamento(self):
        """GET /api/relatorios/manutencoes?tipo_recurso=equipamento should filter only equipamentos"""
        response = requests.get(
            f"{BASE_URL}/api/relatorios/manutencoes?tipo_recurso=equipamento", 
            headers=self.headers
        )
        assert response.status_code == 200
        
        data = response.json()
        # When filtering by equipamento, viaturas should be empty
        assert data["viaturas"] == [], "Viaturas should be empty when filtering by equipamento"
    
    def test_relatorio_manutencoes_filter_viatura(self):
        """GET /api/relatorios/manutencoes?tipo_recurso=viatura should filter only viaturas"""
        response = requests.get(
            f"{BASE_URL}/api/relatorios/manutencoes?tipo_recurso=viatura", 
            headers=self.headers
        )
        assert response.status_code == 200
        
        data = response.json()
        # When filtering by viatura, equipamentos should be empty
        assert data["equipamentos"] == [], "Equipamentos should be empty when filtering by viatura"
    
    # ==================== RELATÓRIO ALERTAS ====================
    
    def test_relatorio_alertas_returns_200(self):
        """GET /api/relatorios/alertas should return 200"""
        response = requests.get(f"{BASE_URL}/api/relatorios/alertas", headers=self.headers)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
    
    def test_relatorio_alertas_structure(self):
        """GET /api/relatorios/alertas should return correct structure"""
        response = requests.get(f"{BASE_URL}/api/relatorios/alertas", headers=self.headers)
        assert response.status_code == 200
        
        data = response.json()
        # Check required fields
        assert "alertas" in data, "Missing 'alertas' field"
        assert "estatisticas" in data, "Missing 'estatisticas' field"
        
        # Check statistics structure
        stats = data["estatisticas"]
        assert "total_alertas" in stats, "Missing 'total_alertas' in statistics"
        assert "expirados" in stats, "Missing 'expirados' in statistics"
        assert "urgentes" in stats, "Missing 'urgentes' in statistics"
        assert "proximos" in stats, "Missing 'proximos' in statistics"
    
    def test_relatorio_alertas_with_dias_antecedencia(self):
        """GET /api/relatorios/alertas?dias_antecedencia=30 should work"""
        response = requests.get(
            f"{BASE_URL}/api/relatorios/alertas?dias_antecedencia=30", 
            headers=self.headers
        )
        assert response.status_code == 200
        
        data = response.json()
        assert "alertas" in data
        assert isinstance(data["alertas"], list)
    
    def test_relatorio_alertas_filter_viatura(self):
        """GET /api/relatorios/alertas?tipo_recurso=viatura should filter only viaturas"""
        response = requests.get(
            f"{BASE_URL}/api/relatorios/alertas?tipo_recurso=viatura", 
            headers=self.headers
        )
        assert response.status_code == 200
        
        data = response.json()
        # All alerts should be for viaturas
        for alerta in data["alertas"]:
            assert alerta.get("tipo_recurso") == "viatura", f"Expected viatura, got {alerta.get('tipo_recurso')}"
    
    def test_relatorio_alertas_alerta_structure(self):
        """Each alert should have required fields"""
        response = requests.get(f"{BASE_URL}/api/relatorios/alertas", headers=self.headers)
        assert response.status_code == 200
        
        data = response.json()
        if data["alertas"]:
            alerta = data["alertas"][0]
            # Check required fields in alert
            assert "tipo_recurso" in alerta, "Missing 'tipo_recurso' in alert"
            assert "recurso_id" in alerta, "Missing 'recurso_id' in alert"
            assert "identificador" in alerta, "Missing 'identificador' in alert"
            assert "tipo_alerta" in alerta, "Missing 'tipo_alerta' in alert"
            assert "urgente" in alerta, "Missing 'urgente' in alert"
            assert "expirado" in alerta, "Missing 'expirado' in alert"
    
    # ==================== RELATÓRIO UTILIZAÇÃO ====================
    
    def test_relatorio_utilizacao_returns_200(self):
        """GET /api/relatorios/utilizacao should return 200"""
        response = requests.get(f"{BASE_URL}/api/relatorios/utilizacao", headers=self.headers)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
    
    def test_relatorio_utilizacao_structure(self):
        """GET /api/relatorios/utilizacao should return correct structure"""
        response = requests.get(f"{BASE_URL}/api/relatorios/utilizacao", headers=self.headers)
        assert response.status_code == 200
        
        data = response.json()
        # Check required fields
        assert "equipamentos" in data, "Missing 'equipamentos' field"
        assert "viaturas" in data, "Missing 'viaturas' field"
        assert "estatisticas" in data, "Missing 'estatisticas' field"
        
        # Check statistics structure
        stats = data["estatisticas"]
        assert "equipamentos" in stats, "Missing 'equipamentos' in statistics"
        assert "viaturas" in stats, "Missing 'viaturas' in statistics"
        
        # Check equipamentos statistics
        eq_stats = stats["equipamentos"]
        assert "total" in eq_stats, "Missing 'total' in equipamentos statistics"
        assert "disponivel" in eq_stats, "Missing 'disponivel' in equipamentos statistics"
        assert "em_obra" in eq_stats, "Missing 'em_obra' in equipamentos statistics"
        assert "manutencao" in eq_stats, "Missing 'manutencao' in equipamentos statistics"
        
        # Check viaturas statistics
        vt_stats = stats["viaturas"]
        assert "total" in vt_stats, "Missing 'total' in viaturas statistics"
        assert "disponivel" in vt_stats, "Missing 'disponivel' in viaturas statistics"
        assert "em_obra" in vt_stats, "Missing 'em_obra' in viaturas statistics"
        assert "manutencao" in vt_stats, "Missing 'manutencao' in viaturas statistics"
    
    def test_relatorio_utilizacao_filter_tipo_equipamento(self):
        """GET /api/relatorios/utilizacao?tipo_recurso=equipamento should filter only equipamentos"""
        response = requests.get(
            f"{BASE_URL}/api/relatorios/utilizacao?tipo_recurso=equipamento", 
            headers=self.headers
        )
        assert response.status_code == 200
        
        data = response.json()
        # When filtering by equipamento, viaturas should be empty
        assert data["viaturas"] == [], "Viaturas should be empty when filtering by equipamento"
    
    def test_relatorio_utilizacao_filter_tipo_viatura(self):
        """GET /api/relatorios/utilizacao?tipo_recurso=viatura should filter only viaturas"""
        response = requests.get(
            f"{BASE_URL}/api/relatorios/utilizacao?tipo_recurso=viatura", 
            headers=self.headers
        )
        assert response.status_code == 200
        
        data = response.json()
        # When filtering by viatura, equipamentos should be empty
        assert data["equipamentos"] == [], "Equipamentos should be empty when filtering by viatura"
    
    def test_relatorio_utilizacao_filter_estado_disponivel(self):
        """GET /api/relatorios/utilizacao?estado=disponivel should filter by state"""
        response = requests.get(
            f"{BASE_URL}/api/relatorios/utilizacao?estado=disponivel", 
            headers=self.headers
        )
        assert response.status_code == 200
        
        data = response.json()
        # All resources should have estado_atual = disponivel
        for eq in data["equipamentos"]:
            assert eq.get("estado_atual") == "disponivel", f"Expected disponivel, got {eq.get('estado_atual')}"
        for vt in data["viaturas"]:
            assert vt.get("estado_atual") == "disponivel", f"Expected disponivel, got {vt.get('estado_atual')}"
    
    def test_relatorio_utilizacao_filter_estado_em_obra(self):
        """GET /api/relatorios/utilizacao?estado=em_obra should filter by state"""
        response = requests.get(
            f"{BASE_URL}/api/relatorios/utilizacao?estado=em_obra", 
            headers=self.headers
        )
        assert response.status_code == 200
        
        data = response.json()
        # All resources should have estado_atual = em_obra
        for eq in data["equipamentos"]:
            assert eq.get("estado_atual") == "em_obra", f"Expected em_obra, got {eq.get('estado_atual')}"
        for vt in data["viaturas"]:
            assert vt.get("estado_atual") == "em_obra", f"Expected em_obra, got {vt.get('estado_atual')}"
    
    def test_relatorio_utilizacao_filter_estado_manutencao(self):
        """GET /api/relatorios/utilizacao?estado=manutencao should filter by state"""
        response = requests.get(
            f"{BASE_URL}/api/relatorios/utilizacao?estado=manutencao", 
            headers=self.headers
        )
        assert response.status_code == 200
        
        data = response.json()
        # All resources should have estado_atual = manutencao
        for eq in data["equipamentos"]:
            assert eq.get("estado_atual") == "manutencao", f"Expected manutencao, got {eq.get('estado_atual')}"
        for vt in data["viaturas"]:
            assert vt.get("estado_atual") == "manutencao", f"Expected manutencao, got {vt.get('estado_atual')}"
    
    def test_relatorio_utilizacao_filter_date_range(self):
        """GET /api/relatorios/utilizacao with date range should work"""
        response = requests.get(
            f"{BASE_URL}/api/relatorios/utilizacao?data_inicio=2024-01-01&data_fim=2025-12-31", 
            headers=self.headers
        )
        assert response.status_code == 200
        
        data = response.json()
        assert "equipamentos" in data
        assert "viaturas" in data
    
    def test_relatorio_utilizacao_resource_has_movement_stats(self):
        """Each resource in utilizacao report should have movement statistics"""
        response = requests.get(f"{BASE_URL}/api/relatorios/utilizacao", headers=self.headers)
        assert response.status_code == 200
        
        data = response.json()
        
        # Check equipamentos have movement stats
        if data["equipamentos"]:
            eq = data["equipamentos"][0]
            assert "total_movimentos" in eq, "Missing 'total_movimentos' in equipamento"
            assert "total_saidas" in eq, "Missing 'total_saidas' in equipamento"
            assert "total_devolucoes" in eq, "Missing 'total_devolucoes' in equipamento"
            assert "estado_atual" in eq, "Missing 'estado_atual' in equipamento"
        
        # Check viaturas have movement stats
        if data["viaturas"]:
            vt = data["viaturas"][0]
            assert "total_movimentos" in vt, "Missing 'total_movimentos' in viatura"
            assert "total_saidas" in vt, "Missing 'total_saidas' in viatura"
            assert "total_devolucoes" in vt, "Missing 'total_devolucoes' in viatura"
            assert "estado_atual" in vt, "Missing 'estado_atual' in viatura"
    
    # ==================== EXISTING REPORTS (Regression) ====================
    
    def test_relatorio_movimentos_returns_200(self):
        """GET /api/relatorios/movimentos should still work (regression)"""
        response = requests.get(f"{BASE_URL}/api/relatorios/movimentos", headers=self.headers)
        assert response.status_code == 200
        
        data = response.json()
        assert "movimentos" in data
        assert "estatisticas" in data
    
    def test_relatorio_stock_returns_200(self):
        """GET /api/relatorios/stock should still work (regression)"""
        response = requests.get(f"{BASE_URL}/api/relatorios/stock", headers=self.headers)
        assert response.status_code == 200
        
        data = response.json()
        assert "movimentos" in data
        assert "estatisticas" in data
    
    # ==================== UNAUTHORIZED ACCESS ====================
    
    def test_relatorio_manutencoes_unauthorized(self):
        """GET /api/relatorios/manutencoes without auth should return 403"""
        response = requests.get(f"{BASE_URL}/api/relatorios/manutencoes")
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
    
    def test_relatorio_alertas_unauthorized(self):
        """GET /api/relatorios/alertas without auth should return 403"""
        response = requests.get(f"{BASE_URL}/api/relatorios/alertas")
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
    
    def test_relatorio_utilizacao_unauthorized(self):
        """GET /api/relatorios/utilizacao without auth should return 403"""
        response = requests.get(f"{BASE_URL}/api/relatorios/utilizacao")
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
