"""
Test PDF Upload and Maintenance Status Features
- POST /api/upload/pdf - PDF file upload (max 10MB)
- PATCH /api/equipamentos/{id}/manutencao - Update maintenance status without editing other fields
"""
import pytest
import requests
import os
import io

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', '').rstrip('/')

class TestAuth:
    """Get authentication token for tests"""
    
    @pytest.fixture(scope="class")
    def auth_token(self):
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": "test@test.com",
            "password": "test123"
        })
        assert response.status_code == 200, f"Login failed: {response.text}"
        return response.json()["access_token"]
    
    @pytest.fixture(scope="class")
    def headers(self, auth_token):
        return {"Authorization": f"Bearer {auth_token}"}


class TestPdfUpload(TestAuth):
    """Test PDF upload endpoint"""
    
    def test_upload_pdf_success(self, headers):
        """Test uploading a valid PDF file"""
        # Create a minimal valid PDF content
        pdf_content = b"%PDF-1.4\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n2 0 obj\n<< /Type /Pages /Kids [] /Count 0 >>\nendobj\nxref\n0 3\n0000000000 65535 f \n0000000009 00000 n \n0000000058 00000 n \ntrailer\n<< /Size 3 /Root 1 0 R >>\nstartxref\n115\n%%EOF"
        
        files = {"file": ("test_document.pdf", io.BytesIO(pdf_content), "application/pdf")}
        response = requests.post(f"{BASE_URL}/api/upload/pdf", files=files, headers=headers)
        
        assert response.status_code == 200, f"PDF upload failed: {response.text}"
        data = response.json()
        assert "url" in data, "Response should contain 'url'"
        assert "filename" in data, "Response should contain 'filename'"
        assert "original_name" in data, "Response should contain 'original_name'"
        assert data["url"].startswith("/api/uploads/"), "URL should start with /api/uploads/"
        assert data["url"].endswith(".pdf"), "URL should end with .pdf"
        assert data["original_name"] == "test_document.pdf", "Original name should match"
        print(f"✓ PDF uploaded successfully: {data['url']}")
    
    def test_upload_pdf_rejects_non_pdf(self, headers):
        """Test that non-PDF files are rejected"""
        # Try to upload a text file
        text_content = b"This is not a PDF file"
        files = {"file": ("test.txt", io.BytesIO(text_content), "text/plain")}
        response = requests.post(f"{BASE_URL}/api/upload/pdf", files=files, headers=headers)
        
        assert response.status_code == 400, f"Should reject non-PDF: {response.status_code}"
        data = response.json()
        assert "detail" in data, "Response should contain error detail"
        assert "PDF" in data["detail"], "Error should mention PDF"
        print(f"✓ Non-PDF file correctly rejected: {data['detail']}")
    
    def test_upload_pdf_rejects_image(self, headers):
        """Test that image files are rejected"""
        # Create a minimal PNG header
        png_content = b'\x89PNG\r\n\x1a\n' + b'\x00' * 100
        files = {"file": ("test.png", io.BytesIO(png_content), "image/png")}
        response = requests.post(f"{BASE_URL}/api/upload/pdf", files=files, headers=headers)
        
        assert response.status_code == 400, f"Should reject image: {response.status_code}"
        print("✓ Image file correctly rejected")
    
    def test_upload_pdf_requires_auth(self):
        """Test that PDF upload requires authentication"""
        pdf_content = b"%PDF-1.4\ntest"
        files = {"file": ("test.pdf", io.BytesIO(pdf_content), "application/pdf")}
        response = requests.post(f"{BASE_URL}/api/upload/pdf", files=files)
        
        assert response.status_code in [401, 403], f"Should require auth: {response.status_code}"
        print("✓ PDF upload correctly requires authentication")


class TestManutencaoEndpoint(TestAuth):
    """Test PATCH /api/equipamentos/{id}/manutencao endpoint"""
    
    @pytest.fixture(scope="class")
    def test_equipamento(self, headers):
        """Create a test equipamento for maintenance tests"""
        payload = {
            "codigo": "TEST_MANUT_001",
            "descricao": "Equipamento para teste de manutenção",
            "marca": "TestMarca",
            "modelo": "TestModelo",
            "ativo": True,
            "estado_conservacao": "Bom",
            "em_manutencao": False,
            "descricao_avaria": ""
        }
        response = requests.post(f"{BASE_URL}/api/equipamentos", json=payload, headers=headers)
        
        if response.status_code == 400 and "já existe" in response.text:
            # Get existing equipamento
            list_response = requests.get(f"{BASE_URL}/api/equipamentos", headers=headers)
            equipamentos = list_response.json()
            for eq in equipamentos:
                if eq.get("codigo") == "TEST_MANUT_001":
                    return eq
        
        assert response.status_code in [200, 201], f"Failed to create test equipamento: {response.text}"
        return response.json()
    
    def test_marcar_em_manutencao(self, headers, test_equipamento):
        """Test marking equipamento as in maintenance"""
        eq_id = test_equipamento["id"]
        
        payload = {
            "em_manutencao": True,
            "descricao_avaria": "Motor não funciona - enviado para oficina"
        }
        response = requests.patch(f"{BASE_URL}/api/equipamentos/{eq_id}/manutencao", json=payload, headers=headers)
        
        assert response.status_code == 200, f"Failed to update maintenance: {response.text}"
        data = response.json()
        assert data["em_manutencao"] == True, "em_manutencao should be True"
        assert data["descricao_avaria"] == "Motor não funciona - enviado para oficina", "descricao_avaria should match"
        # Verify other fields are unchanged
        assert data["codigo"] == test_equipamento["codigo"], "codigo should be unchanged"
        assert data["descricao"] == test_equipamento["descricao"], "descricao should be unchanged"
        print(f"✓ Equipamento marked as in maintenance: {data['descricao_avaria']}")
    
    def test_marcar_disponivel(self, headers, test_equipamento):
        """Test marking equipamento as available (removing from maintenance)"""
        eq_id = test_equipamento["id"]
        
        payload = {
            "em_manutencao": False,
            "descricao_avaria": ""
        }
        response = requests.patch(f"{BASE_URL}/api/equipamentos/{eq_id}/manutencao", json=payload, headers=headers)
        
        assert response.status_code == 200, f"Failed to update maintenance: {response.text}"
        data = response.json()
        assert data["em_manutencao"] == False, "em_manutencao should be False"
        assert data["descricao_avaria"] == "", "descricao_avaria should be empty"
        print("✓ Equipamento marked as available")
    
    def test_manutencao_preserves_other_fields(self, headers, test_equipamento):
        """Test that PATCH manutencao doesn't change other fields"""
        eq_id = test_equipamento["id"]
        
        # First, get current state
        get_response = requests.get(f"{BASE_URL}/api/equipamentos/{eq_id}", headers=headers)
        assert get_response.status_code == 200
        original = get_response.json()["equipamento"]
        
        # Update maintenance status
        payload = {
            "em_manutencao": True,
            "descricao_avaria": "Teste de preservação de campos"
        }
        response = requests.patch(f"{BASE_URL}/api/equipamentos/{eq_id}/manutencao", json=payload, headers=headers)
        assert response.status_code == 200
        updated = response.json()
        
        # Verify other fields are preserved
        assert updated["codigo"] == original["codigo"], "codigo should be preserved"
        assert updated["descricao"] == original["descricao"], "descricao should be preserved"
        assert updated["marca"] == original["marca"], "marca should be preserved"
        assert updated["modelo"] == original["modelo"], "modelo should be preserved"
        assert updated["ativo"] == original["ativo"], "ativo should be preserved"
        assert updated["estado_conservacao"] == original["estado_conservacao"], "estado_conservacao should be preserved"
        print("✓ Other fields preserved during maintenance update")
    
    def test_manutencao_not_found(self, headers):
        """Test PATCH manutencao with non-existent equipamento"""
        payload = {
            "em_manutencao": True,
            "descricao_avaria": "Test"
        }
        response = requests.patch(f"{BASE_URL}/api/equipamentos/non-existent-id/manutencao", json=payload, headers=headers)
        
        assert response.status_code == 404, f"Should return 404: {response.status_code}"
        print("✓ Non-existent equipamento correctly returns 404")
    
    def test_manutencao_requires_auth(self, test_equipamento):
        """Test that PATCH manutencao requires authentication"""
        eq_id = test_equipamento["id"]
        payload = {
            "em_manutencao": True,
            "descricao_avaria": "Test"
        }
        response = requests.patch(f"{BASE_URL}/api/equipamentos/{eq_id}/manutencao", json=payload)
        
        assert response.status_code in [401, 403], f"Should require auth: {response.status_code}"
        print("✓ PATCH manutencao correctly requires authentication")


class TestEquipamentoStatusInList(TestAuth):
    """Test that equipamento status is correctly returned in list"""
    
    def test_list_includes_manutencao_status(self, headers):
        """Test that equipamentos list includes em_manutencao field"""
        response = requests.get(f"{BASE_URL}/api/equipamentos", headers=headers)
        
        assert response.status_code == 200, f"Failed to get equipamentos: {response.text}"
        equipamentos = response.json()
        
        # Check that at least one equipamento has the em_manutencao field
        has_manutencao_field = False
        for eq in equipamentos:
            if "em_manutencao" in eq:
                has_manutencao_field = True
                break
        
        assert has_manutencao_field, "Equipamentos should have em_manutencao field"
        print(f"✓ Equipamentos list includes em_manutencao field ({len(equipamentos)} items)")
    
    def test_detail_includes_manutencao_status(self, headers):
        """Test that equipamento detail includes em_manutencao field"""
        # Get first equipamento
        list_response = requests.get(f"{BASE_URL}/api/equipamentos", headers=headers)
        assert list_response.status_code == 200
        equipamentos = list_response.json()
        
        if len(equipamentos) > 0:
            eq_id = equipamentos[0]["id"]
            detail_response = requests.get(f"{BASE_URL}/api/equipamentos/{eq_id}", headers=headers)
            
            assert detail_response.status_code == 200, f"Failed to get detail: {detail_response.text}"
            data = detail_response.json()
            
            assert "equipamento" in data, "Response should have 'equipamento' key"
            eq = data["equipamento"]
            assert "em_manutencao" in eq, "Equipamento should have em_manutencao field"
            assert "descricao_avaria" in eq, "Equipamento should have descricao_avaria field"
            print(f"✓ Equipamento detail includes maintenance fields: em_manutencao={eq['em_manutencao']}")


class TestCleanup(TestAuth):
    """Cleanup test data"""
    
    def test_cleanup_test_equipamento(self, headers):
        """Remove test equipamento created during tests"""
        # Find and delete test equipamento
        list_response = requests.get(f"{BASE_URL}/api/equipamentos", headers=headers)
        if list_response.status_code == 200:
            equipamentos = list_response.json()
            for eq in equipamentos:
                if eq.get("codigo", "").startswith("TEST_MANUT_"):
                    delete_response = requests.delete(f"{BASE_URL}/api/equipamentos/{eq['id']}", headers=headers)
                    print(f"✓ Cleaned up test equipamento: {eq['codigo']}")
        print("✓ Cleanup completed")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
