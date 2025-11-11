import styles from "./TableRow.module.css";

export default function TableRow({ data, group, type }) {
  return (
    <tr>
      <td className={styles.tableItem}>
        <div>{data.name || data._description}</div>
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
          <td className={styles.tableItem}>
            <div>{data.prevValue}</div>
          </td>
        </>
      )}
    </tr>
  );
}
