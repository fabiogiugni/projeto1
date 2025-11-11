import { useState, useEffect } from "react";
import styles from "./CreateDataModal.module.css";

export default function CreateDataModal({
  open,
  onClose,
  selectedGroupType,
  selectedGroup,
  selectedDataType,
  onCreated, // callback para atualizar a tabela após criação
}) {
  const [description, setDescription] = useState("");
  const [responsibleID, setResponsibleID] = useState("");
  const [employees, setEmployees] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  // Buscar usuários relacionados ao grupo selecionado
  useEffect(() => {
    async function fetchUsers() {
      if (!selectedGroupType || !selectedGroup) return;

      let endpoint = "";
      if (selectedGroupType === "company") endpoint = `getAllEmployees/${selectedGroup}`;
      else if (selectedGroupType === "department")
        endpoint = `department_users/${selectedGroup}`;
      else if (selectedGroupType === "team")
        endpoint = `team_users/${selectedGroup}`;

      try {
        const res = await fetch(`http://localhost:8000/${endpoint}`);
        const data = await res.json();
        setEmployees(data.data || []);
      } catch (err) {
        console.error("Erro ao buscar usuários:", err);
      }
    }

    fetchUsers();
  }, [selectedGroupType, selectedGroup]);

  async function handleSubmit(e) {
    e.preventDefault();

    if (!description || !responsibleID) {
      alert("Preencha todos os campos obrigatórios.");
      return;
    }

    setIsLoading(true);
    try {
      const endpoints = {
        rpe: "RPE",
        objective: "objective",
        kr: "KR",
        kpi: "KPI",
      };

      const url = `http://localhost:8000/${endpoints[selectedDataType]}`;
      const body = {
        description,
        responsibleID,
      };

      // Cria o item
      const res = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });

      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Erro ao criar item.");

      // Se for RPE, adiciona ao grupo correspondente
      if (selectedDataType === "rpe" && selectedGroupType && selectedGroup) {
        let addEndpoint = "";
        console.log(data)

        if (selectedGroupType === "company")
          addEndpoint = `addCompanyRPE/${selectedGroup}/${data.id}`;
        else if (selectedGroupType === "department")
          addEndpoint = `addDepartmentRPE/${selectedGroup}/${data.id}`;
        else if (selectedGroupType === "team")
          addEndpoint = `addTeamRPE/${selectedGroup}/${data.id}`;

        if (addEndpoint) {
          const addRes = await fetch(`http://localhost:8000/${addEndpoint}`, {
            method: "PUT",
          });
          const addData = await addRes.json();
          if (!addRes.ok)
            throw new Error(addData.detail || "Erro ao adicionar RPE ao grupo.");
        }
      }

      alert(`${selectedDataType.toUpperCase()} criado com sucesso!`);
      onCreated(); // atualiza a tabela
      onClose();
    } catch (err) {
      console.error(err);
      alert(err.message || "Erro ao criar item.");
    } finally {
      setIsLoading(false);
    }
  }

  if (!open) return null;

  return (
    <div className={styles.overlay}>
      <div className={styles.modal}>
        <h2>
          Criar novo {selectedDataType?.toUpperCase()} para{" "}
          {selectedGroupType?.toUpperCase()}
        </h2>
        <form onSubmit={handleSubmit} className={styles.form}>
          <label>
            Descrição:
            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Descreva o objetivo, RPE, KR ou KPI..."
              required
            />
          </label>

          <label>
            Responsável:
            <select
              value={responsibleID}
              onChange={(e) => setResponsibleID(e.target.value)}
              required
            >
              <option value="">Selecione o responsável</option>
              {employees.map((emp) => (
                <option key={emp.id || emp._id} value={emp.id || emp._id}>
                  {emp.name || emp._name}
                </option>
              ))}
            </select>
          </label>

          <div className={styles.actions}>
            <button type="button" onClick={onClose} className={styles.cancelBtn}>
              Cancelar
            </button>
            <button type="submit" disabled={isLoading} className={styles.confirmBtn}>
              {isLoading ? "Criando..." : "Criar"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
