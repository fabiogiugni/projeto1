import { Link } from "react-router-dom";
import { Button } from "../../components";
import styles from "./Header.module.css";
import Logo from "../../assets/Logo.svg";
import { directors } from "../../assets/testValues";

export default function Header() {
  let user = directors[0];

  const role = user?.role || "";

  return (
    <div className={styles.header}>
      {!!role ? (
        <Link to="/">
          <img
            src={Logo}
            alt="Logo"
            style={{ height: "2.5rem", outerWidth: "2.5rem" }}
          />
        </Link>
      ) : (
        <img
          src={Logo}
          alt="Logo"
          style={{ height: "2.5rem", outerWidth: "2.5rem" }}
        />
      )}

      <div className={styles.links}>
        {/* Not logged in */}
        {!role && (
          <Link to="/login" className={styles.link}>
            <Button text="Login" variant="light" />
          </Link>
        )}

        {/* Director */}
        {role === "director" && (
          <>
            <Link to="/company" className={styles.link}>
              Empresa
            </Link>
            <Link to="/departments" className={styles.link}>
              Departamento
            </Link>
            <Link to="/teams" className={styles.link}>
              Equipe
            </Link>
            <Link to="/employees" className={styles.link}>
              Funcionários
            </Link>
            <Link to="/rpe">
              <Button text="Gerenciar RPEs" />
            </Link>
            <Link to="/profile">
              <Button text="Perfil" variant="light" />
            </Link>
          </>
        )}

        {/* Manager */}
        {role === "manager" && (
          <>
            <Link to="/teams" className={styles.link}>
              Equipes
            </Link>
            <Link to="/employees" className={styles.link}>
              Funcionários
            </Link>
            <Link to="/rpe">
              <Button text="Gerenciar RPEs" />
            </Link>
            <Link to="/profile">
              <Button text="Perfil" variant="light" />
            </Link>
          </>
        )}

        {/* Employee */}
        {role === "employee" && (
          <Link to="/profile">
            <Button text="Perfil" variant="light" />
          </Link>
        )}
      </div>
    </div>
  );
}
