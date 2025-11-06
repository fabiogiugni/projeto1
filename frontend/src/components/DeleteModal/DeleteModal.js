import * as Dialog from "@radix-ui/react-dialog";
import styles from "./DeleteModal.module.css";
import Button from "../Button/Button";
import CancelButton from "../../assets/X.svg";

export default function DeleteModal({ open, onOpenChange, onDelete, text }) {
  return (
    <Dialog.Root open={open} onOpenChange={onOpenChange}>
      <Dialog.Portal>
        <Dialog.Overlay className={styles.overlay} />

        <Dialog.Content className={styles.content}>
          <div className={styles.header}>
            <Dialog.Title className={styles.title}>Confirmar</Dialog.Title>
            <Dialog.Close asChild>
              <button className={styles.closeButton}>
                <img
                  src={CancelButton}
                  alt="Delete Icon"
                  className={styles.cancelIcon}
                />
              </button>
            </Dialog.Close>
          </div>

          <div className={styles.text}>{text}</div>

          <div className={styles.actions}>
            <Dialog.Close asChild>
              <Button className={styles.cancelButton} text="Cancelar" />
            </Dialog.Close>
            <Button
              className={styles.deleteButton}
              onClick={() => {
                onDelete();
                onOpenChange(false);
              }}
              text="Apagar"
              variant="red"
              style={{}}
            />
          </div>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
}
