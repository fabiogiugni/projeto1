import styles from "./ManageRPEsTable.module.css";
import TableRow from "./TableRow";

export default function HomeTable({
  data,
  type,
  group,
  groupType,
  deleteText = "Tem certeza que deseja deletar? Os dados não poderão ser recuperados.",
  setOnDelete,
}) {



  return (
    <table className={styles.tableBackground}>
      <tbody>
        <>
          {type === "rpe" || type === "objective" ? (
            <tr>
              <th className={styles.headerTitle}>Descrição</th>
              <th className={styles.headerTitle}>Departamento</th>
              <th className={styles.headerTitle}> </th>
              <th className={styles.headerTitle}> </th>
              <th className={styles.headerTitle}> </th>
            </tr>
          ) : (
            <tr className={styles.title}>
              <th className={styles.headerTitle}>Descrição</th>
              <th className={styles.headerTitle}>Departamento</th>
              <th className={styles.headerTitle}>Valor Atual</th>
              <th className={styles.headerTitle}> </th>
              <th className={styles.headerTitle}> </th>
              <th className={styles.headerTitle}> </th>
            </tr>
          )}

          {data.map((lineData) => (
            <TableRow
              data={lineData}
              group={group}
              type={type}
              key={lineData.id}
              deleteText={deleteText}
              setOnDelete={setOnDelete}
            />
          ))}
        </>
      </tbody>
    </table>
  );
}
