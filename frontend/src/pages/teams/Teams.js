import { useEffect, useState } from "react";
import { CommonPageTable, Input, Select, CreateModal } from "../../components";
import styles from "./Teams.module.css";
import plusCircle from "../../assets/Plus-circle.svg";

export default function Teams() {
  const [selectedTeam, setSelectedTeam] = useState("");
  const [searchedEmployee, setSearchedEmployee] = useState("");
  const [teamOptions, setTeamOptions] = useState([]);
  const [employeeOptions, setEmployeeOptions] = useState([]);
  const [dataToShowOnTable, setDataToShowOnTable] = useState([]);
  const [allEmployees, setAllEmployees] = useState([]);
  const [openCreateModal, setOpenCreateModal] = useState(false);

  // Carregar todas as equipes
  useEffect(() => {
    async function fetchTeams() {
      const response = await fetch(`http://localhost:8000/getAllTeams`);
      const data = await response.json();
      setTeamOptions(data.data);
    }
    fetchTeams();
  }, []);

  // Carregar todos os funcionários
  useEffect(() => {
    async function fetchEmployees() {
      const response = await fetch(`http://localhost:8000/getAllEmployees`);
      const data = await response.json();
      setEmployeeOptions(data.data);
    }
    fetchEmployees();
  }, []);

  // Filtrar funcionários pelo nome digitado
  useEffect(() => {
    if (searchedEmployee && allEmployees.length > 0) {
      const filtered = allEmployees.filter((emp) =>
        emp._name.toLowerCase().includes(searchedEmployee.toLowerCase())
      );
      setDataToShowOnTable(filtered);
    } else {
      setDataToShowOnTable(allEmployees);
    }
  }, [searchedEmployee]);

  // Buscar funcionários da equipe selecionada
  useEffect(() => {
    async function fetchUsers() {
      if (selectedTeam) {
        const response = await fetch(
          `http://localhost:8000/team_users/${selectedTeam}`
        );
        const data = await response.json();
        setDataToShowOnTable(data.data);
        setAllEmployees(data.data);
      }
    }
    fetchUsers();
  }, [selectedTeam]);

  // Criar (adicionar funcionário à equipe)
  async function handleCreate(data) {
    const payload = {
      userID: data.employeeID,
      teamID: data.teamID,
    };

    // Aqui você deve criar um endpoint no backend tipo: PUT /user_team/{userID}/{teamID}
    // Exemplo de chamada:
    await fetch(
      `http://localhost:8000/user_team/${payload.userID}/${payload.teamID}`,
      { method: "PUT" }
    );

    const response = await fetch(
      `http://localhost:8000/team_users/${payload.teamID}`
    );
    const tableUpdated = await response.json();
    setDataToShowOnTable(tableUpdated.data);
    setAllEmployees(tableUpdated.data);
  }

  // Atualizar a tabela após deletar alguém
  async function handleDeleteFunction() {
    if (!selectedTeam) return;

    const response = await fetch(
      `http://localhost:8000/team_users/${selectedTeam}`
    );
    const updated = await response.json();
    setDataToShowOnTable(updated.data);
    setAllEmployees(updated.data);
  }

  return (
    <div className={styles.container} style={{ width: "100vw" }}>
      <h1>Equipes</h1>

      <div className={styles.inputContainer}>
        <Input
          onInputChange={setSearchedEmployee}
          placeHolder={"Digite o nome do funcionário"}
        />

        {teamOptions && (
          <Select
            title="Equipe"
            options={teamOptions.map((team) => ({
              label: team._name,
              value: team._id,
            }))}
            onChange={setSelectedTeam}
          />
        )}

        <button
          className={styles.iconButton}
          onClick={() => setOpenCreateModal(true)}
        >
          <img src={plusCircle} alt="Plus Circle" />
        </button>
      </div>

      {!dataToShowOnTable || dataToShowOnTable.length === 0 ? (
        "Escolha uma equipe para ver os funcionários"
      ) : (
        <CommonPageTable
          name="Funcionários da equipe"
          data={dataToShowOnTable}
          type={"employees"}
          hasEditFunction={true}
          hasDeleteFunction={true}
          setOnDelete={handleDeleteFunction}
        />
      )}

      {teamOptions && (
        <CreateModal
          open={openCreateModal}
          onOpenChange={setOpenCreateModal}
          title="Adicionar funcionário à equipe"
          onCreate={handleCreate}
          fields={[
            {
              tipo: "select",
              nome: "teamID",
              label: "Equipe",
              options: teamOptions.map((item) => ({
                label: item._name,
                value: item._id,
              })),
            },
            {
              tipo: "select",
              nome: "employeeID",
              label: "Funcionário",
              options: employeeOptions.map((u) => ({
                label: u._name,
                value: u._id,
              })),
            },
          ]}
        />
      )}
    </div>
  );
}
