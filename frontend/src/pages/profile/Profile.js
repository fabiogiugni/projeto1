import { use, useEffect, useState } from "react";
import { persons } from "../../assets/testValues";
import styles from "./Profile.module.css";
import TableRow from "./TableRow";

export default function Employees() {
  const [department, setDepartment] = useState("");
  const user = JSON.parse(sessionStorage.getItem("user"));
  let dataToShowOnTable = {
    ID: user._id,
    Nome: user._name,
    CPF: user._cpf,
    Cargo: user._role,
    Email: user._Person__email,
    Departamento: department || "TechNova Global",
  };
  useEffect(() => {
    async function fetchdepartment() {
      const response = await fetch(
        `http://localhost:8000/department/${user._departmentID}`
      );
      const jsonResponse = await response.json();
      console.log(user._departmentID);
      setDepartment(jsonResponse.data._name);
    }
    fetchdepartment();
  }, []);

  console.log(department);
  return (
    <div className={styles.container} style={{ width: "100vw" }}>
      <h1>Perfil</h1>
      <table className={styles.tableBackground}>
        <tbody>
          {Object.entries(dataToShowOnTable).map(([key, value]) => {
            if (key !== "id")
              return <TableRow key={key} field={key} value={value} />;
          })}
        </tbody>
      </table>
    </div>
  );
}
