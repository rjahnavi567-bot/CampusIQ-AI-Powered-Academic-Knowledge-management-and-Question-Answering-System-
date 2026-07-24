import { createContext, useContext, useEffect, useState } from "react";
import { login as loginService, getCurrentUser } from "../services/authService";

const AuthContext = createContext();

export function AuthProvider({ children }) {

    const [user, setUser] = useState(null);

    const [loading, setLoading] = useState(true);

    useEffect(() => {

        async function loadUser() {

            const token = localStorage.getItem("token");

            if (!token) {
                setLoading(false);
                return;
            }

            try {

                const currentUser = await getCurrentUser();

                setUser(currentUser);

            } catch {

                localStorage.removeItem("token");

                setUser(null);

            }

            setLoading(false);
        }

        loadUser();

    }, []);

    async function login(email, password) {

        const response = await loginService(email, password);

        localStorage.setItem(
            "token",
            response.access_token
        );

        const currentUser = await getCurrentUser();

        setUser(currentUser);

        return currentUser;
    }

    function logout() {

        localStorage.removeItem("token");

        setUser(null);
    }

    return (

        <AuthContext.Provider
            value={{
                user,
                loading,
                login,
                logout
            }}
        >

            {children}

        </AuthContext.Provider>

    );
}

export function useAuth() {

    return useContext(AuthContext);
}