import { useEffect, useState } from "react";
import { HomeTable, Select } from "../../components";
import styles from "./Home.module.css";

export default function Home() {
  const [selectedGroupType, setSelectedGroupType] = useState("");
  const [selectedGroup, setSelectedGroup] = useState("");
  const [selectedDataType, setSelectedDataType] = useState("");

  const [groups, setGroups] = useState([]);
  const [tableData, setTableData] = useState([]);

  useEffect(() => {
    setSelectedGroup("");
    setSelectedDataType("");
    setTableData([]);
  }, [selectedGroupType]);

  useEffect(() => {
    async function fetchGroups() {
      if (!selectedGroupType) return;

      const endpoints = {
        company: "/getAllCompanies",
        department: "/getAllDepartments",
        team: "/getAllTeams",
      };

      try {
        const res = await fetch(
          `http://localhost:8000${endpoints[selectedGroupType]}`
        );
        const json = await res.json();

        const normalized = Array.isArray(json.data) ? json.data : [json.data];

        setGroups(normalized);
      } catch (err) {
        console.error("Erro ao buscar grupos:", err);
      }
    }

    fetchGroups();
  }, [selectedGroupType]);

  useEffect(() => {
    async function fetchTable() {
      if (!selectedGroupType || !selectedGroup || !selectedDataType) {
        setTableData([]);
        return;
      }

      try {
        const url = `http://localhost:8000/data/${selectedGroupType}/${selectedGroup}/${selectedDataType}`;
        const response = await fetch(url);
        const json = await response.json();
        const normalized = Array.isArray(json.data) ? json.data : [json.data];

        setTableData(normalized);
      } catch (err) {
        console.error("Erro ao carregar dados da tabela:", err);
      }
    }

    fetchTable();
  }, [selectedGroupType, selectedGroup, selectedDataType]);

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
    label: item._name,
    value: item._id,
  }));

  function getLabelByValue(value, options) {
    const item = options.find((opt) => opt.value === value);
    return item ? item.label : "";
  }

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
          width={true}
          disabled={!selectedGroupType}
        />

        <Select
          title="Dado"
          options={dataTypeOptions}
          onChange={setSelectedDataType}
          disabled={!selectedGroup}
        />
      </div>

      {selectedGroupType && selectedGroup && selectedDataType ? (
        <HomeTable
          data={tableData}
          type={selectedDataType}
          group={getLabelByValue(selectedGroup, groupOptions)}
          groupType={getLabelByValue(selectedGroupType, groupTypeOptions)}
        />
      ) : (
        <div>Preencha todos os dados para visualizar a tabela</div>
      )}
    </div>
  );
}
