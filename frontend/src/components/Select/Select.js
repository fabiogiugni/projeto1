import styles from "./Select.module.css";

export default function Select({ title, options = [], onChange }) {
  return (
    <div className={styles.selectWrapper}>
      <select
        className={styles.select}
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
