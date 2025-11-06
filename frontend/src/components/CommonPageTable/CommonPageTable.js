import { data } from "react-router-dom";
import styles from "./Table.module.css";
import TableRow from "./TableRow";

export default function CommonPageTable({
  data,
  type,
  hasEditFunction,
  hasDeleteFunction,
  name = "Nome",
  deleteText = "Tem certeza que deseja deletar? Os dados não poderão ser recuperados.",
}) {
  console.log(data);
  return (
    <table className={styles.tableBackground}>
      <tbody>
        <tr>
          <th className={styles.headerTitle}>{name}</th>
          {hasEditFunction && <th className={styles.headerTitle}> </th>}
          {hasDeleteFunction && <th className={styles.headerTitle}> </th>}
        </tr>

        {data.map((lineData) => (
          <>
            <TableRow
              key={lineData._id}
              data={lineData}
              hasEditFunction={hasEditFunction}
              hasDeleteFunction={hasDeleteFunction}
              deleteText={deleteText}
            />
          </>
        ))}
      </tbody>
    </table>
  );
}
