import { useState } from "react";
import { Select, Table } from "../../components";
import styles from "./Home.module.css";

export default function Home() {
  const [selectedType, setSelectedType] = useState("");
  const [selectedData, setSelectedData] = useState("");

  const typeOptions = [
    { label: "Financeiro", value: "financeiro" },
    { label: "Operacional", value: "operacional" },
    { label: "Comercial", value: "comercial" },
  ];

  const dataOptions = [
    { label: "Lucro", value: "lucro" },
    { label: "Crescimento", value: "crescimento" },
    { label: "Desempenho", value: "desempenho" },
  ];

  return (
    <div className={styles.container} style={{ width: "100vw" }}>
      <h1>Home</h1>

      <div className={styles.selectContainer}>
        <Select
          title="Tipo Dado"
          options={typeOptions}
          onChange={setSelectedType}
        />
        <Select title="Dado" options={dataOptions} onChange={setSelectedData} />
      </div>
    </div>
  );
}
