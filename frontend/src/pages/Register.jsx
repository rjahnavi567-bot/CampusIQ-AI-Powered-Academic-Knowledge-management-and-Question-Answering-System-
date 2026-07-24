import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { api } from "../api/api";

export default function Register() {

    const navigate = useNavigate();

    const [form, setForm] = useState({
        name: "",
        email: "",
        password: "",
        confirm_password: ""
    });

    const [message, setMessage] = useState("");

    const handleChange = (e) => {

        setForm({
            ...form,
            [e.target.name]: e.target.value
        });

    };

    const handleRegister = async () => {

    if (!form.name.trim()) {

        setMessage("Please enter your name");

        return;

    }

    if (!form.email.trim()) {

        setMessage("Please enter your email");

        return;

    }

    if (!form.password.trim()) {

        setMessage("Please enter your password");

        return;

    }

    if (form.password.length < 8) {

        setMessage("Password must contain at least 8 characters");

        return;

    }

    if (form.password !== form.confirm_password) {

        setMessage("Passwords do not match");

        return;

    }

    try {

        const res = await api.post(
            "/register",
            form
        );

        setMessage("✅ Registration Successful");

        setTimeout(() => {

            navigate("/login");

        }, 1500);

    }

    catch (err) {

        if (err.response) {

            setMessage(err.response.data.detail);

        }

        else {

            setMessage("Registration Failed");

        }

    }

};

    return (

        <div className="login-container">

            <div className="login-card">

                <h2>Create Account</h2>

                <input
                    type="text"
                    name="name"
                    placeholder="Full Name"
                    value={form.name}
                    onChange={handleChange}
                />

                <input
                    type="email"
                    name="email"
                    placeholder="Email"
                    value={form.email}
                    onChange={handleChange}
                />

                <input
                    type="password"
                    name="password"
                    placeholder="Password"
                    value={form.password}
                    onChange={handleChange}
                />

                <input
                    type="password"
                    name="confirm_password"
                    placeholder="Confirm Password"
                    value={form.confirm_password}
                    onChange={handleChange}
                />

                <button
                    onClick={handleRegister}
                >
                    Register
                </button>

                <p
    style={{
        color: message.includes("Successful")
            ? "green"
            : "red",
        marginTop: "15px"
    }}
>
    {message}
</p>

                <p>

                    Already have an account?

                    <Link to="/login">

                        Login

                    </Link>

                </p>

            </div>

        </div>

    );

}