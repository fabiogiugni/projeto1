import { useState } from "react";
import { Input, Button } from "../../components";
import styles from "./Login.module.css";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  function logIn(e) {
    e.preventDefault();
  }

  return (
    <div className={styles.container} style={{ width: "100vw" }}>
      <h1>Login</h1>

      <form className={styles.form} onSubmit={logIn}>
        <Input onInputChange={setEmail} placeHolder="Digite o email" />
        <Input
          onInputChange={setPassword}
          placeHolder="Digite a senha"
          type="password"
        />

        <Button text="Entrar" variant="light" type="submit" />
      </form>
    </div>
  );
}
