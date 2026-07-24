import api from "../api/axios";

export async function login(email, password) {

    const response = await api.post("/login", {
        email,
        password,
    });

    return response.data;
}

export async function getCurrentUser() {

    const response = await api.get("/me");

    return response.data;
}