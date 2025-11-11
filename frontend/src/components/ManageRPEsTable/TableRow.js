import { useState } from "react";

import styles from "./TableRow.module.css";
import EditButton from "../../assets/Edit.svg";
import DeleteButton from "../../assets/Delete.svg";
import UploadButton from "../../assets/Folder.svg";
import { DeleteModal } from "../";

export default function TableRow({ data, group, type, deleteText, setOnDelete }) {
  const [isDeleteModalOpen, setDeleteModalOpen] = useState(false);
  

  async function handleDelete() {
    console.log(data)
    if (!data.id) return;

    const endpoints = {
      rpe: `http://localhost:8000/rpe/${data.id}`,
      kr: `http://localhost:8000/kr/${data.id}`,
      kpi: `http://localhost:8000/kpi/${data.id}`,
      objective: `http://localhost:8000/objective/${data.id}`,
    };

    const url = endpoints[type];
    console.log(data)

    if (!url) {
      console.error("DELETE endpoint not implemented for type:", type);
      return;
    }

    await fetch(url, { method: "DELETE" });

    

    setDeleteModalOpen(false);
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
