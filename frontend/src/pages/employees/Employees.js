import { useState } from "react";
import { Input, Select } from "../../components";
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

  console.log(searchedEmployee);
  /* espaço destinado a chamar a função do backend */
  let dataToShowOnTable = [];

  return (
    <div className={styles.container} style={{ width: "100vw" }}>
      <h1>Employees</h1>

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

        <button style={{ all: "unset" }}>
          <img src={plusCircle} alt="Plus Circle" />
        </button>
      </div>
      {/* {selectedDataType && selectedGroupType && selectedGroup ? (
        <HomeTable
          data={dataToShowOnTable}
          type={selectedDataType}
          group={selectedGroup}
          groupType={selectedGroupType}
        />
      ) : (
        <div>Preencha todos os dados visualizar a tabela</div>
      )} */}
    </div>
  );
}
