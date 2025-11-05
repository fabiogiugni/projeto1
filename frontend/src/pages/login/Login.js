import { useState } from "react";
import { Input, Button } from "../../components";
import { useNavigate } from "react-router-dom";
import styles from "./Login.module.css";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(false);
  const navigate = useNavigate();

  async function login(e) {
    e.preventDefault();

    console.log(email, password);

    const response = await fetch("http://localhost:8000/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
      },
      body: JSON.stringify({ email, password }),
    });

    const data = await response.json();
    if (data.status == true) {
      sessionStorage.setItem("user", JSON.stringify(data.message));
      navigate("/");
    } else {
      setError(true);
    }
  }

  return (
    <div className={styles.container} style={{ width: "100vw" }}>
      <h1>Login</h1>

      <form className={styles.form} onSubmit={login}>
        <Input
          onInputChange={setEmail}
          placeHolder="Digite o email"
          error={error}
          type="email"
        />
        <Input
          onInputChange={setPassword}
          placeHolder="Digite a senha"
          type="password"
          error={error}
        />

        <Button text="Entrar" variant="light" type="submit" />

        {error && <div className={styles.error}>Email ou senha incorretos</div>}
      </form>
    </div>
  );
}
