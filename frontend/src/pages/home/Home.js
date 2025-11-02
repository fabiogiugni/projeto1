import { useState } from "react";
import { HomeTable, Select } from "../../components";
import styles from "./Home.module.css";

import {
  companies,
  departments,
  teams,
  rpes,
  objectives,
  krs,
  kpis,
} from "../../assets/testValues";

export default function Home() {
  // Para o funcionamento da página, temos 2 inputs
  // Um é o input de grupo que filtra por rpes, objetivo, etc. e o outro é o de dado, que filtra por empresa, departamento, etc
  // Enquanto algum dos filtros estiver vazio, o backend não é chamado para puxar os dados

  const [selectedGroupType, setSelectedGroupType] = useState("");
  const [selectedGroup, setSelectedGroup] = useState("");
  const [selectedDataType, setSelectedDataType] = useState("");

  const groupTypeOptions = [
    { label: "Empresa", value: "company" },
    { label: "Departamento", value: "department" },
    { label: "Equipe", value: "team" },
  ];

  const dataTypeOptions = [
    { label: "RPE", value: "rpe" },
    { label: "Objetivo", value: "objective" },
    { label: "KR", value: "kr" },
    { label: "KPI", value: "kpi" },
  ];

  let groupOptions = [];
  if (selectedGroupType === "company")
    groupOptions = companies.map((company) => ({
      label: company.name,
      value: company.id,
    }));
  if (selectedGroupType === "department")
    groupOptions = departments.map((department) => ({
      label: department.name,
      value: department.id,
    }));
  if (selectedGroupType === "team")
    groupOptions = teams.map((team) => ({ label: team.name, value: team.id }));

  /* espaço destinado a chamar a função do backend */
  let dataToShowOnTable = [];
  if (selectedDataType === "RPE") dataToShowOnTable = rpes;
  else if (selectedDataType === "objective") dataToShowOnTable = objectives;
  else if (selectedDataType === "kr") dataToShowOnTable = krs;
  else dataToShowOnTable = kpis;

  return (
    <div className={styles.container} style={{ width: "100vw" }}>
      <h1>Home</h1>

      <div className={styles.selectContainer}>
        <Select
          title="Tipo Grupo"
          options={groupTypeOptions}
          onChange={setSelectedGroupType}
        />
        <Select
          title="Grupo"
          options={groupOptions}
          onChange={setSelectedGroup}
        />
        <Select
          title="Dado"
          options={dataTypeOptions}
          onChange={setSelectedDataType}
        />
      </div>
      {selectedDataType && selectedGroupType && selectedGroup ? (
        <HomeTable
          data={dataToShowOnTable}
          type={selectedDataType}
          group={selectedGroup}
          groupType={selectedGroupType}
        />
      ) : (
        <div>Preencha todos os dados visualizar a tabela</div>
      )}
    </div>
  );
}
