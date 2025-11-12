const handleSubmit = async (e) => {
  e.preventDefault();

    const username = document.querySelector("#username").value;
    const password = document.querySelector("#password").value;

  const response = await fetch("/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  });


    if (response.ok) {
      const data = await response.json();
      localStorage.setItem("token", data.token); 
      window.location.href = "/user";
  } else {
    alert("Неверное имя пользователя или пароль");
  }
};


document.getElementById("loginForm").addEventListener("submit", handleSubmit);