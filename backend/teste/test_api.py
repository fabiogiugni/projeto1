import requests
import json
import random
import string

# Configurações
BASE_URL = "http://localhost:8000"

class APITester:
    def __init__(self, base_url):
        self.base_url = base_url
        self.created_ids = {}
        self.session = requests.Session()
        
    def generate_random_string(self, length=10):
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
    
    def generate_random_cpf(self):
        return ''.join(random.choices(string.digits, k=11))
    
    def generate_random_cnpj(self):
        return ''.join(random.choices(string.digits, k=14))
    
    def print_test_result(self, test_name, success, response=None):
        status = "✅ PASSOU" if success else "❌ FALHOU"
        print(f"{status} - {test_name}")
        if not success and response:
            print(f"   Erro: {response.status_code} - {response.text}")
    
    def test_root_endpoint(self):
        try:
            response = self.session.get(f"{self.base_url}/")
            success = response.status_code == 200
            self.print_test_result("Endpoint Raiz", success, response if not success else None)
            return success
        except Exception as e:
            self.print_test_result("Endpoint Raiz", False)
            print(f"   Exceção: {e}")
            return False
    
    def test_company_operations(self):
        print("\n🔧 TESTANDO OPERAÇÕES DE EMPRESA")
        
        company_data = {
            "name": f"Empresa Teste {self.generate_random_string()}",
            "cnpj": self.generate_random_cnpj()
        }
        
        try:
            response = self.session.post(f"{self.base_url}/company", json=company_data)
            success = response.status_code == 200
            self.print_test_result("Criar Empresa", success, response if not success else None)
            
            if success:
                response = self.session.get(f"{self.base_url}/company/{company_data['cnpj']}")
                success_get = response.status_code == 200
                self.print_test_result("Buscar Empresa por CNPJ", success_get, response if not success_get else None)
                
                if success_get:
                    company_info = response.json()
                    self.created_ids['company_id'] = company_info['data']['_id']
                    self.created_ids['company_cnpj'] = company_data['cnpj']
            
            return success
        except Exception as e:
            self.print_test_result("Operações de Empresa", False)
            print(f"   Exceção: {e}")
            return False
    
    def test_department_operations(self):
        print("\n🔧 TESTANDO OPERAÇÕES DE DEPARTAMENTO")
        
        if not self.created_ids.get('company_id'):
            print("⚠️  Pulando teste de departamento - empresa não criada")
            return False
        
        department_data = {
            "name": f"Departamento Teste {self.generate_random_string()}",
            "companyID": self.created_ids['company_id']
        }
        
        try:
            response = self.session.post(f"{self.base_url}/department", json=department_data)
            success = response.status_code == 200
            self.print_test_result("Criar Departamento", success, response if not success else None)
            
            if success:
                response = self.session.get(f"{self.base_url}/getAllDepartments")
                success_get_all = response.status_code == 200
                self.print_test_result("Buscar Todos Departamentos", success_get_all, response if not success_get_all else None)
                
                if success_get_all:
                    departments = response.json()['data']
                    if departments:
                        self.created_ids['department_id'] = departments[0]['_id']
            
            return success
        except Exception as e:
            self.print_test_result("Operações de Departamento", False)
            print(f"   Exceção: {e}")
            return False
    
    def test_team_operations(self):
        print("\n🔧 TESTANDO OPERAÇÕES DE TIME")
        
        if not self.created_ids.get('department_id'):
            print("⚠️  Pulando teste de time - departamento não criado")
            return False
        
        team_data = {
            "name": f"Time Teste {self.generate_random_string()}",
            "departmentID": self.created_ids['department_id']
        }
        
        try:
            response = self.session.post(f"{self.base_url}/team", json=team_data)
            success = response.status_code == 200
            self.print_test_result("Criar Time", success, response if not success else None)
            
            if success:
                response = self.session.get(f"{self.base_url}/getAllTeams")
                success_get_all = response.status_code == 200
                self.print_test_result("Buscar Todos Times", success_get_all, response if not success_get_all else None)
                
                if success_get_all:
                    teams = response.json()['data']
                    if teams:
                        self.created_ids['team_id'] = teams[0]['_id']
            
            return success
        except Exception as e:
            self.print_test_result("Operações de Time", False)
            print(f"   Exceção: {e}")
            return False
    
    def test_user_operations(self):
        print("\n🔧 TESTANDO OPERAÇÕES DE USUÁRIO")
        
        if not self.created_ids.get('company_id'):
            print("⚠️  Pulando teste de usuário - empresa não criada")
            return False
        
        user_data = {
            "name": f"Usuário Teste {self.generate_random_string()}",
            "cpf": self.generate_random_cpf(),
            "companyID": self.created_ids['company_id'],
            "departmentID": self.created_ids.get('department_id'),
            "teamID": self.created_ids.get('team_id'),
            "email": f"test{self.generate_random_string()}@example.com",
            "password": "testpassword123"
        }
        
        try:
            response = self.session.post(f"{self.base_url}/user", json=user_data)
            success = response.status_code == 200
            self.print_test_result("Criar Usuário", success, response if not success else None)
            
            if success:
                response = self.session.get(f"{self.base_url}/user_by_email/{user_data['email']}")
                success_get_email = response.status_code == 200
                self.print_test_result("Buscar Usuário por Email", success_get_email, response if not success_get_email else None)
                
                if success_get_email:
                    user_info = response.json()['data']
                    self.created_ids['user_id'] = user_info['_id']
                    self.created_ids['user_email'] = user_data['email']
            
            return success
        except Exception as e:
            self.print_test_result("Operações de Usuário", False)
            print(f"   Exceção: {e}")
            return False
    
    def test_rpe_operations(self):
        print("\n🔧 TESTANDO OPERAÇÕES DE RPE")
        
        if not self.created_ids.get('user_id'):
            print("⚠️  Pulando teste de RPE - usuário não criado")
            return False
        
        rpe_data = {
            "description": f"RPE Teste {self.generate_random_string()}",
            "responsibleID": self.created_ids['user_id']
        }
        
        try:
            response = self.session.post(f"{self.base_url}/RPE", json=rpe_data)
            success = response.status_code == 200
            self.print_test_result("Criar RPE", success, response if not success else None)
            
            if success:
                rpe_info = response.json()
                rpe_id = rpe_info.get('id')
                if rpe_id:
                    self.created_ids['rpe_id'] = rpe_id
                    
                    response = self.session.get(f"{self.base_url}/RPE/{rpe_id}")
                    success_get = response.status_code == 200
                    self.print_test_result("Buscar RPE por ID", success_get, response if not success_get else None)
            
            return success
        except Exception as e:
            self.print_test_result("Operações de RPE", False)
            print(f"   Exceção: {e}")
            return False
    
    def test_delete_operations_complete(self):
        """Testa operações de delete para todos os objetos"""
        print("\n🔧 TESTANDO OPERAÇÕES DE DELETE COMPLETAS")
        
        delete_tests = []
        
        # Testar delete de todos os objetos criados (na ordem inversa da criação)
        objects_to_delete = [
            ('kr_id', 'kr', 'KR'),
            ('kpi_id', 'kpi', 'KPI'),
            ('objective_id', 'objective', 'Objective'),
            ('rpe_id', 'rpe', 'RPE'),
            ('user_id', 'user', 'User'),
            ('team_id', 'team', 'Team'),
            ('department_id', 'department', 'Department'),
            ('company_id', 'company', 'Company'),
        ]
        
        for id_key, endpoint, name in objects_to_delete:
            if self.created_ids.get(id_key):
                try:
                    response = self.session.delete(f"{self.base_url}/{endpoint}/{self.created_ids[id_key]}")
                    success = response.status_code == 200
                    delete_tests.append((f"Delete {name}", success))
                    if not success:
                        print(f"   Erro: {response.status_code} - {response.text}")
                except Exception as e:
                    delete_tests.append((f"Delete {name}", False))
                    print(f"   Exceção: {e}")
        
        # Imprimir resultados dos testes de delete
        for test_name, success in delete_tests:
            self.print_test_result(test_name, success)
        
        return len(delete_tests) > 0
    
    def test_all_endpoints(self):
        """Executa todos os testes"""
        print("🚀 INICIANDO TESTES AUTOMATIZADOS DA API")
        print("=" * 50)
        
        tests = [
            self.test_root_endpoint,
            self.test_company_operations,
            self.test_department_operations,
            self.test_team_operations,
            self.test_user_operations,
            self.test_rpe_operations,
            self.test_delete_operations_complete,  # Agora testa todos os deletes
        ]
        
        results = []
        for test in tests:
            try:
                result = test()
                results.append(result)
            except Exception as e:
                print(f"❌ ERRO NO TESTE {test.__name__}: {e}")
                results.append(False)
        
        # Relatório final
        print("\n" + "=" * 50)
        print("📊 RELATÓRIO FINAL DOS TESTES")
        print("=" * 50)
        
        passed = sum(results)
        total = len(results)
        
        print(f"✅ Testes passados: {passed}/{total}")
        print(f"❌ Testes falhados: {total - passed}/{total}")
        print(f"📈 Taxa de sucesso: {(passed/total)*100:.1f}%")
        
        if passed == total:
            print("🎉 TODOS OS TESTES PASSARAM!")
        else:
            print("⚠️  Alguns testes falharam. Verifique os logs acima.")
        
        return all(results)

# Executar os testes
if __name__ == "__main__":
    tester = APITester(BASE_URL)
    
    print("⚠️  AVISO: Teste automatizado com operações de DELETE")
    print("Os objetos criados durante o teste serão DELETADOS ao final!")
    print("Execute a API antes de rodar os testes!\n")
    
    input("Pressione Enter para iniciar os testes...")
    
    success = tester.test_all_endpoints()
    
    if success:
        print("\n✨ Testes concluídos com sucesso! Todos os objetos de teste foram limpos.")
    else:
        print("\n💥 Alguns testes falharam. Verifique a configuração da API.")