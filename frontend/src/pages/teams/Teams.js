import { useEffect, useState } from "react";
import { CommonPageTable, Input, Select } from "../../components";
import styles from "./Teams.module.css";
import plusCircle from "../../assets/Plus-circle.svg";

export default function Teams() {
  const [selectedTeam, setSelectedTeam] = useState("");
  const [searchedEmployee, setSearchedEmployee] = useState("");
  const [teamOptions, setTeamOptions] = useState("");
  const [dataToShowOnTable, setDataToShowOnTable] = useState("");

  useEffect(() => {
    async function fetchTeams() {
      const response = await fetch(`http://localhost:8000/getAllTeams`);

      const data = await response.json();
      setTeamOptions(data.data);
    }

    fetchTeams();
  }, []);

  useEffect(() => {
    async function fetchUsers() {
      if (selectedTeam) {
        const response = await fetch(
          `http://localhost:8000/team_users/${selectedTeam}`
        );
        const data = await response.json();
        setDataToShowOnTable(data.data);
        console.log(data);
      }
    }

    fetchUsers();
  }, [selectedTeam]);

  return (
    <div className={styles.container} style={{ width: "100vw" }}>
      <h1>Times do departamento</h1>

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

        <button className={styles.iconButton}>
          <img src={plusCircle} alt="Plus Circle" />
        </button>
      </div>
      {!dataToShowOnTable ? (
        "Escolha uma equipe para ver a tabela "
      ) : (
        <CommonPageTable
          name="Funcionários da equipe"
          data={dataToShowOnTable}
          type={"teams"}
          hasEditFunction={true}
          hasDeleteFunction={true}
        />
      )}
    </div>
  );
}
