import { useEffect, useState } from "react";
import { CommonPageTable, Input } from "../../components";
import styles from "./Employees.module.css";
import plusCircle from "../../assets/Plus-circle.svg";
import CreateModal from "../../components/CreateModal/CreateModal";

export default function Employees() {
  const [dataToShowOnTable, setDataToShowOnTable] = useState("");
  const [searchedEmployee, setSearchedEmployee] = useState("");
  const [openCreateModal, setOpenCreateModal] = useState(false);

  const [departmentOptions, setDepartmentOptions] = useState([]);
  const [teamOptions, setTeamOptions] = useState([]);
  const [selectedDepartment, setSelectedDepartment] = useState(null); // 👈 novo

  useEffect(() => {
    async function fetchData() {
      const employeesResponse = await fetch(
        "http://localhost:8000/getAllEmployees"
      );
      const employeesData = await employeesResponse.json();
      setDataToShowOnTable(employeesData.data);

      const departmentsResponse = await fetch(
        "http://localhost:8000/getAllDepartments"
      );
      const departmentsData = await departmentsResponse.json();
      setDepartmentOptions(departmentsData.data);

      const teamsResponse = await fetch("http://localhost:8000/getAllTeams");
      const teamsData = await teamsResponse.json();
      setTeamOptions(teamsData.data);
    }

    fetchData();
  }, []);

  // ===============================
  // Criação de funcionário
  // ===============================
  async function handleCreate(newEmployee) {
    const response = await fetch("http://localhost:8000/employee", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(newEmployee),
    });

    if (response.ok) {
      const updated = await fetch("http://localhost:8000/getAllEmployees");
      const updatedData = await updated.json();
      setDataToShowOnTable(updatedData.data);
    }
  }

  // ===============================
  // Campos do modal
  // ===============================
  let modalFields = [
    { tipo: "text", nome: "employeeName", label: "Nome do funcionário" },
    { tipo: "text", nome: "cpf", label: "CPF" },
    { tipo: "email", nome: "email", label: "E-mail" },
    { tipo: "password", nome: "password", label: "Senha" },
    {
      tipo: "select",
      nome: "departmentID",
      label: "Departamento",
      options: departmentOptions.map((d) => ({
        label: d._name,
        value: d._id,
      })),
      // 👇 interceptamos o onChange do select de departamento
      onChangeCustom: (value) => setSelectedDepartment(value),
    },
    {
      tipo: "select",
      nome: "teamID",
      label: "Equipe",
      options: teamOptions
        .filter(
          (t) =>
            !selectedDepartment || t._Team__departmentID === selectedDepartment
        )
        .map((t) => ({
          label: t._name,
          value: t._id,
        })),
    },
  ];

  return (
    <div className={styles.container} style={{ width: "100vw" }}>
      <h1>Funcionários</h1>

      <div className={styles.inputContainer}>
        <Input
          onInputChange={setSearchedEmployee}
          placeHolder="Digite o nome do funcionário"
        />

        <button
          className={styles.iconButton}
          onClick={() => setOpenCreateModal(true)}
        >
          <img src={plusCircle} alt="Plus Circle" />
        </button>
      </div>

      {dataToShowOnTable && (
        <CommonPageTable
          data={dataToShowOnTable}
          type="employees"
          hasEditFunction={true}
          hasDeleteFunction={true}
          deleteText="Tem certeza que deseja deletar o funcionário?"
          showDepartment={true}
        />
      )}

      <CreateModal
        open={openCreateModal}
        onOpenChange={setOpenCreateModal}
        title="Cadastrar Funcionário"
        onCreate={handleCreate}
        fields={modalFields}
      />
    </div>
  );
}
