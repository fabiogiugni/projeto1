import styles from "./TableRow.module.css";

export default function TableRow({ field, value }) {
  return (
    <tr>
      <td className={styles.tableItem}>
        <div className={styles.field}>{field}</div>
        <div className={styles.description}>{value}</div>
      </td>
    </tr>
  );
}
