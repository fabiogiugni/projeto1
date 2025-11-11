import * as Dialog from "@radix-ui/react-dialog";
import styles from "./CreateModal.module.css";
import Button from "../Button/Button";
import CancelButton from "../../assets/X.svg";
import { Input, Select } from "../../components";
import { useState, useEffect } from "react";

export default function CreateModal({
  open,
  onOpenChange,
  onCreate,
  fields,
  title = "Criar",
}) {
  // Estado inicial dinâmico baseado nos campos
  const initialState = fields.reduce((acc, field) => {
    acc[field.nome] = "";
    return acc;
  }, {});

  const [formData, setFormData] = useState(initialState);
  const [isValid, setIsValid] = useState(false);

  // Reset quando fecha
  useEffect(() => {
    if (!open) {
      setFormData(initialState);
    }
  }, [open]);

  // Validação automática
  useEffect(() => {
    const everyFieldFilled = Object.values(formData).every(
      (value) => value !== "" && value !== null
    );
    setIsValid(everyFieldFilled);
  }, [formData]);

  function handleChange(name, value) {
    setFormData((prev) => ({ ...prev, [name]: value }));
  }

  function handleSubmit() {
    if (!isValid) return;
    onCreate(formData);
    onOpenChange(false);
  }

  return (
    <Dialog.Root open={open} onOpenChange={onOpenChange}>
      <Dialog.Portal>
        <Dialog.Overlay className={styles.overlay} />

        <Dialog.Content className={styles.content}>
          <div className={styles.header}>
            <Dialog.Title className={styles.title}>{title}</Dialog.Title>

            <Dialog.Close asChild>
              <button className={styles.closeButton}>
                <img
                  src={CancelButton}
                  alt="Close"
                  className={styles.cancelIcon}
                />
              </button>
            </Dialog.Close>
          </div>

          <div className={styles.fieldContainer}>
            {fields.map((field) => (
              <div key={field.nome} className={styles.field}>
                <label className={styles.label}>{field.label}</label>
                <div>
                  {field.tipo === "text" && (
                    <Input
                      placeHolder={field.label}
                      onInputChange={(value) => handleChange(field.nome, value)}
                    />
                  )}

                  {field.tipo === "select" && (
                    <Select
                      title={field.label}
                      options={field.options || []}
                      onChange={(value) => handleChange(field.nome, value)}
                      modal={true}
                    />
                  )}
                </div>
              </div>
            ))}
          </div>

          {!isValid && (
            <div className={styles.errorMessage}>
              Preencha todos os campos para continuar
            </div>
          )}

          <div className={styles.actions}>
            <Dialog.Close asChild>
              <Button className={styles.cancelButton} text="Cancelar" />
            </Dialog.Close>

            <Button
              className={styles.createButton}
              onClick={handleSubmit}
              text="Criar"
              variant="blue"
              disabled={!isValid}
            />
          </div>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
}
