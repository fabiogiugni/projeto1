import { useEffect, useState } from "react";
import { CommonPageTable, Input, Select } from "../../components";
import styles from "./Company.module.css";

export default function Company() {
  const [searchedDepartment, setSearchedDepartment] = useState("");
  const [dataToShowOnTable, setDataToShowOnTable] = useState("");

  useEffect(() => {
    async function fetchDepartaments() {
      const response = await fetch(`http://localhost:8000/getAllDepartments`);
      const data = await response.json();
      setDataToShowOnTable(data.data);
    }

    fetchDepartaments();
  }, []);

  return (
    <div className={styles.container} style={{ width: "100vw" }}>
      <h1>Empresa</h1>

      <div className={styles.inputContainer}>
        <Input
          onInputChange={setSearchedDepartment}
          placeHolder={"Digite o nome do departamento"}
        />
      </div>
      {!dataToShowOnTable ? (
        "Escolha uma empresa para ver a tabela"
      ) : (
        <CommonPageTable
          name="Departamentos da empresa"
          data={dataToShowOnTable}
          type={"teams"}
          hasEditFunction={false}
          hasDeleteFunction={true}
        />
      )}
    </div>
  );
}
