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
  fields, // [{ tipo, nome, label, options? }]
  title = "Criar",
}) {
  const initialState = fields.reduce((acc, field) => {
    acc[field.nome] = "";
    return acc;
  }, {});

  const [formData, setFormData] = useState(initialState);
  const [touchedSubmit, setTouchedSubmit] = useState(false);

  useEffect(() => {
    if (!open) {
      setFormData(initialState);
      setTouchedSubmit(false);
    }
  }, [open]);

  function handleChange(name, value) {
    setFormData((prev) => ({ ...prev, [name]: value }));
  }

  function isFormValid() {
    return Object.values(formData).every(
      (v) => v !== "" && v !== null && v !== undefined
    );
  }

  function handleSubmit() {
    setTouchedSubmit(true);

    if (!isFormValid()) {
      return; // apenas mostra mensagem, sem enviar
    }

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

                {field.tipo === "text" && (
                  <Input
                    placeHolder={field.label}
                    onInputChange={(value) => handleChange(field.nome, value)}
                  />
                )}
                {field.tipo === "email" && (
                  <Input
                    placeHolder={field.label}
                    type="email"
                    onInputChange={(value) => handleChange(field.nome, value)}
                  />
                )}
                {field.tipo === "password" && (
                  <Input
                    placeHolder={field.label}
                    type="password"
                    onInputChange={(value) => handleChange(field.nome, value)}
                  />
                )}
                {field.tipo === "select" && (
                  <Select
                    title={field.label}
                    options={field.options || []}
                    onChange={(value) => {
                      handleChange(field.nome, value);
                      field.onChangeCustom?.(value); // 👈 dispara lógica extra se existir
                    }}
                    modal={true}
                  />
                )}
              </div>
            ))}
          </div>

          {touchedSubmit && !isFormValid() && (
            <div className={styles.errorGlobal}>Preencha todos os campos</div>
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
            />
          </div>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
}
