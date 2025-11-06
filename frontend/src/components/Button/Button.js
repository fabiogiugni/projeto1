import styles from "./Button.module.css";

export default function Button({ text, variant = "dark" }) {
  const buttonClass =
    variant === "light"
      ? `${styles.button} ${styles.light}`
      : variant === "red"
      ? `${styles.button} ${styles.red}`
      : styles.button;

  return <button className={buttonClass}>{text}</button>;
}
