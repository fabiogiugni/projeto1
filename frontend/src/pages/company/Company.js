import { useEffect, useState } from "react";
import { CommonPageTable, Input, Select, CreateModal } from "../../components";
import styles from "./Company.module.css";
import plusCircle from "../../assets/Plus-circle.svg";

export default function Company() {
  const [searchedDepartment, setSearchedDepartment] = useState("");
  const [dataToShowOnTable, setDataToShowOnTable] = useState([]);
  const [allDepartments, setAllDepartments] = useState([]);

  const [employeeOptions, setEmployeeOptions] = useState([]);
  const [openCreateModal, setOpenCreateModal] = useState(false);

  // ===============================
  // Carregar departamentos
  // ===============================
  useEffect(() => {
    async function fetchDepartments() {
      const response = await fetch(`http://localhost:8000/getAllDepartments`);
      const data = await response.json();

      setAllDepartments(data.data);
      setDataToShowOnTable(data.data);
    }

    fetchDepartments();
  }, []);

  // ===============================
  // Carregar funcionários (para select)
  // ===============================
  useEffect(() => {
    async function fetchEmployees() {
      const response = await fetch(`http://localhost:8000/getAllEmployees`);
      const data = await response.json();
      setEmployeeOptions(data.data);
    }

    fetchEmployees();
  }, []);

  // ===============================
  // Filtrar apenas diretores
  // ===============================
  const directorOptions = employeeOptions
    .filter((u) => u._role === "Director")
    .map((u) => ({
      label: u._name,
      value: u._id,
    }));

  // ===============================
  // Filtro digitado
  // ===============================
  useEffect(() => {
    if (!searchedDepartment) {
      setDataToShowOnTable(allDepartments);
      return;
    }

    const filtered = allDepartments.filter((dept) =>
      dept._name.toLowerCase().includes(searchedDepartment.toLowerCase())
    );

    setDataToShowOnTable(filtered);
  }, [searchedDepartment, allDepartments]);

  // ===============================
  // Atualizar tabela após exclusão
  // ===============================
  async function handleDeleteFunction() {
    const response = await fetch(`http://localhost:8000/getAllDepartments`);
    const updated = await response.json();

    setAllDepartments(updated.data);
    setDataToShowOnTable(updated.data);
  }

  // ===============================
  // Criar Departamento
  // ===============================
  async function handleCreate(data) {
    const payload = {
      name: data.departmentName,
      companyID: "c972a771-0718-4c75-bddf-dfa605b7b93d",
      directorID: data.directorID, // ✅ Agora enviando diretor
    };

    console.log(payload);
    await fetch("http://localhost:8000/department", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    const response = await fetch(`http://localhost:8000/getAllDepartments`);
    const updated = await response.json();

    setAllDepartments(updated.data);
    setDataToShowOnTable(updated.data);
  }

  return (
    <div className={styles.container} style={{ width: "100vw" }}>
      <h1>Empresa</h1>

      <div className={styles.inputContainer}>
        <Input
          onInputChange={setSearchedDepartment}
          placeHolder={"Digite o nome do departamento"}
        />

        {/* Botão + */}
        <button
          className={styles.iconButton}
          onClick={() => setOpenCreateModal(true)}
        >
          <img src={plusCircle} alt="Plus Circle" />
        </button>
      </div>

      {!dataToShowOnTable.length ? (
        "Nenhum departamento encontrado"
      ) : (
        <CommonPageTable
          name="Departamentos da empresa"
          data={dataToShowOnTable}
          type={"departments"}
          hasEditFunction={false}
          hasDeleteFunction={true}
          setOnDelete={handleDeleteFunction}
        />
      )}

      {/* Modal de criação */}
      <CreateModal
        open={openCreateModal}
        onOpenChange={setOpenCreateModal}
        title="Criar departamento"
        onCreate={handleCreate}
        fields={[
          {
            tipo: "text",
            nome: "departmentName",
            label: "Nome do departamento",
          },
          {
            tipo: "select",
            nome: "directorID",
            label: "Diretor responsável",
            options: directorOptions,
          },
        ]}
      />
    </div>
  );
}
