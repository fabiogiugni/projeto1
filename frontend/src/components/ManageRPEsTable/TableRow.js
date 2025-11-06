import { useState } from "react";

import styles from "./TableRow.module.css";
import EditButton from "../../assets/Edit.svg";
import DeleteButton from "../../assets/Delete.svg";
import UploadButton from "../../assets/Folder.svg";
import { DeleteModal } from "../";

export default function TableRow({ data, group, type, deleteText }) {
  const [isDeleteModalOpen, setDeleteModalOpen] = useState(false);

  function handleDelete() {
    console.log("Item deleted!");
  }

  return (
    <tr>
      <td className={styles.tableItem}>
        <div>{data.name}</div>
        <div className={styles.description}>{data.description}</div>
      </td>
      <td className={styles.tableItem}>{group}</td>
      {type !== "rpe" && type !== "objective" && (
        <>
          <td
            className={`${styles.tableItem} ${
              data.value < data.goal
                ? styles.badIndicator
                : styles.goodIndicator
            }`}
          >
            <div>{data.value}</div>
            {data.goal && <div>Meta: {data.goal}</div>}
          </td>
        </>
      )}
      <td className={`${styles.tableItem} ${styles.actionCell}`}>
        <div className={styles.actionButtons}>
          <button className={styles.iconButton}>
            <img src={UploadButton} alt="Upload Icon" />
          </button>
        </div>
      </td>
      <td className={`${styles.tableItem} ${styles.actionCell}`}>
        <div className={styles.actionButtons}>
          <button className={styles.iconButton}>
            <img src={EditButton} alt="Edit Icon" />
          </button>
        </div>
      </td>
      <td className={`${styles.tableItem} ${styles.actionCell}`}>
        <div className={styles.actionButtons}>
          <button
            className={styles.iconButton}
            onClick={() => setDeleteModalOpen(true)}
          >
            <img src={DeleteButton} alt="Delete Icon" />
          </button>
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
