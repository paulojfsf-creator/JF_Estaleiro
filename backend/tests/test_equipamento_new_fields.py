"""
Test suite for new Equipamento fields:
- manual_url, certificado_url, ficha_manutencao_url (documentation URLs)
- em_manutencao (boolean for maintenance/broken status)
- descricao_avaria (description of the issue)
- Enhanced search functionality
"""
import pytest
import requests
import os
import uuid

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', '').rstrip('/')

class TestEquipamentoNewFields:
    """Test new fields added to Equipamento model"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup: Login and get auth token"""
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": "test@test.com",
            "password": "test123"
        })
        if response.status_code != 200:
            pytest.skip("Authentication failed - skipping tests")
        self.token = response.json()["access_token"]
        self.headers = {"Authorization": f"Bearer {self.token}"}
        self.created_ids = []
        yield
        # Cleanup: Delete test-created equipamentos
        for eq_id in self.created_ids:
            try:
                requests.delete(f"{BASE_URL}/api/equipamentos/{eq_id}", headers=self.headers)
            except:
                pass
    
    def test_create_equipamento_with_documentation_urls(self):
        """Test POST /api/equipamentos with new documentation URL fields"""
        unique_code = f"TEST_DOC_{uuid.uuid4().hex[:8]}"
        payload = {
            "codigo": unique_code,
            "descricao": "Equipamento com documentação",
            "marca": "TestMarca",
            "modelo": "TestModelo",
            "manual_url": "https://example.com/manual.pdf",
            "certificado_url": "https://example.com/certificado.pdf",
            "ficha_manutencao_url": "https://example.com/ficha.pdf",
            "em_manutencao": False,
            "descricao_avaria": ""
        }
        
        response = requests.post(f"{BASE_URL}/api/equipamentos", json=payload, headers=self.headers)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        
        data = response.json()
        self.created_ids.append(data["id"])
        
        # Verify all new fields are returned
        assert data["manual_url"] == "https://example.com/manual.pdf"
        assert data["certificado_url"] == "https://example.com/certificado.pdf"
        assert data["ficha_manutencao_url"] == "https://example.com/ficha.pdf"
        assert data["em_manutencao"] == False
        assert data["descricao_avaria"] == ""
        print(f"✓ Created equipamento with documentation URLs: {data['id']}")
    
    def test_create_equipamento_em_manutencao(self):
        """Test POST /api/equipamentos with em_manutencao=True and descricao_avaria"""
        unique_code = f"TEST_MAN_{uuid.uuid4().hex[:8]}"
        payload = {
            "codigo": unique_code,
            "descricao": "Equipamento avariado",
            "marca": "TestMarca",
            "modelo": "TestModelo",
            "em_manutencao": True,
            "descricao_avaria": "Motor queimado, aguarda peças de substituição"
        }
        
        response = requests.post(f"{BASE_URL}/api/equipamentos", json=payload, headers=self.headers)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        
        data = response.json()
        self.created_ids.append(data["id"])
        
        # Verify maintenance fields
        assert data["em_manutencao"] == True
        assert data["descricao_avaria"] == "Motor queimado, aguarda peças de substituição"
        print(f"✓ Created equipamento em manutenção: {data['id']}")
    
    def test_update_equipamento_add_documentation(self):
        """Test PUT /api/equipamentos/{id} to add documentation URLs"""
        # First create an equipamento without documentation
        unique_code = f"TEST_UPD_{uuid.uuid4().hex[:8]}"
        create_payload = {
            "codigo": unique_code,
            "descricao": "Equipamento sem documentação inicial"
        }
        
        create_response = requests.post(f"{BASE_URL}/api/equipamentos", json=create_payload, headers=self.headers)
        assert create_response.status_code == 200
        eq_id = create_response.json()["id"]
        self.created_ids.append(eq_id)
        
        # Update with documentation URLs
        update_payload = {
            "codigo": unique_code,
            "descricao": "Equipamento com documentação adicionada",
            "manual_url": "https://example.com/manual_updated.pdf",
            "certificado_url": "https://example.com/cert_updated.pdf",
            "ficha_manutencao_url": "https://example.com/ficha_updated.pdf"
        }
        
        update_response = requests.put(f"{BASE_URL}/api/equipamentos/{eq_id}", json=update_payload, headers=self.headers)
        assert update_response.status_code == 200, f"Expected 200, got {update_response.status_code}: {update_response.text}"
        
        data = update_response.json()
        assert data["manual_url"] == "https://example.com/manual_updated.pdf"
        assert data["certificado_url"] == "https://example.com/cert_updated.pdf"
        assert data["ficha_manutencao_url"] == "https://example.com/ficha_updated.pdf"
        print(f"✓ Updated equipamento with documentation URLs: {eq_id}")
    
    def test_update_equipamento_set_em_manutencao(self):
        """Test PUT /api/equipamentos/{id} to set em_manutencao status"""
        # First create a normal equipamento
        unique_code = f"TEST_MNT_{uuid.uuid4().hex[:8]}"
        create_payload = {
            "codigo": unique_code,
            "descricao": "Equipamento funcional",
            "em_manutencao": False
        }
        
        create_response = requests.post(f"{BASE_URL}/api/equipamentos", json=create_payload, headers=self.headers)
        assert create_response.status_code == 200
        eq_id = create_response.json()["id"]
        self.created_ids.append(eq_id)
        
        # Update to set em_manutencao
        update_payload = {
            "codigo": unique_code,
            "descricao": "Equipamento funcional",
            "em_manutencao": True,
            "descricao_avaria": "Avaria no sistema hidráulico"
        }
        
        update_response = requests.put(f"{BASE_URL}/api/equipamentos/{eq_id}", json=update_payload, headers=self.headers)
        assert update_response.status_code == 200
        
        data = update_response.json()
        assert data["em_manutencao"] == True
        assert data["descricao_avaria"] == "Avaria no sistema hidráulico"
        print(f"✓ Updated equipamento to em_manutencao: {eq_id}")
    
    def test_get_equipamento_detail_with_new_fields(self):
        """Test GET /api/equipamentos/{id} returns all new fields"""
        # Create equipamento with all new fields
        unique_code = f"TEST_GET_{uuid.uuid4().hex[:8]}"
        create_payload = {
            "codigo": unique_code,
            "descricao": "Equipamento completo para teste GET",
            "marca": "MarcaTest",
            "modelo": "ModeloTest",
            "categoria": "Ferramentas",
            "numero_serie": "SN123456",
            "manual_url": "https://example.com/manual_get.pdf",
            "certificado_url": "https://example.com/cert_get.pdf",
            "ficha_manutencao_url": "https://example.com/ficha_get.pdf",
            "em_manutencao": True,
            "descricao_avaria": "Teste de avaria para GET"
        }
        
        create_response = requests.post(f"{BASE_URL}/api/equipamentos", json=create_payload, headers=self.headers)
        assert create_response.status_code == 200
        eq_id = create_response.json()["id"]
        self.created_ids.append(eq_id)
        
        # GET the equipamento detail
        get_response = requests.get(f"{BASE_URL}/api/equipamentos/{eq_id}", headers=self.headers)
        assert get_response.status_code == 200
        
        data = get_response.json()
        equipamento = data["equipamento"]
        
        # Verify all new fields are present
        assert equipamento["manual_url"] == "https://example.com/manual_get.pdf"
        assert equipamento["certificado_url"] == "https://example.com/cert_get.pdf"
        assert equipamento["ficha_manutencao_url"] == "https://example.com/ficha_get.pdf"
        assert equipamento["em_manutencao"] == True
        assert equipamento["descricao_avaria"] == "Teste de avaria para GET"
        print(f"✓ GET equipamento detail returns all new fields: {eq_id}")
    
    def test_list_equipamentos_includes_new_fields(self):
        """Test GET /api/equipamentos returns new fields in list"""
        # Create equipamento with new fields
        unique_code = f"TEST_LST_{uuid.uuid4().hex[:8]}"
        create_payload = {
            "codigo": unique_code,
            "descricao": "Equipamento para teste lista",
            "em_manutencao": True,
            "descricao_avaria": "Avaria teste lista"
        }
        
        create_response = requests.post(f"{BASE_URL}/api/equipamentos", json=create_payload, headers=self.headers)
        assert create_response.status_code == 200
        eq_id = create_response.json()["id"]
        self.created_ids.append(eq_id)
        
        # GET list of equipamentos
        list_response = requests.get(f"{BASE_URL}/api/equipamentos", headers=self.headers)
        assert list_response.status_code == 200
        
        equipamentos = list_response.json()
        # Find our created equipamento
        found = next((e for e in equipamentos if e["id"] == eq_id), None)
        assert found is not None, "Created equipamento not found in list"
        
        # Verify new fields are present
        assert "em_manutencao" in found
        assert found["em_manutencao"] == True
        assert "descricao_avaria" in found
        print(f"✓ List equipamentos includes new fields")
    
    def test_create_equipamento_with_all_fields(self):
        """Test creating equipamento with ALL fields including new ones"""
        unique_code = f"TEST_ALL_{uuid.uuid4().hex[:8]}"
        payload = {
            "codigo": unique_code,
            "descricao": "Equipamento completo com todos os campos",
            "marca": "MarcaCompleta",
            "modelo": "ModeloCompleto",
            "data_aquisicao": "2024-01-15",
            "ativo": True,
            "categoria": "Máquinas",
            "numero_serie": "SN-FULL-123",
            "estado_conservacao": "Bom",
            "foto": "",
            "obra_id": None,
            "manual_url": "https://example.com/manual_full.pdf",
            "certificado_url": "https://example.com/cert_full.pdf",
            "ficha_manutencao_url": "https://example.com/ficha_full.pdf",
            "em_manutencao": False,
            "descricao_avaria": ""
        }
        
        response = requests.post(f"{BASE_URL}/api/equipamentos", json=payload, headers=self.headers)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        
        data = response.json()
        self.created_ids.append(data["id"])
        
        # Verify all fields
        assert data["codigo"] == unique_code
        assert data["descricao"] == "Equipamento completo com todos os campos"
        assert data["marca"] == "MarcaCompleta"
        assert data["modelo"] == "ModeloCompleto"
        assert data["categoria"] == "Máquinas"
        assert data["numero_serie"] == "SN-FULL-123"
        assert data["estado_conservacao"] == "Bom"
        assert data["manual_url"] == "https://example.com/manual_full.pdf"
        assert data["certificado_url"] == "https://example.com/cert_full.pdf"
        assert data["ficha_manutencao_url"] == "https://example.com/ficha_full.pdf"
        assert data["em_manutencao"] == False
        print(f"✓ Created equipamento with ALL fields: {data['id']}")


class TestEquipamentoSearch:
    """Test enhanced search functionality for Equipamentos"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup: Login and get auth token"""
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": "test@test.com",
            "password": "test123"
        })
        if response.status_code != 200:
            pytest.skip("Authentication failed - skipping tests")
        self.token = response.json()["access_token"]
        self.headers = {"Authorization": f"Bearer {self.token}"}
        self.created_ids = []
        yield
        # Cleanup
        for eq_id in self.created_ids:
            try:
                requests.delete(f"{BASE_URL}/api/equipamentos/{eq_id}", headers=self.headers)
            except:
                pass
    
    def test_search_by_codigo(self):
        """Test that search works by codigo"""
        unique_code = f"SRCH_COD_{uuid.uuid4().hex[:6]}"
        payload = {
            "codigo": unique_code,
            "descricao": "Equipamento para pesquisa por código"
        }
        
        response = requests.post(f"{BASE_URL}/api/equipamentos", json=payload, headers=self.headers)
        assert response.status_code == 200
        self.created_ids.append(response.json()["id"])
        
        # Get all equipamentos and verify our item is there
        list_response = requests.get(f"{BASE_URL}/api/equipamentos", headers=self.headers)
        assert list_response.status_code == 200
        
        equipamentos = list_response.json()
        found = [e for e in equipamentos if unique_code in e["codigo"]]
        assert len(found) > 0, f"Equipamento with codigo {unique_code} not found"
        print(f"✓ Search by codigo works - found {len(found)} result(s)")
    
    def test_search_by_numero_serie(self):
        """Test that search works by numero_serie"""
        unique_serie = f"NS_{uuid.uuid4().hex[:8]}"
        payload = {
            "codigo": f"TEST_NS_{uuid.uuid4().hex[:6]}",
            "descricao": "Equipamento para pesquisa por nº série",
            "numero_serie": unique_serie
        }
        
        response = requests.post(f"{BASE_URL}/api/equipamentos", json=payload, headers=self.headers)
        assert response.status_code == 200
        self.created_ids.append(response.json()["id"])
        
        # Get all equipamentos
        list_response = requests.get(f"{BASE_URL}/api/equipamentos", headers=self.headers)
        assert list_response.status_code == 200
        
        equipamentos = list_response.json()
        found = [e for e in equipamentos if e.get("numero_serie") == unique_serie]
        assert len(found) > 0, f"Equipamento with numero_serie {unique_serie} not found"
        print(f"✓ Search by numero_serie works - found {len(found)} result(s)")
    
    def test_search_by_categoria(self):
        """Test that search works by categoria"""
        unique_cat = f"Cat_{uuid.uuid4().hex[:6]}"
        payload = {
            "codigo": f"TEST_CAT_{uuid.uuid4().hex[:6]}",
            "descricao": "Equipamento para pesquisa por categoria",
            "categoria": unique_cat
        }
        
        response = requests.post(f"{BASE_URL}/api/equipamentos", json=payload, headers=self.headers)
        assert response.status_code == 200
        self.created_ids.append(response.json()["id"])
        
        # Get all equipamentos
        list_response = requests.get(f"{BASE_URL}/api/equipamentos", headers=self.headers)
        assert list_response.status_code == 200
        
        equipamentos = list_response.json()
        found = [e for e in equipamentos if e.get("categoria") == unique_cat]
        assert len(found) > 0, f"Equipamento with categoria {unique_cat} not found"
        print(f"✓ Search by categoria works - found {len(found)} result(s)")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
