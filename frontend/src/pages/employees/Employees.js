import { useState } from "react";
import { CommonPageTable, Input, Select } from "../../components";
import styles from "./Employees.module.css";
import plusCircle from "../../assets/Plus-circle.svg";

import { persons, departments } from "../../assets/testValues";

export default function Employees() {
  const [selectedDepartment, setSelectedDepartment] = useState("");
  const [searchedEmployee, setSearchedEmployee] = useState("");

  const departmentOptions = departments.map((department) => ({
    label: department.name,
    value: department.id,
  }));

  /* espaço destinado a chamar a função do backend */
  let dataToShowOnTable = persons;

  return (
    <div className={styles.container} style={{ width: "100vw" }}>
      <h1>Funcionários</h1>

      <div className={styles.inputContainer}>
        <Input
          onInputChange={setSearchedEmployee}
          placeHolder={"Digite o nome do funcionário"}
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
        type={"employees"}
        hasEditFunction={true}
        hasDeleteFunction={true}
        deleteText="Tem certeza que deseja deletar o funciário?"
      />
    </div>
  );
}
