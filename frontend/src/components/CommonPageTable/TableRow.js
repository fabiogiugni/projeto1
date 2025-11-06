import { useEffect, useState } from "react";
import styles from "./TableRow.module.css";
import EditButton from "../../assets/Edit.svg";
import DeleteButton from "../../assets/Delete.svg";
import { DeleteModal } from "../";

export default function TableRow({
  data,
  hasEditFunction,
  hasDeleteFunction,
  deleteText,
  showDepartment,
  handleDelete = () => console.log("Deleted"),
}) {
  const [isDeleteModalOpen, setDeleteModalOpen] = useState(false);
  const [department, setDepartment] = useState("");
  useEffect(() => {
    if (showDepartment) {
      async function fetchdepartment() {
        const response = await fetch(
          `http://localhost:8000/department/${data._departmentID}`
        );
        const jsonResponse = await response.json();
        setDepartment(jsonResponse.data);
      }
      fetchdepartment();
    }
  }, []);
  return (
    <tr>
      <td className={styles.tableItem}>
        <div>{data._name}</div>
        {data._description ||
          (data._role && (
            <div className={styles.description}>
              {data._description || data._role}
            </div>
          ))}
      </td>
      {showDepartment && <td className={styles.tableItem}>{department}</td>}
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
