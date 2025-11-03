import { useState } from "react";
import { CommonPageTable, Input, Select } from "../../components";
import styles from "./Teams.module.css";
import plusCircle from "../../assets/Plus-circle.svg";

import { teams, departments } from "../../assets/testValues";

export default function Teams() {
  const [selectedDepartment, setSelectedDepartment] = useState("");
  const [searchedTeam, setSearchedTeam] = useState("");

  const departmentOptions = departments.map((department) => ({
    label: department.name,
    value: department.id,
  }));

  console.log(searchedTeam);
  /* espaço destinado a chamar a função do backend */
  let dataToShowOnTable = teams;

  return (
    <div className={styles.container} style={{ width: "100vw" }}>
      <h1>Equipes</h1>

      <div className={styles.inputContainer}>
        <Input
          onInputChange={setSearchedTeam}
          placeHolder={"Digite o nome da equipe"}
        />

        <Select
          title="Departamento"
          options={departmentOptions}
          onChange={setSelectedDepartment}
        />

        <button className={styles.iconButton}>
          <img src={plusCircle} alt="Plus Circle" />
        </button>
      </div>

      <CommonPageTable
        data={dataToShowOnTable}
        type={"teams"}
        hasEditFunction={true}
        hasDeleteFunction={true}
      />
    </div>
  );
}
