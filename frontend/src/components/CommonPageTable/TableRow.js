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
  type,
  setOnDelete,
}) {
  const [isDeleteModalOpen, setDeleteModalOpen] = useState(false);
  const [department, setDepartment] = useState("");

  async function handleDelete() {
    if (!data._id) return;

    const endpoints = {
      teams: `http://localhost:8000/team/${data._id}`,
      employees: `http://localhost:8000/user/${data._id}`,
      departments: `http://localhost:8000/department/${data._id}`,
      company: `http://localhost:8000/company/${data._id}`,
    };

    const url = endpoints[type];

    if (!url) {
      console.error("DELETE endpoint not implemented for type:", type);
      return;
    }

    await fetch(url, { method: "DELETE" });

    setOnDelete();

    setDeleteModalOpen(false);
  }

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
      {showDepartment && department && (
        <td className={styles.tableItem}>{department._name}</td>
      )}
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
