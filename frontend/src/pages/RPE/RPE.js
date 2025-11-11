import { useEffect, useState } from "react";
import { ManageRPEsTable, Select, CreateDataModal } from "../../components";
import styles from "./RPE.module.css";
import plusCircle from "../../assets/Plus-circle.svg";

export default function RPE() {
  const [isCreateModalOpen, setCreateModalOpen] = useState(false);
  const [selectedGroupType, setSelectedGroupType] = useState("");
  const [selectedGroup, setSelectedGroup] = useState("");
  const [selectedDataType, setSelectedDataType] = useState("");

  const [groups, setGroups] = useState([]);
  const [tableData, setTableData] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  // opções
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

  // resetar selects ao mudar tipo de grupo
  useEffect(() => {
    setSelectedGroup("");
    setSelectedDataType("");
    setTableData([]);
  }, [selectedGroupType]);

  // buscar grupos
  useEffect(() => {
    async function fetchGroups() {
      if (!selectedGroupType) return;

      const endpoints = {
        company: "/getAllCompanies",
        department: "/getAllDepartments",
        team: "/getAllTeams",
      };

      try {
        const res = await fetch(`http://localhost:8000${endpoints[selectedGroupType]}`);
        const json = await res.json();
        const normalized = Array.isArray(json.data) ? json.data : [json.data];
        setGroups(normalized);
      } catch (err) {
        console.error("Erro ao buscar grupos:", err);
      }
    }

    fetchGroups();
  }, [selectedGroupType]);

  // 👉 função reutilizável para buscar dados da tabela
  async function fetchTable() {
    if (!selectedGroupType || !selectedGroup || !selectedDataType) {
      setTableData([]);
      return;
    }

    setIsLoading(true);
    try {
      const url = `http://localhost:8000/data/${selectedGroupType}/${selectedGroup}/${selectedDataType}`;
      const response = await fetch(url);
      const json = await response.json();

      const normalized = Array.isArray(json.data) ? json.data : [json.data];
      const dataWithIds = normalized.map((item) => ({
        ...item,
        id: item._id || item.id || "",
      }));

      setTableData(dataWithIds);
    } catch (err) {
      console.error("Erro ao carregar dados da tabela:", err);
    } finally {
      setIsLoading(false);
    }
  }

  // atualizar dados quando selects mudam
  useEffect(() => {
    fetchTable();
  }, [selectedGroupType, selectedGroup, selectedDataType]);

  // recarregar manualmente após criar algo
  const reloadData = () => {
    fetchTable();
  };

  const groupOptions = groups.map((item) => ({
    label: item._name || item.name,
    value: item._id || item.id,
  }));

  const getLabelByValue = (value, options) => {
    const found = options.find((opt) => opt.value === value);
    return found ? found.label : "";
  };

  return (
    <div className={styles.container} style={{ width: "100vw" }}>
      <h1>Gerenciar RPEs</h1>

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
          disabled={!selectedGroupType}
        />

        <Select
          title="Dado"
          options={dataTypeOptions}
          onChange={setSelectedDataType}
          disabled={!selectedGroup}
        />

        <button className={styles.iconButton} onClick={() => {setCreateModalOpen(true); fetchTable();}}>
          <img src={plusCircle} alt="Plus Circle" />
        </button>
      </div>

      <CreateDataModal
        open={isCreateModalOpen}
        onClose={() => setCreateModalOpen(false)}
        selectedGroupType={selectedGroupType}
        selectedGroup={selectedGroup}
        selectedDataType={selectedDataType}
        onCreated={reloadData}
      />

      {isLoading ? (
        <div>Carregando dados...</div>
      ) : selectedGroupType && selectedGroup && selectedDataType ? (
        <ManageRPEsTable
          data={tableData}
          type={selectedDataType}
          group={getLabelByValue(selectedGroup, groupOptions)}
          groupType={getLabelByValue(selectedGroupType, groupTypeOptions)}
          setOnDelete={fetchTable}
        />
      ) : (
        <div>Preencha todos os campos para visualizar a tabela</div>
      )}
    </div>
  );
}
