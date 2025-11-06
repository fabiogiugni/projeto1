import { useState } from "react";
import styles from "./TableRow.module.css";
import EditButton from "../../assets/Edit.svg";
import DeleteButton from "../../assets/Delete.svg";
import { DeleteModal } from "../";

export default function TableRow({
  data,
  hasEditFunction,
  hasDeleteFunction,
  deleteText,
}) {
  const [isDeleteModalOpen, setDeleteModalOpen] = useState(false);

  function handleDelete() {
    console.log("Item deleted!");
    // call your backend delete function here
  }

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
            <button
              className={styles.iconButton}
              onClick={() => setDeleteModalOpen(true)}
            >
              <img src={DeleteButton} alt="Delete Icon" />
            </button>
          )}
        </div>
      </td>

      <DeleteModal
        open={isDeleteModalOpen}
        onOpenChange={setDeleteModalOpen}
        onDelete={handleDelete}
        text={deleteText}
      />
    </tr>
  );
}
