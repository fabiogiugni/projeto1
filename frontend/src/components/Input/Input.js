import styles from "./Input.module.css";

export default function Input({ onInputChange, placeHolder, type }) {
  return (
    <input
      onChange={(e) => onInputChange(e.target.value)}
      className={styles.input}
      placeholder={placeHolder}
      type={type || "input"}
    />
  );
}
