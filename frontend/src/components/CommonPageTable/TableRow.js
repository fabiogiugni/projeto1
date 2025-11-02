import styles from "./TableRow.module.css";
import EditButton from "../../assets/Edit.svg";
import DeleteButton from "../../assets/Delete.svg";

export default function TableRow({ data, hasEditFunction, hasDeleteFunction }) {
  console.log(hasEditFunction);
  return (
    <tr>
      <td className={styles.tableItem}>
        <div>{data.name}</div>
        {data.description && (
          <div className={styles.description}>{data.description}</div>
        )}
      </td>
      <td className={`${styles.tableItem} ${styles.actionCell}`}>
        <div className={styles.actionButtons}>
          {hasEditFunction && (
            <button className={styles.iconButton}>
              <img src={EditButton} alt="Edit Icon" />
            </button>
          )}
        </div>
      </td>
      <td className={`${styles.tableItem} ${styles.actionCell}`}>
        <div className={styles.actionButtons}>
          {hasDeleteFunction && (
            <button className={styles.iconButton}>
              <img src={DeleteButton} alt="Delete Icon" />
            </button>
          )}
        </div>
      </td>
    </tr>
  );
}
