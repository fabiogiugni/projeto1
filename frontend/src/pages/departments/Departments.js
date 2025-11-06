import { useEffect, useState } from "react";
import { CommonPageTable, Input, Select } from "../../components";
import styles from "./Departments.module.css";
import plusCircle from "../../assets/Plus-circle.svg";

import { teams, departments } from "../../assets/testValues";

export default function Departments() {
  const [selectedDepartment, setSelectedDepartment] = useState("");
  const [searchedTeam, setSearchedTeam] = useState("");
  const [departamentOptions, setDepartamentOptions] = useState("");

  useEffect(() => {
    async function fetchDepartaments() {
      const response = await fetch(`http://localhost:8000/getAllDepartments`);

      const data = await response.json();
      console.log(data.data);
      setDepartamentOptions(data.data);
    }

    fetchDepartaments();
  }, []);

  let dataToShowOnTable = teams;

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

        <button className={styles.iconButton}>
          <img src={plusCircle} alt="Plus Circle" />
        </button>
      </div>
      {!selectedDepartment ? (
        "Escolha um departamento para ver a tabela"
      ) : (
        <CommonPageTable
          data={dataToShowOnTable}
          type={"teams"}
          hasEditFunction={true}
          hasDeleteFunction={true}
        />
      )}
    </div>
  );
}
