import styles from "./Input.module.css";

export default function Input({ onInputChange, placeHolder, type, error }) {
  const inputClass = error
    ? `${styles.input} ${styles.error}`
    : `${styles.input}`;
  return (
    <input
      onChange={(e) => onInputChange(e.target.value)}
      className={inputClass}
      placeholder={placeHolder}
      type={type || "input"}
    />
  );
}
