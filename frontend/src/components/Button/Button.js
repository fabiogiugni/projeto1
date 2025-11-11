import styles from "./Button.module.css";

export default function Button({
  text,
  variant = "dark",
  className = "",
  ...props
}) {
  const buttonClass =
    variant === "light"
      ? `${styles.button} ${styles.light}`
      : variant === "red"
      ? `${styles.button} ${styles.red}`
      : styles.button;

  const finalClassName = `${buttonClass} ${className}`.trim();

  return (
    <button className={finalClassName} {...props}>
      {text}
    </button>
  );
}
