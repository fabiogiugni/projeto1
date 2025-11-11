import { useEffect, useState } from "react";
import { ManageRPEsTable, Select, CreateDataModal, } from "../../components";
import styles from "./RPE.module.css";
import plusCircle from "../../assets/Plus-circle.svg";

export default function RPE() {
  const [isCreateModalOpen, setCreateModalOpen] = useState(false);
  const [selectedGroupType, setSelectedGroupType] = useState("");
  const [selectedGroup, setSelectedGroup] = useState("");
  const [selectedDataType, setSelectedDataType] = useState("");

  const [groupOptions, setGroupOptions] = useState([]);
  const [dataToShowOnTable, setDataToShowOnTable] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

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



  // 1️⃣ Buscar opções do grupo (empresas, departamentos, equipes)
  useEffect(() => {
    async function fetchGroups() {
      if (!selectedGroupType) return;

      let endpoint = "";
      if (selectedGroupType === "company") endpoint = "getAllCompanies";
      else if (selectedGroupType === "department") endpoint = "getAllDepartments";
      else if (selectedGroupType === "team") endpoint = "getAllTeams";

      try {
        const res = await fetch(`http://localhost:8000/${endpoint}`);
        const data = await res.json();
        const formatted = data.data.map((item) => ({
          label: item._name || item.name,
          value: item._id || item.id,
        }));
        setGroupOptions(formatted);
      } catch (err) {
        console.error("Erro ao buscar grupos:", err);
      }
    }

    fetchGroups();
  }, [selectedGroupType]);

  // 2️⃣ Buscar RPEs, Objectives, KRs ou KPIs de acordo com o grupo selecionado
  useEffect(() => {
    async function fetchData() {
      if (!selectedDataType || !selectedGroupType || !selectedGroup) return;

      setIsLoading(true);
      try {
        // Determina o endpoint base do grupo
        const groupEndpoints = {
          company: "company",
          department: "department",
          team: "team",
        };

        const groupUrl = `http://localhost:8000/${groupEndpoints[selectedGroupType]}/${selectedGroup}`;
        const groupResponse = await fetch(groupUrl);
        const groupData = await groupResponse.json();

        // Extrai o array de IDs conforme o tipo selecionado
        const groupInfo = groupData.data;
        let ids = [];

        if (selectedDataType === "rpe") ids = groupInfo.rpeIds || [];
        else if (selectedDataType === "objective") ids = groupInfo.objectiveIds || [];
        else if (selectedDataType === "kr") ids = groupInfo.krIds || [];
        else if (selectedDataType === "kpi") ids = groupInfo.kpiIds || [];

        if (!ids.length) {
          setDataToShowOnTable([]);
          setIsLoading(false);
          return;
        }

        // Busca todos os objetos correspondentes
        const fetchPromises = ids.map(async (id) => {
          const res = await fetch(`http://localhost:8000/${selectedDataType}/${id}`);
          const itemData = await res.json();
          return itemData.data;
        });

        const results = await Promise.all(fetchPromises);
        setDataToShowOnTable(results);
      } catch (err) {
        console.error("Erro ao buscar dados:", err);
      } finally {
        setIsLoading(false);
      }
    }

    fetchData();
  }, [selectedDataType, selectedGroup, selectedGroupType]);

  const reloadData = () => {
    setSelectedDataType((prev) => prev); // força re-render da useEffect
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
        />
        <Select
          title="Dado"
          options={dataTypeOptions}
          onChange={setSelectedDataType}
        />

        <button className={styles.iconButton} onClick={() => setCreateModalOpen(true)}>
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
      ) : selectedDataType && selectedGroupType && selectedGroup ? (
        <ManageRPEsTable
          data={dataToShowOnTable}
          type={selectedDataType}
          group={selectedGroup}
          groupType={selectedGroupType}
        />
      ) : (
        <div>Preencha todos os campos para visualizar a tabela</div>
      )}
    </div>
  );
}
