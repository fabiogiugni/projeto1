import { persons } from "../../assets/testValues";
import styles from "./Profile.module.css";
import TableRow from "./TableRow";

export default function Employees() {
  let dataToShowOnTable = persons[0];
  // Aqui o backend será chamado

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
