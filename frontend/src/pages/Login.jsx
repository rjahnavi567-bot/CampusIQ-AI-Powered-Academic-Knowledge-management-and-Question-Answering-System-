import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { Link } from "react-router-dom";
function Login() {

    const navigate = useNavigate();

    const { login } = useAuth();

    const [email, setEmail] = useState("");

    const [password, setPassword] = useState("");

    const [error, setError] = useState("");

    async function handleLogin(e) {

        e.preventDefault();

        setError("");

        try {

            await login(email, password);

            navigate("/dashboard");

        }

        catch {

            setError("Invalid Email or Password");

        }

    }

    return (

        <div
            style={{
                width: "350px",
                margin: "100px auto"
            }}
        >

            <h2>AI Academic System Login</h2>

            <form onSubmit={handleLogin}>

                <input
                    type="email"
                    placeholder="Email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    style={{
                        width: "100%",
                        marginBottom: "10px"
                    }}
                />

                <input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    style={{
                        width: "100%",
                        marginBottom: "10px"
                    }}
                />

                <button
                    type="submit"
                    style={{
                        width: "100%"
                    }}
                >
                    Login
                </button>
                <p
    style={{
        marginTop: "20px"
    }}
>

    Don't have an account?

    <Link
        to="/register"
    >

        Register

    </Link>

</p>
            </form>

            <p style={{ color: "red" }}>
                {error}
            </p>

        </div>

    );

}

export default Login;