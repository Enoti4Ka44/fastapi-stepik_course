const handleCookieLogin = async (e) => {
  e.preventDefault();

  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  const response = await fetch("/login_cookie", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
    credentials: "include" 
  });

  if (response.ok) {
    alert("Успешный вход!");
    setTimeout(() => window.location.href = "/user_cookie", 1000);
  } else {
    const data = await response.json();
    alert(data.detail || "Ошибка входа");
  }
};

document.getElementById("loginCookieForm").addEventListener("submit", handleCookieLogin);
