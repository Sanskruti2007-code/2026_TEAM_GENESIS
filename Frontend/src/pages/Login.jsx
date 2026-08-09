import { useState } from "react";
import {
  Eye,
  EyeOff,
  LockKeyhole,
  Mail,
} from "lucide-react";

export default function Login({ onLogin }) {
  const [form, setForm] = useState({
    identity: "owner@vyaparsaathi.in",
    password: "demo123",
    remember: true,
  });

  const [showPassword, setShowPassword] =
    useState(false);

  const [error, setError] = useState("");

  const submit = (event) => {
    event.preventDefault();

    const email =
      /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    const mobile = /^[6-9]\d{9}$/;

    const normalizedMobile =
      form.identity.replace(/\D/g, "");

    if (
      !email.test(form.identity) &&
      !mobile.test(normalizedMobile)
    ) {
      setError(
        "Enter a valid email address or 10-digit mobile number."
      );
      return;
    }

    if (form.password.length < 6) {
      setError(
        "Password must contain at least 6 characters."
      );
      return;
    }

    setError("");
    onLogin(form.remember);
  };

  return (
    <main className="login-page">
      <section className="login-brand-panel">
        <img
          src="/vyaparsaathi-logo.jpeg"
          alt="VyaparSaathi logo"
        />

        <div>
          <span className="eyebrow gold">
            Voice-first business OS
          </span>

          <h1>
            Your business.
            <br />
            Clear, connected and in control.
          </h1>

          <p>
            Manage products, orders, profit and
            stock from one premium workspace—powered
            by regional-language voice commands.
          </p>
        </div>

        <small>Built for Indian MSME operators</small>
      </section>

      <section className="login-form-panel">
        <form
          className="login-card"
          onSubmit={submit}
        >
          <div className="mobile-logo">
            <img
              src="/vyaparsaathi-logo.jpeg"
              alt="VyaparSaathi logo"
            />
            <strong>VyaparSaathi</strong>
          </div>

          <span className="eyebrow">
            Secure business portal
          </span>

          <h2>Welcome to VyaparSaathi</h2>

          <p>
            Sign in to continue to your business
            dashboard.
          </p>

          <label>
            Email / Mobile Number

            <div className="input-with-icon">
              <Mail size={18} />

              <input
                value={form.identity}
                onChange={(event) =>
                  setForm({
                    ...form,
                    identity: event.target.value,
                  })
                }
                placeholder="owner@vyaparsaathi.in"
              />
            </div>
          </label>

          <label>
            Password

            <div className="input-with-icon">
              <LockKeyhole size={18} />

              <input
                type={
                  showPassword ? "text" : "password"
                }
                value={form.password}
                onChange={(event) =>
                  setForm({
                    ...form,
                    password: event.target.value,
                  })
                }
              />

              <button
                type="button"
                onClick={() =>
                  setShowPassword(!showPassword)
                }
              >
                {showPassword ? (
                  <EyeOff size={18} />
                ) : (
                  <Eye size={18} />
                )}
              </button>
            </div>
          </label>

          <div className="login-options">
            <label className="checkbox">
              <input
                type="checkbox"
                checked={form.remember}
                onChange={(event) =>
                  setForm({
                    ...form,
                    remember: event.target.checked,
                  })
                }
              />

              Remember me
            </label>

            <button
              type="button"
              className="text-button"
            >
              Forgot password?
            </button>
          </div>

          {error && (
            <p className="form-error">{error}</p>
          )}

          <button className="button primary full">
            Login to Dashboard
          </button>

          <p className="signup-copy">
            New to VyaparSaathi?{" "}
            <button
              type="button"
              className="text-button"
            >
              Create Account
            </button>
          </p>

          <div className="demo-note">
            <strong>Demo login</strong>
            <span>
              owner@vyaparsaathi.in · demo123
            </span>
          </div>
        </form>
      </section>
    </main>
  );
}