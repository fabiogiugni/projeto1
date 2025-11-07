import { useEffect, useState } from "react";
import { HomeTable, Select } from "../../components";
import styles from "./Home.module.css";

export default function Home() {
  const [selectedGroupType, setSelectedGroupType] = useState("");
  const [groups, setGroups] = useState([]); // <- aqui guarda os grupos vindos do backend
  const [selectedGroup, setSelectedGroup] = useState("");
  const [selectedDataType, setSelectedDataType] = useState("");

  // ================================
  // CHAMAR BACKEND AO MUDAR O TIPO
  // ================================
  useEffect(() => {
    async function fetchGroups() {
      if (!selectedGroupType) {
        setGroups([]);
        return;
      }

      try {
        let url = "";

        if (selectedGroupType === "company") {
          // você *não tem* este endpoint ainda
          // então vou deixar como exemplo
          url = "http://localhost:8000/getAllCompanies";
        }

        if (selectedGroupType === "department") {
          url = "http://localhost:8000/getAllDepartments";
        }

        if (selectedGroupType === "team") {
          url = "http://localhost:8000/getAllTeams";
        }

        const response = await fetch(url);
        const data = await response.json();
        setGroups(data.data);
      } catch (err) {
        console.error("Erro ao buscar grupos", err);
      }
    }

    fetchGroups();
  }, [selectedGroupType]);

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

  const groupOptions = groups.map((item) => ({
    label: item.name,
    value: item.id,
  }));

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
          data={[]}
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
