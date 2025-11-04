import styles from "./Table.module.css";
import TableRow from "./TableRow";

export default function CommonPageTable({
  data,
  type,
  hasEditFunction,
  hasDeleteFunction,
  deleteText = "Tem certeza que deseja deletar? Os dados não poderão ser recuperados.",
}) {
  return (
    <table className={styles.tableBackground}>
      <tbody>
        <tr>
          <th className={styles.headerTitle}>Nome</th>
          {hasEditFunction && <th className={styles.headerTitle}> </th>}
          {hasDeleteFunction && <th className={styles.headerTitle}> </th>}
        </tr>

        {data.map((lineData) => (
          <TableRow
            key={data.name}
            data={lineData}
            hasEditFunction={hasEditFunction}
            hasDeleteFunction={hasDeleteFunction}
            deleteText={deleteText}
          />
        ))}
      </tbody>
    </table>
  );
}
