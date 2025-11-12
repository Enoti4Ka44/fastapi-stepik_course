const addFilmBtn = document.querySelector('#addFilmBtn');
const filmCostNode = document.querySelector('#filmCost');
const filmNameNode = document.querySelector('#filmName');
const filmDirectorNode = document.querySelector('#filmDirector');

async function loadUser() {
    const response = await fetch("/user_data_cookie", { 
        credentials: "include" // обязательно, чтобы cookie передавались
    });

    if (response.ok) {
        const data = await response.json();
        document.getElementById("username").textContent = `Username: ${data.username}`;
        document.getElementById("loginTime").textContent = `Login time: ${data.login_time}`;
        document.getElementById("sessionExpires").textContent = `Session expires: ${data.session_expires}`;

        const tbody = document.getElementById("moviesTable").querySelector("tbody");
        tbody.innerHTML = ""; // очищаем таблицу перед заполнением
        data.movies.forEach(movie => {
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td>${movie.id}</td>
                <td>${movie.name}</td>
                <td>${movie.cost}</td>
                <td>${movie.director}</td>
            `;
            tbody.appendChild(tr);
        });
    } else {
        alert("Сессия истекла или вы не авторизованы");
        window.location.href = "/login_cookie";
    }
}

const handleAddFilm = async (e) => {
    e.preventDefault();

    const filmName = filmNameNode.value;
    const filmCost = parseInt(filmCostNode.value);
    const filmDirector = filmDirectorNode.value;

    const response = await fetch("/add_film_cookie", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            name: filmName,
            cost: filmCost,
            director: filmDirector
        }),
        credentials: "include" // обязательно для cookie
    });

    if (response.ok) {
        const data = await response.json();
        alert(data.message);
        window.location.reload();
    } else {
        const error = await response.json();
        alert("Ошибка: " + error.detail);
    }
};

window.addEventListener("DOMContentLoaded", loadUser);
addFilmBtn.addEventListener('click', handleAddFilm);
