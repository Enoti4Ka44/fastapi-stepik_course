const addFilmBtn = document.querySelector('#addFilmBtn')
const filmCostNode = document.querySelector('#filmCost')
const filmNameNode = document.querySelector('#filmName')
const filmDirectorNode = document.querySelector('#filmDirector')

async function loadUser() {
    const token = localStorage.getItem("token");
    if (!token) {
        alert("Пожалуйста, войдите в аккаует");
        window.location.href = "/login";
        return;
    }

    const response = await fetch("/user_data", { 
        headers: {
            "Authorization": `Bearer ${token}`
        }
    });
    
    if (response.ok) {
        const data = await response.json();
        document.getElementById("username").textContent = `Username: ${data.username}`;

        const tbody = document.getElementById("moviesTable").querySelector("tbody");
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
        localStorage.removeItem("token");
        alert("Сессия истекла, войдите снова");
        window.location.href = "/login";
    }
}

const handleAddFilm = async (e) => {
    e.preventDefault();

    const token = localStorage.getItem("token");
    if (!token) {
        alert("Пожалуйста, войдите в систему");
        window.location.href = "/login";
        return;
    }

    const filmName = filmNameNode.value;
    const filmCost = parseInt(filmCostNode.value);
    const filmDirector = filmDirectorNode.value;

    const response = await fetch("/add_film", {
        method: "POST",
        headers: { 
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({
            name: filmName,
            cost: filmCost,
            director: filmDirector
        }),
        credentials: "include"
    });

    if (response.ok) {
        const data = await response.json();
        alert(data.message);
        window.location.reload();
    } else {
        alert("Ошибка: " + data.message);
    }
};


window.addEventListener("DOMContentLoaded", loadUser);
addFilmBtn.addEventListener('click', handleAddFilm)
