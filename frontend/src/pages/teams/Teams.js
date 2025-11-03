import { useState } from "react";
import { CommonPageTable, Input, Select } from "../../components";
import styles from "./Teams.module.css";
import plusCircle from "../../assets/Plus-circle.svg";

import { persons, departments } from "../../assets/testValues";

export default function Teams() {
  const [selectedTeam, setSelectedTeam] = useState("");
  const [searchedEmployee, setSearchedEmployee] = useState("");

  const departmentOptions = departments.map((department) => ({
    label: department.name,
    value: department.id,
  }));

  console.log(searchedEmployee);
  /* espaço destinado a chamar a função do backend */
  let dataToShowOnTable = persons;

  return (
    <div className={styles.container} style={{ width: "100vw" }}>
      <h1>Equipe</h1>

      <div className={styles.inputContainer}>
        <Input
          onInputChange={setSearchedEmployee}
          placeHolder={"Digite o nome do funcionário"}
        />

        <Select
          title="Equipe"
          options={departmentOptions}
          onChange={setSelectedTeam}
        />

        <button className={styles.iconButton}>
          <img src={plusCircle} alt="Plus Circle" />
        </button>
      </div>
      {!selectedTeam ? (
        "Escolha uma equipe para ver a tabela "
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
