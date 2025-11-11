import styles from "./Select.module.css";

export default function Select({
  title,
  options = [],
  onChange,
  width,
  modal,
}) {
  const selectClassName = width
    ? `${styles.select} ${styles.increasedWidth}`
    : modal
    ? `${styles.select} ${styles.modal}`
    : styles.select;

  return (
    <div className={styles.selectWrapper}>
      <select
        className={selectClassName}
        defaultValue=""
        onChange={(e) => onChange(e.target.value)}
      >
        <option value="" disabled>
          {title}
        </option>
        {options.map((e) => (
          <option key={e.value} value={e.value}>
            {e.label}
          </option>
        ))}
      </select>
    </div>
  );
}
