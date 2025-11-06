# test_api.py
import requests
import json
import time
import random
import string

class APITester:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.created_ids = {
            "companies": [],
            "departments": [], 
            "teams": [],
            "users": [],
            "rpes": [],
            "objectives": [],
            "krs": [],
            "kpis": []
        }
    
    def generate_random_string(self, length=8):
        """Gera uma string aleatória para testes"""
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
    
    def generate_random_email(self):
        """Gera um email aleatório para testes"""
        return f"test_{self.generate_random_string()}@example.com"
    
    def generate_random_cpf(self):
        """Gera um CPF aleatório para testes (apenas para testes)"""
        return ''.join(random.choices(string.digits, k=11))
    
    def generate_random_cnpj(self):
        """Gera um CNPJ aleatório para testes (apenas para testes)"""
        return ''.join(random.choices(string.digits, k=14))
    
    def print_test_result(self, test_name, success, response=None):
        """Imprime o resultado do teste"""
        status = "✅ PASSOU" if success else "❌ FALHOU"
        print(f"{status} - {test_name}")
        if not success and response:
            print(f"   Erro: {response.status_code} - {response.text}")
    
    def test_health_check(self):
        """Testa o endpoint raiz"""
        try:
            response = requests.get(f"{self.base_url}/")
            success = response.status_code == 200 and "Backend Python funcionando" in response.text
            self.print_test_result("Health Check", success, response)
            return success
        except Exception as e:
            self.print_test_result("Health Check", False)
            print(f"   Exception: {e}")
            return False
    
    def test_company_operations(self):
        """Testa operações de empresa"""
        try:
            # Criar empresa
            company_data = {
                "name": f"Empresa Teste {self.generate_random_string()}",
                "cnpj": self.generate_random_cnpj()
            }
            response = requests.post(f"{self.base_url}/company", json=company_data)
            success = response.status_code == 200
            self.print_test_result("Criar Empresa", success, response)
            
            if success:
                company_id = response.json().get("id")
                if company_id:
                    self.created_ids["companies"].append(company_id)
            
            # Buscar empresa por CNPJ
            if success:
                response = requests.get(f"{self.base_url}/company/{company_data['cnpj']}")
                success = response.status_code == 200
                self.print_test_result("Buscar Empresa por CNPJ", success, response)
            
            return success
        except Exception as e:
            self.print_test_result("Operações de Empresa", False)
            print(f"   Exception: {e}")
            return False
    
    def test_user_operations(self):
        """Testa operações de usuário"""
        try:
            # Primeiro cria uma empresa para associar o usuário
            company_data = {
                "name": f"Empresa para Usuário {self.generate_random_string()}",
                "cnpj": self.generate_random_cnpj()
            }
            company_response = requests.post(f"{self.base_url}/company", json=company_data)
            
            if company_response.status_code != 200:
                self.print_test_result("Criar Usuário - Empresa Base", False, company_response)
                return False
            
            company_id = company_response.json().get("id")
            self.created_ids["companies"].append(company_id)
            
            # Criar usuário
            user_data = {
                "name": f"Usuário Teste {self.generate_random_string()}",
                "cpf": self.generate_random_cpf(),
                "companyID": company_id,
                "email": self.generate_random_email(),
                "password": "senha123"
            }
            response = requests.post(f"{self.base_url}/user", json=user_data)
            success = response.status_code == 200
            self.print_test_result("Criar Usuário", success, response)
            
            user_id = None
            if success:
                # Em uma implementação real, a API retornaria o ID do usuário criado
                # Para teste, vamos assumir que podemos buscar pelo email
                response = requests.get(f"{self.base_url}/user_by_email/{user_data['email']}")
                if response.status_code == 200:
                    user_id = "test_user_id"  # Em produção, extrair do response
                    self.created_ids["users"].append(user_id)
            
            return success
        except Exception as e:
            self.print_test_result("Operações de Usuário", False)
            print(f"   Exception: {e}")
            return False
    
    def test_rpe_operations(self):
        """Testa operações de RPE"""
        try:
            # Criar RPE
            rpe_data = {
                "description": f"RPE Teste {self.generate_random_string()}",
                "responsibleID": "test_responsible_id"  # Em produção, usar ID real
            }
            response = requests.post(f"{self.base_url}/RPE", json=rpe_data)
            success = response.status_code == 200
            self.print_test_result("Criar RPE", success, response)
            
            if success:
                rpe_id = response.json().get("id")
                if rpe_id:
                    self.created_ids["rpes"].append(rpe_id)
                
                # Buscar RPE por ID
                response = requests.get(f"{self.base_url}/RPE/{rpe_id}")
                self.print_test_result("Buscar RPE por ID", response.status_code == 200, response)
            
            return success
        except Exception as e:
            self.print_test_result("Operações de RPE", False)
            print(f"   Exception: {e}")
            return False
    
    def test_objective_kr_kpi_operations(self):
        """Testa operações de Objective, KR e KPI"""
        try:
            # Primeiro cria um RPE
            rpe_data = {
                "description": f"RPE para Objective {self.generate_random_string()}",
                "responsibleID": "test_responsible_id"
            }
            rpe_response = requests.post(f"{self.base_url}/RPE", json=rpe_data)
            
            if rpe_response.status_code != 200:
                self.print_test_result("Criar RPE para Objective", False, rpe_response)
                return False
            
            rpe_id = rpe_response.json().get("id")
            self.created_ids["rpes"].append(rpe_id)
            
            # Criar Objective
            objective_data = {
                "description": f"Objective Teste {self.generate_random_string()}",
                "responsibleID": "test_responsible_id",
                "RPEID": rpe_id
            }
            response = requests.post(f"{self.base_url}/objective", json=objective_data)
            success = response.status_code == 200
            self.print_test_result("Criar Objective", success, response)
            
            objective_id = None
            if success:
                objective_id = response.json().get("id")
                self.created_ids["objectives"].append(objective_id)
                
                # Criar KR
                kr_data = {
                    "description": f"KR Teste {self.generate_random_string()}",
                    "responsibleID": "test_responsible_id",
                    "goal": 100.0,
                    "objectiveID": objective_id
                }
                response = requests.post(f"{self.base_url}/kr", json=kr_data)
                kr_success = response.status_code == 200
                self.print_test_result("Criar KR", kr_success, response)
                
                if kr_success:
                    kr_id = response.json().get("id")
                    self.created_ids["krs"].append(kr_id)
                    
                    # Atualizar goal do KR
                    kr_update_data = {"goal": 150.0}
                    response = requests.put(f"{self.base_url}/kr_goal/{kr_id}", json=kr_update_data)
                    self.print_test_result("Atualizar Goal do KR", response.status_code == 200, response)
                    
                    # Adicionar dados ao KR
                    data_add = {"data": 75.5}
                    response = requests.put(f"{self.base_url}/kr_data/{kr_id}", json=data_add)
                    self.print_test_result("Adicionar Dados ao KR", response.status_code == 200, response)
                
                # Criar KPI
                kpi_data = {
                    "description": f"KPI Teste {self.generate_random_string()}",
                    "responsibleID": "test_responsible_id", 
                    "objectiveID": objective_id
                }
                response = requests.post(f"{self.base_url}/kpi", json=kpi_data)
                kpi_success = response.status_code == 200
                self.print_test_result("Criar KPI", kpi_success, response)
                
                if kpi_success:
                    kpi_id = response.json().get("id")
                    self.created_ids["kpis"].append(kpi_id)
                    
                    # Adicionar dados ao KPI
                    data_add = {"data": 85.0}
                    response = requests.put(f"{self.base_url}/kpi_data/{kpi_id}", json=data_add)
                    self.print_test_result("Adicionar Dados ao KPI", response.status_code == 200, response)
            
            return success
        except Exception as e:
            self.print_test_result("Operações Objective/KR/KPI", False)
            print(f"   Exception: {e}")
            return False
    
    def test_department_operations(self):
        """Testa operações de departamento"""
        try:
            # Criar empresa primeiro
            company_data = {
                "name": f"Empresa para Departamento {self.generate_random_string()}",
                "cnpj": self.generate_random_cnpj()
            }
            company_response = requests.post(f"{self.base_url}/company", json=company_data)
            
            if company_response.status_code != 200:
                self.print_test_result("Criar Departamento - Empresa Base", False, company_response)
                return False
            
            company_id = company_response.json().get("id")
            self.created_ids["companies"].append(company_id)
            
            # Criar departamento
            department_data = {
                "name": f"Departamento Teste {self.generate_random_string()}",
                "companyID": company_id
            }
            response = requests.post(f"{self.base_url}/department", json=department_data)
            success = response.status_code == 200
            self.print_test_result("Criar Departamento", success, response)
            
            if success:
                department_id = response.json().get("id")
                if department_id:
                    self.created_ids["departments"].append(department_id)
            
            return success
        except Exception as e:
            self.print_test_result("Operações de Departamento", False)
            print(f"   Exception: {e}")
            return False
    
    def test_team_operations(self):
        """Testa operações de equipe"""
        try:
            # Criar empresa e departamento primeiro
            company_data = {
                "name": f"Empresa para Equipe {self.generate_random_string()}",
                "cnpj": self.generate_random_cnpj()
            }
            company_response = requests.post(f"{self.base_url}/company", json=company_data)
            company_id = company_response.json().get("id")
            self.created_ids["companies"].append(company_id)
            
            department_data = {
                "name": f"Departamento para Equipe {self.generate_random_string()}",
                "companyID": company_id
            }
            department_response = requests.post(f"{self.base_url}/department", json=department_data)
            department_id = department_response.json().get("id")
            self.created_ids["departments"].append(department_id)
            
            # Criar equipe
            team_data = {
                "name": f"Equipe Teste {self.generate_random_string()}",
                "departmentID": department_id
            }
            response = requests.post(f"{self.base_url}/team", json=team_data)
            success = response.status_code == 200
            self.print_test_result("Criar Equipe", success, response)
            
            if success:
                team_id = response.json().get("id")
                if team_id:
                    self.created_ids["teams"].append(team_id)
            
            return success
        except Exception as e:
            self.print_test_result("Operações de Equipe", False)
            print(f"   Exception: {e}")
            return False
    
    def test_error_cases(self):
        """Testa casos de erro"""
        try:
            # Buscar usuário inexistente
            response = requests.get(f"{self.base_url}/user_by_email/email_inexistente@example.com")
            self.print_test_result("Buscar Usuário Inexistente", response.status_code == 404, response)
            
            # Buscar RPE inexistente
            response = requests.get(f"{self.base_url}/RPE/id_inexistente_123")
            self.print_test_result("Buscar RPE Inexistente", response.status_code == 404, response)
            
            return True
        except Exception as e:
            self.print_test_result("Testes de Casos de Erro", False)
            print(f"   Exception: {e}")
            return False
    
    def cleanup(self):
        """Limpa os dados de teste criados"""
        print("\n🧹 Executando limpeza dos dados de teste...")
        
        for resource_type, ids in self.created_ids.items():
            for resource_id in ids:
                try:
                    response = requests.delete(f"{self.base_url}/delete/{resource_id}")
                    if response.status_code == 200:
                        print(f"   ✅ {resource_type.capitalize()} {resource_id} deletado")
                    else:
                        print(f"   ❌ Falha ao deletar {resource_type} {resource_id}")
                except Exception as e:
                    print(f"   ❌ Erro ao deletar {resource_type} {resource_id}: {e}")
    
    def run_all_tests(self):
        """Executa todos os testes"""
        print("🚀 Iniciando testes automatizados da API")
        print("=" * 50)
        
        tests = [
            ("Health Check", self.test_health_check),
            ("Operações de Empresa", self.test_company_operations),
            ("Operações de Departamento", self.test_department_operations),
            ("Operações de Equipe", self.test_team_operations),
            ("Operações de Usuário", self.test_user_operations),
            ("Operações de RPE", self.test_rpe_operations),
            ("Operações Objective/KR/KPI", self.test_objective_kr_kpi_operations),
            ("Casos de Erro", self.test_error_cases)
        ]
        
        results = []
        for test_name, test_func in tests:
            print(f"\n🔍 Executando: {test_name}")
            result = test_func()
            results.append(result)
            time.sleep(0.5)  # Pequena pausa entre testes
        
        # Estatísticas
        passed = sum(results)
        total = len(results)
        
        print("\n" + "=" * 50)
        print("📊 RESUMO DOS TESTES")
        print("=" * 50)
        print(f"✅ Testes passaram: {passed}/{total}")
        print(f"❌ Testes falharam: {total - passed}/{total}")
        print(f"📈 Taxa de sucesso: {(passed/total)*100:.1f}%")
        
        if passed == total:
            print("\n🎉 Todos os testes passaram!")
        else:
            print("\n⚠️  Alguns testes falharam. Verifique os logs acima.")
        
        return all(results)

# Script de execução
if __name__ == "__main__":
    import sys
    
    # Verificar se a API está rodando
    try:
        response = requests.get("http://localhost:8000/", timeout=5)
        print("✅ API está respondendo!")
    except:
        print("❌ API não está respondendo em http://localhost:8000/")
        print("💡 Execute a API primeiro com: python main.py")
        sys.exit(1)
    
    tester = APITester()
    
    try:
        # Executar testes
        success = tester.run_all_tests()
        
        # Perguntar se deseja limpar dados de teste
        if success and tester.created_ids["companies"]:  # Só pergunta se criou algum dado
            cleanup = input("\n🧹 Deseja limpar os dados de teste? (s/N): ").lower().strip()
            if cleanup in ['s', 'sim', 'y', 'yes']:
                tester.cleanup()
            else:
                print("Dados de teste mantidos para inspeção.")
        
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print("\n⏹️  Testes interrompidos pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Erro inesperado durante os testes: {e}")
        sys.exit(1)