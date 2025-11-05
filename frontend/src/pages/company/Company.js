import { useState } from "react";
import { CommonPageTable, Input, Select } from "../../components";
import styles from "./Company.module.css";

import { companies, departments } from "../../assets/testValues";

export default function Company() {
  const [selectedCompany, setSelectedCompany] = useState("");
  const [searchedDepartment, setSearchedDepartment] = useState("");

  const departmentOptions = companies.map((department) => ({
    label: department.name,
    value: department.id,
  }));

  console.log(searchedDepartment);
  /* espaço destinado a chamar a função do backend */
  let dataToShowOnTable = departments;

  return (
    <div className={styles.container} style={{ width: "100vw" }}>
      <h1>Empresa</h1>

      <div className={styles.inputContainer}>
        <Input
          onInputChange={setSearchedDepartment}
          placeHolder={"Digite o nome do departamento"}
        />

        <Select
          title="Empresa"
          options={departmentOptions}
          onChange={setSelectedCompany}
        />
      </div>
      {!selectedCompany ? (
        "Escolha uma empresa para ver a tabela"
      ) : (
        <CommonPageTable
          data={dataToShowOnTable}
          type={"teams"}
          hasEditFunction={false}
          hasDeleteFunction={true}
        />
      )}
    </div>
  );
}
