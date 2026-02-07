"""
Comprehensive API tests for José Firmino Warehouse Management System
Tests: Authentication, Equipamentos, Viaturas, Materiais, Obras, Movimentos, Export/Import
"""
import pytest
import requests
import os
import uuid

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://constructpm-1.preview.emergentagent.com')

# Test credentials
TEST_EMAIL = "test@test.com"
TEST_PASSWORD = "test123"
TEST_NAME = "Test User"

class TestAuthentication:
    """Authentication endpoint tests"""
    
    def test_api_root(self):
        """Test API root endpoint"""
        response = requests.get(f"{BASE_URL}/api/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "José Firmino" in data["message"]
        print("✓ API root endpoint working")
    
    def test_login_success(self):
        """Test login with valid credentials"""
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD
        })
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "user" in data
        assert data["user"]["email"] == TEST_EMAIL
        print(f"✓ Login successful for {TEST_EMAIL}")
        return data["access_token"]
    
    def test_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": "wrong@example.com",
            "password": "wrongpass"
        })
        assert response.status_code == 401
        print("✓ Invalid credentials correctly rejected")
    
    def test_get_current_user(self, auth_token):
        """Test getting current user info"""
        response = requests.get(f"{BASE_URL}/api/auth/me", headers={
            "Authorization": f"Bearer {auth_token}"
        })
        assert response.status_code == 200
        data = response.json()
        assert "email" in data
        assert "name" in data
        print(f"✓ Current user retrieved: {data['name']}")


class TestEquipamentos:
    """Equipamentos CRUD tests"""
    
    def test_list_equipamentos(self, auth_token):
        """Test listing all equipamentos"""
        response = requests.get(f"{BASE_URL}/api/equipamentos", headers={
            "Authorization": f"Bearer {auth_token}"
        })
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        print(f"✓ Listed {len(data)} equipamentos")
    
    def test_create_equipamento(self, auth_token):
        """Test creating a new equipamento"""
        unique_code = f"TEST_EQ_{uuid.uuid4().hex[:6].upper()}"
        payload = {
            "codigo": unique_code,
            "descricao": "Test Equipment",
            "marca": "TestBrand",
            "modelo": "TestModel",
            "categoria": "Ferramentas",
            "estado_conservacao": "Bom",
            "ativo": True
        }
        response = requests.post(f"{BASE_URL}/api/equipamentos", json=payload, headers={
            "Authorization": f"Bearer {auth_token}"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["codigo"] == unique_code
        assert data["descricao"] == "Test Equipment"
        assert "id" in data
        print(f"✓ Created equipamento: {unique_code}")
        return data["id"]
    
    def test_get_equipamento_detail(self, auth_token, created_equipamento_id):
        """Test getting equipamento detail with history"""
        response = requests.get(f"{BASE_URL}/api/equipamentos/{created_equipamento_id}", headers={
            "Authorization": f"Bearer {auth_token}"
        })
        assert response.status_code == 200
        data = response.json()
        assert "equipamento" in data
        assert "historico" in data
        print(f"✓ Retrieved equipamento detail with history")
    
    def test_update_equipamento(self, auth_token, created_equipamento_id):
        """Test updating an equipamento"""
        payload = {
            "codigo": f"TEST_EQ_{uuid.uuid4().hex[:6].upper()}",
            "descricao": "Updated Equipment",
            "marca": "UpdatedBrand",
            "modelo": "UpdatedModel",
            "estado_conservacao": "Razoável",
            "ativo": True
        }
        response = requests.put(f"{BASE_URL}/api/equipamentos/{created_equipamento_id}", json=payload, headers={
            "Authorization": f"Bearer {auth_token}"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["descricao"] == "Updated Equipment"
        print(f"✓ Updated equipamento")
    
    def test_delete_equipamento(self, auth_token, created_equipamento_id):
        """Test deleting an equipamento"""
        response = requests.delete(f"{BASE_URL}/api/equipamentos/{created_equipamento_id}", headers={
            "Authorization": f"Bearer {auth_token}"
        })
        assert response.status_code == 200
        print(f"✓ Deleted equipamento")


class TestViaturas:
    """Viaturas CRUD tests"""
    
    def test_list_viaturas(self, auth_token):
        """Test listing all viaturas"""
        response = requests.get(f"{BASE_URL}/api/viaturas", headers={
            "Authorization": f"Bearer {auth_token}"
        })
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        print(f"✓ Listed {len(data)} viaturas")
    
    def test_create_viatura(self, auth_token):
        """Test creating a new viatura"""
        unique_matricula = f"TEST-{uuid.uuid4().hex[:4].upper()}"
        payload = {
            "matricula": unique_matricula,
            "marca": "TestMarca",
            "modelo": "TestModelo",
            "combustivel": "Gasoleo",
            "ativa": True
        }
        response = requests.post(f"{BASE_URL}/api/viaturas", json=payload, headers={
            "Authorization": f"Bearer {auth_token}"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["matricula"] == unique_matricula
        assert "id" in data
        print(f"✓ Created viatura: {unique_matricula}")
        return data["id"]
    
    def test_get_viatura_detail(self, auth_token, created_viatura_id):
        """Test getting viatura detail with history and km history"""
        response = requests.get(f"{BASE_URL}/api/viaturas/{created_viatura_id}", headers={
            "Authorization": f"Bearer {auth_token}"
        })
        assert response.status_code == 200
        data = response.json()
        assert "viatura" in data
        assert "historico" in data
        assert "km_historico" in data
        print(f"✓ Retrieved viatura detail with history")
    
    def test_delete_viatura(self, auth_token, created_viatura_id):
        """Test deleting a viatura"""
        response = requests.delete(f"{BASE_URL}/api/viaturas/{created_viatura_id}", headers={
            "Authorization": f"Bearer {auth_token}"
        })
        assert response.status_code == 200
        print(f"✓ Deleted viatura")


class TestMateriais:
    """Materiais CRUD tests"""
    
    def test_list_materiais(self, auth_token):
        """Test listing all materiais"""
        response = requests.get(f"{BASE_URL}/api/materiais", headers={
            "Authorization": f"Bearer {auth_token}"
        })
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        print(f"✓ Listed {len(data)} materiais")
    
    def test_create_material(self, auth_token):
        """Test creating a new material"""
        unique_code = f"TEST_MAT_{uuid.uuid4().hex[:6].upper()}"
        payload = {
            "codigo": unique_code,
            "descricao": "Test Material",
            "unidade": "kg",
            "stock_atual": 100,
            "stock_minimo": 10,
            "ativo": True
        }
        response = requests.post(f"{BASE_URL}/api/materiais", json=payload, headers={
            "Authorization": f"Bearer {auth_token}"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["codigo"] == unique_code
        assert data["stock_atual"] == 100
        print(f"✓ Created material: {unique_code}")
        return data["id"]
    
    def test_delete_material(self, auth_token, created_material_id):
        """Test deleting a material"""
        response = requests.delete(f"{BASE_URL}/api/materiais/{created_material_id}", headers={
            "Authorization": f"Bearer {auth_token}"
        })
        assert response.status_code == 200
        print(f"✓ Deleted material")


class TestObras:
    """Obras CRUD tests"""
    
    def test_list_obras(self, auth_token):
        """Test listing all obras"""
        response = requests.get(f"{BASE_URL}/api/obras", headers={
            "Authorization": f"Bearer {auth_token}"
        })
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        print(f"✓ Listed {len(data)} obras")
    
    def test_create_obra(self, auth_token):
        """Test creating a new obra"""
        unique_code = f"TEST_OBR_{uuid.uuid4().hex[:6].upper()}"
        payload = {
            "codigo": unique_code,
            "nome": "Test Obra",
            "endereco": "Test Address",
            "cliente": "Test Client",
            "estado": "Ativa"
        }
        response = requests.post(f"{BASE_URL}/api/obras", json=payload, headers={
            "Authorization": f"Bearer {auth_token}"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["codigo"] == unique_code
        assert data["nome"] == "Test Obra"
        print(f"✓ Created obra: {unique_code}")
        return data["id"]
    
    def test_get_obra_detail(self, auth_token, created_obra_id):
        """Test getting obra detail with assigned equipamentos and viaturas"""
        response = requests.get(f"{BASE_URL}/api/obras/{created_obra_id}", headers={
            "Authorization": f"Bearer {auth_token}"
        })
        assert response.status_code == 200
        data = response.json()
        assert "obra" in data
        assert "equipamentos" in data
        assert "viaturas" in data
        print(f"✓ Retrieved obra detail with assigned resources")
    
    def test_delete_obra(self, auth_token, created_obra_id):
        """Test deleting an obra"""
        response = requests.delete(f"{BASE_URL}/api/obras/{created_obra_id}", headers={
            "Authorization": f"Bearer {auth_token}"
        })
        assert response.status_code == 200
        print(f"✓ Deleted obra")


class TestMovimentos:
    """Movimentos tests - Asset assignment, Stock movements, Vehicle KM"""
    
    def test_list_movimentos(self, auth_token):
        """Test listing all asset movements"""
        response = requests.get(f"{BASE_URL}/api/movimentos", headers={
            "Authorization": f"Bearer {auth_token}"
        })
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        print(f"✓ Listed {len(data)} asset movements")
    
    def test_list_stock_movimentos(self, auth_token):
        """Test listing all stock movements"""
        response = requests.get(f"{BASE_URL}/api/movimentos/stock", headers={
            "Authorization": f"Bearer {auth_token}"
        })
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        print(f"✓ Listed {len(data)} stock movements")
    
    def test_list_viatura_movimentos(self, auth_token):
        """Test listing all viatura KM movements"""
        response = requests.get(f"{BASE_URL}/api/movimentos/viaturas", headers={
            "Authorization": f"Bearer {auth_token}"
        })
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        print(f"✓ Listed {len(data)} viatura KM movements")


class TestDashboardAndAlerts:
    """Dashboard summary and alerts tests"""
    
    def test_get_summary(self, auth_token):
        """Test getting dashboard summary"""
        response = requests.get(f"{BASE_URL}/api/summary", headers={
            "Authorization": f"Bearer {auth_token}"
        })
        assert response.status_code == 200
        data = response.json()
        assert "equipamentos" in data
        assert "viaturas" in data
        assert "materiais" in data
        assert "obras" in data
        assert "alerts" in data
        print(f"✓ Dashboard summary retrieved - Equipamentos: {data['equipamentos']['total']}, Viaturas: {data['viaturas']['total']}, Materiais: {data['materiais']['total']}, Obras: {data['obras']['total']}")
    
    def test_check_alerts(self, auth_token):
        """Test checking alerts"""
        response = requests.get(f"{BASE_URL}/api/alerts/check", headers={
            "Authorization": f"Bearer {auth_token}"
        })
        assert response.status_code == 200
        data = response.json()
        assert "alerts" in data
        assert "total" in data
        print(f"✓ Alerts checked - {data['total']} alerts found")


class TestExportImport:
    """Export/Import functionality tests"""
    
    def test_export_pdf(self, auth_token):
        """Test PDF export"""
        response = requests.get(f"{BASE_URL}/api/export/pdf", headers={
            "Authorization": f"Bearer {auth_token}"
        })
        assert response.status_code == 200
        assert response.headers.get("content-type") == "application/pdf"
        assert len(response.content) > 0
        print(f"✓ PDF export successful - {len(response.content)} bytes")
    
    def test_export_excel(self, auth_token):
        """Test Excel export"""
        response = requests.get(f"{BASE_URL}/api/export/excel", headers={
            "Authorization": f"Bearer {auth_token}"
        })
        assert response.status_code == 200
        assert "spreadsheet" in response.headers.get("content-type", "")
        assert len(response.content) > 0
        print(f"✓ Excel export successful - {len(response.content)} bytes")


# Fixtures
@pytest.fixture(scope="session")
def auth_token():
    """Get authentication token for tests"""
    response = requests.post(f"{BASE_URL}/api/auth/login", json={
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD
    })
    if response.status_code != 200:
        # Try to register if login fails
        reg_response = requests.post(f"{BASE_URL}/api/auth/register", json={
            "name": TEST_NAME,
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD
        })
        if reg_response.status_code == 200:
            return reg_response.json()["access_token"]
        pytest.skip("Authentication failed - cannot proceed with tests")
    return response.json()["access_token"]

@pytest.fixture
def created_equipamento_id(auth_token):
    """Create an equipamento for testing and cleanup after"""
    unique_code = f"TEST_EQ_{uuid.uuid4().hex[:6].upper()}"
    response = requests.post(f"{BASE_URL}/api/equipamentos", json={
        "codigo": unique_code,
        "descricao": "Fixture Equipment",
        "marca": "FixtureBrand",
        "modelo": "FixtureModel",
        "estado_conservacao": "Bom",
        "ativo": True
    }, headers={"Authorization": f"Bearer {auth_token}"})
    eq_id = response.json()["id"]
    yield eq_id
    # Cleanup
    requests.delete(f"{BASE_URL}/api/equipamentos/{eq_id}", headers={"Authorization": f"Bearer {auth_token}"})

@pytest.fixture
def created_viatura_id(auth_token):
    """Create a viatura for testing and cleanup after"""
    unique_matricula = f"TEST-{uuid.uuid4().hex[:4].upper()}"
    response = requests.post(f"{BASE_URL}/api/viaturas", json={
        "matricula": unique_matricula,
        "marca": "FixtureMarca",
        "modelo": "FixtureModelo",
        "combustivel": "Gasoleo",
        "ativa": True
    }, headers={"Authorization": f"Bearer {auth_token}"})
    v_id = response.json()["id"]
    yield v_id
    # Cleanup
    requests.delete(f"{BASE_URL}/api/viaturas/{v_id}", headers={"Authorization": f"Bearer {auth_token}"})

@pytest.fixture
def created_material_id(auth_token):
    """Create a material for testing and cleanup after"""
    unique_code = f"TEST_MAT_{uuid.uuid4().hex[:6].upper()}"
    response = requests.post(f"{BASE_URL}/api/materiais", json={
        "codigo": unique_code,
        "descricao": "Fixture Material",
        "unidade": "kg",
        "stock_atual": 50,
        "stock_minimo": 5,
        "ativo": True
    }, headers={"Authorization": f"Bearer {auth_token}"})
    m_id = response.json()["id"]
    yield m_id
    # Cleanup
    requests.delete(f"{BASE_URL}/api/materiais/{m_id}", headers={"Authorization": f"Bearer {auth_token}"})

@pytest.fixture
def created_obra_id(auth_token):
    """Create an obra for testing and cleanup after"""
    unique_code = f"TEST_OBR_{uuid.uuid4().hex[:6].upper()}"
    response = requests.post(f"{BASE_URL}/api/obras", json={
        "codigo": unique_code,
        "nome": "Fixture Obra",
        "endereco": "Fixture Address",
        "cliente": "Fixture Client",
        "estado": "Ativa"
    }, headers={"Authorization": f"Bearer {auth_token}"})
    o_id = response.json()["id"]
    yield o_id
    # Cleanup
    requests.delete(f"{BASE_URL}/api/obras/{o_id}", headers={"Authorization": f"Bearer {auth_token}"})


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
