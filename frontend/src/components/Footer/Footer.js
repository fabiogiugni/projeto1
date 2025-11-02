import styles from "./Footer.module.css";
import Logo from "../../assets/Logo.svg";
import { Link } from "react-router-dom";

export default function Header() {
  let user = {
    name: "Samuel",
    cpf: "123.456.789.10",
    companyID: 12334,
    departmentID: 12334,
    teamID: 12334,
    email: "samuelfelipeif@gmail.com",
    role: "director",
  };

  const role = user?.role || "";

  return (
    <div className={styles.footer}>
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
    </div>
  );
}
