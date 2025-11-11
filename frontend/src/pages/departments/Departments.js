import { useEffect, useState } from "react";
import { CommonPageTable, Input, Select, CreateModal } from "../../components";
import styles from "./Departments.module.css";
import plusCircle from "../../assets/Plus-circle.svg";

export default function Departments() {
  const [selectedDepartment, setSelectedDepartment] = useState("");
  const [searchedTeam, setSearchedTeam] = useState("");
  const [departamentOptions, setDepartamentOptions] = useState("");
  const [dataToShowOnTable, setDataToShowOnTable] = useState("");

  const [openCreateModal, setOpenCreateModal] = useState(false);

  useEffect(() => {
    async function fetchDepartaments() {
      const response = await fetch(`http://localhost:8000/getAllDepartments`);
      const data = await response.json();
      setDepartamentOptions(data.data);
    }

    fetchDepartaments();
  }, []);

  console.log(departamentOptions);

  useEffect(() => {
    async function fetchTeams() {
      if (selectedDepartment) {
        const response = await fetch(
          `http://localhost:8000/department_teams/${selectedDepartment}`
        );
        const data = await response.json();
        setDataToShowOnTable(data.data);
      }
    }

    fetchTeams();
  }, [selectedDepartment]);

  async function handleCreate(data) {
    const payload = {
      name: data.teamName,
      departmentID: data.department,
    };

    console.log(payload);

    // await fetch("http://localhost:8000/team", {
    //   method: "POST",
    //   headers: { "Content-Type": "application/json" },
    //   body: JSON.stringify(payload),
    // });

    // // refresh table
    // const response = await fetch(
    //   `http://localhost:8000/department_teams/${selectedDepartment}`
    // );
    // const tableUpdated = await response.json();
    // setDataToShowOnTable(tableUpdated.data);
  }

  return (
    <div className={styles.container} style={{ width: "100vw" }}>
      <h1>Departamento</h1>

      <div className={styles.inputContainer}>
        <Input
          onInputChange={setSearchedTeam}
          placeHolder={"Digite o nome da equipe"}
        />

        {departamentOptions && (
          <Select
            title="Departamento"
            options={departamentOptions.map((team) => ({
              label: team._name,
              value: team._id,
            }))}
            onChange={setSelectedDepartment}
          />
        )}

        <button
          className={styles.iconButton}
          onClick={() => setOpenCreateModal(true)}
        >
          <img src={plusCircle} alt="Plus Circle" />
        </button>
      </div>

      {!dataToShowOnTable ? (
        "Escolha um departamento para ver a tabela"
      ) : (
        <CommonPageTable
          name="Equipes do departamento"
          data={dataToShowOnTable}
          type={"teams"}
          hasEditFunction={true}
          hasDeleteFunction={true}
        />
      )}

      {departamentOptions && (
        <CreateModal
          open={openCreateModal}
          onOpenChange={setOpenCreateModal}
          title="Criar equipe"
          onCreate={handleCreate}
          fields={[
            { tipo: "text", nome: "teamName", label: "Nome da equipe" },
            {
              tipo: "select",
              nome: "department",
              label: "Departamento",
              options: departamentOptions.map((item) => ({
                label: item._name,
                value: item._id,
              })),
            },
          ]}
        />
      )}
    </div>
  );
}
