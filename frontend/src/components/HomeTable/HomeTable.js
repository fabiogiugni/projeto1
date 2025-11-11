import styles from "./Table.module.css";
import TableRow from "./TableRow";

export default function HomeTable({ data, type, group, groupType }) {
  return (
    <table className={styles.tableBackground}>
      <tbody>
        <>
          {/* Conditional Header Row */}
          {type === "rpe" || type === "objective" ? (
            <tr>
              <th className={styles.headerTitle}>Descrição</th>
              <th className={styles.headerTitle}>{groupType}</th>
            </tr>
          ) : (
            <tr className={styles.title}>
              <th className={styles.headerTitle}>Descrição</th>
              <th className={styles.headerTitle}>{groupType}</th>
              <th className={styles.headerTitle}>Valor Atual</th>
              <th className={styles.headerTitle}>Valor Anterior</th>
            </tr>
          )}

          {/* Mapped Data Rows */}
          {data.map((lineData) => (
            <TableRow
              data={lineData}
              group={group}
              type={type}
              key={lineData.id}
            />
          ))}
        </>
      </tbody>
    </table>
  );
}
