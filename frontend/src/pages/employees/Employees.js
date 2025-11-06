import { useEffect, useState } from "react";
import { CommonPageTable, Input, Select } from "../../components";
import styles from "./Employees.module.css";
import plusCircle from "../../assets/Plus-circle.svg";

import { persons, departments } from "../../assets/testValues";

export default function Employees() {
  const [dataToShowOnTable, setDataToShowOnTable] = useState("");
  const [searchedEmployee, setSearchedEmployee] = useState("");

  useEffect(() => {
    async function fetchUsers() {
      const response = await fetch(`http://localhost:8000/getAllEmployees`);
      const data = await response.json();
      setDataToShowOnTable(data.data);
    }

    fetchUsers();
  }, []);

  return (
    <div className={styles.container} style={{ width: "100vw" }}>
      <h1>Funcionários</h1>

      <div className={styles.inputContainer}>
        <Input
          onInputChange={setSearchedEmployee}
          placeHolder={"Digite o nome do funcionário"}
        />

        <button className={styles.iconButton}>
          <img src={plusCircle} alt="Plus Circle" />
        </button>
      </div>
      {dataToShowOnTable && (
        <CommonPageTable
          data={dataToShowOnTable}
          type={"employees"}
          hasEditFunction={true}
          hasDeleteFunction={true}
          deleteText="Tem certeza que deseja deletar o funciário?"
          showDepartment={true}
        />
      )}
    </div>
  );
}
