export const companies = [
  { id: 1, name: "TechCorp", cnpj: "11.111.111/0001-11" },
];

export const departments = [
  { id: 1, name: "Financeiro", companyId: 1 },
  { id: 2, name: "Operacional", companyId: 1 },
  { id: 3, name: "Comercial", companyId: 2 },
];

export const teams = [
  { id: 1, name: "Equipe A", departmentId: 1, managerId: 1 },
  { id: 2, name: "Equipe B", departmentId: 2, managerId: 2 },
  { id: 3, name: "Equipe C", departmentId: 3, managerId: 3 },
];

export const rpes = [
  {
    id: 1,
    name: "RPE Financeiro 2025",
    description: "RPE Financeiro 2025",
    departmentId: 1,
  },
  {
    id: 2,
    name: "RPE Operacional 2025",
    description: "RPE Financeiro 2025",
    departmentId: 2,
  },
  {
    id: 3,
    name: "RPE Comercial 2025",
    description: "RPE Financeiro 2025",
    departmentId: 3,
  },
];

export const objectives = [
  {
    id: 1,
    name: "Aumentar Receita",
    description: "Aumentar Receita",
    rpeId: 1,
  },
  { id: 2, name: "Reduzir Custos", description: "Aumentar Receita", rpeId: 2 },
  {
    id: 3,
    name: "Expandir Mercado",
    description: "Aumentar Receita",
    rpeId: 3,
  },
];

export const krs = [
  {
    id: 1,
    name: "Lucro Líquido",
    description: "Descrição novos clientes",
    goal: 100000,
    objectiveId: 1,
    value: 10,
    prevValue: 6,
  },
  {
    id: 2,
    name: "Eficiência Operacional",
    description: "Descrição novos clientes",
    goal: 0.85,
    objectiveId: 2,
    value: 10,
    prevValue: 5,
  },
  {
    id: 3,
    name: "Novos Clientes",
    description: "Descrição novos clientes",
    goal: 50,
    objectiveId: 3,
    value: 9,
    prevValue: 4,
  },
];

export const kpis = [
  {
    id: 1,
    name: "ROI",
    description: "Descrição ROI",
    goal: 10,
    krId: 1,
    value: 10,
    prevValue: 6,
  },
  {
    id: 2,
    name: "Taxa de Produção",
    description: "Descrição Taxa de Prod",
    value: 30,
    goal: 90,
    krId: 2,
    prevValue: 5,
  },
  {
    id: 3,
    name: "Conversão de Vendas",
    description: "Descrição Conversão",
    krId: 3,
    prevValue: 4,
    value: 10,
  },
];

export const persons = [
  {
    id: 1,
    name: "João Silva",
    email: "joao@techcorp.com",
    role: "employee",
    teamId: 1,
  },
  {
    id: 2,
    name: "Maria Souza",
    email: "maria@techcorp.com",
    role: "employee",
    teamId: 2,
  },
  {
    id: 3,
    name: "Pedro Lima",
    email: "pedro@ecosolutions.com",
    role: "employee",
    teamId: 3,
  },
];

export const managers = [
  {
    id: 1,
    name: "Ana Lima",
    email: "ana@techcorp.com",
    role: "manager",
    departmentId: 1,
  },
  {
    id: 2,
    name: "Carlos Mendes",
    email: "carlos@techcorp.com",
    role: "manager",
    departmentId: 2,
  },
  {
    id: 3,
    name: "Rafael Costa",
    email: "rafael@ecosolutions.com",
    role: "manager",
    departmentId: 3,
  },
];

export const directors = [
  {
    id: 1,
    name: "Fernanda Alves",
    email: "fernanda@techcorp.com",
    role: "director",
    companyId: 1,
  },
  {
    id: 2,
    name: "Lucas Rocha",
    email: "lucas@ecosolutions.com",
    role: "director",
    companyId: 2,
  },
];
