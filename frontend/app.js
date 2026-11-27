const $ = (id) => document.getElementById(id);
const API_BASE = "/api";
const tokenKey = "verifyonce_access_token";
const nameKey = "verifyonce_citizen_name";
const showNotice = (message) => { const box = $("formNotice"); if (box) { box.textContent = message; box.classList.add("show"); } };
const getToken = () => sessionStorage.getItem(tokenKey);
async function api(path, options = {}) {
  const headers = { "Content-Type": "application/json", ...(options.headers || {}) };
  if (getToken()) headers.Authorization = `Bearer ${getToken()}`;
  const response = await fetch(`${API_BASE}${path}`, { ...options, headers });
  const payload = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(payload.message || `Request failed (${response.status})`);
  return payload;
}

const registerForm = $("registerForm");
if (registerForm) {
  let otpStep = false;
  let registeredIdentity = "";
  registerForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    if (!registerForm.reportValidity()) return;
    const submit = $("registerSubmit");
    submit.disabled = true;
    try {
      if (!otpStep) {
        const body = {
          full_name: $("fullName").value.trim(),
          email: $("email").value.trim(),
          mobile: $("mobile").value.trim(),
          password: $("newPassword").value
        };
        const result = await api("/auth/register", { method: "POST", body: JSON.stringify(body) });
        registeredIdentity = body.email;
        otpStep = true;
        $("otpField").hidden = false;
        $("otp").required = true;
        $("otp").focus();
        submit.innerHTML = 'Verify OTP <span aria-hidden="true">→</span>';
        showNotice(`${result.message} Demo OTP: ${result.demo_otp || "Check backend console/configuration"}`);
      } else {
        const result = await api("/auth/otp/verify", { method: "POST", body: JSON.stringify({ identity: registeredIdentity, otp: $("otp").value }) });
        sessionStorage.setItem(tokenKey, result.access_token);
        sessionStorage.setItem(nameKey, result.citizen.full_name);
        window.location.href = "dashboard.html";
      }
    } catch (error) { showNotice(error.message); }
    finally { submit.disabled = false; }
  });
}

const loginForm = $("loginForm");
if (loginForm) loginForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  if (!loginForm.reportValidity()) return;
  const submit = loginForm.querySelector('button[type="submit"]');
  submit.disabled = true;
  try {
    const result = await api("/auth/login", { method: "POST", body: JSON.stringify({ identity: $("identity").value.trim(), password: $("password").value }) });
    sessionStorage.setItem(tokenKey, result.access_token);
    sessionStorage.setItem(nameKey, result.citizen.full_name);
    window.location.href = "dashboard.html";
  } catch (error) { showNotice(error.message); }
  finally { submit.disabled = false; }
});

const dashboard = $("welcomeName");
if (dashboard) {
  (async () => {
    if (!getToken()) { window.location.replace("login.html"); return; }
    try {
      const result = await api("/citizens/me");
      const citizen = result.citizen;
      const name = citizen.full_name || "Citizen";
      dashboard.textContent = `Welcome, ${name}`;
      if ($("profileName")) $("profileName").textContent = name;
      if ($("headerName")) $("headerName").textContent = name;
      if ($("avatar")) $("avatar").textContent = name.split(/\s+/).slice(0, 2).map(part => part[0]).join("").toUpperCase();
      if ($("citizenId")) $("citizenId").textContent = citizen.citizen_id || "Citizen ID pending";
      if ($("verificationBadge")) $("verificationBadge").textContent = "Demo contact verified · Not government verified";
    } catch (error) {
      sessionStorage.removeItem(tokenKey);
      sessionStorage.removeItem(nameKey);
      window.location.replace("login.html");
    }
  })();
}

const logout = $("logoutBtn");
if (logout) logout.addEventListener("click", (event) => {
  event.preventDefault();
  sessionStorage.removeItem(tokenKey);
  sessionStorage.removeItem(nameKey);
  window.location.href = "index.html";
});

if (!window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
  document.querySelectorAll(".reveal").forEach((el, i) => { el.style.animationDelay = `${i * 100}ms`; });
}
