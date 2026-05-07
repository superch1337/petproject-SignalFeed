import { useEffect, useState } from "react";
import API from "./api";

function App() {
  const [posts, setPosts] = useState([]);
  const [user, setUser] = useState(null);

  const [favorites, setFavorites] = useState([]);
  const [page, setPage] = useState("home");

  // AI modal
  const [analysisText, setAnalysisText] = useState("");
  const [showModal, setShowModal] = useState(false);

  // Trends modal
  const [trendsText, setTrendsText] = useState("");
  const [showTrendsModal, setShowTrendsModal] = useState(false);

  // Save modal
  const [saveText, setSaveText] = useState("");
  const [showSaveModal, setShowSaveModal] = useState(false);

  const loadUser = async () => {
    try {
      const res = await API.get("/me");
      setUser(res.data.user);
    } catch {
      setUser(null);
    }
  };

  const loadPosts = async () => {
    const res = await API.get("/posts");
    setPosts(res.data.posts);
  };

  const loadFavorites = async () => {
    try {
      const res = await API.get("/favorites");
      setFavorites(res.data.favorites);
    } catch (e) {
      console.error("Ошибка загрузки избранного:", e);
    }
  };

  const removeFavorite = async (url) => {
    await API.delete("/favorites", {
      params: { url },
    });

    loadFavorites();
  };

  useEffect(() => {
    loadUser();
    loadPosts();
  }, []);

  const login = () => {
    window.location.href = "http://localhost:8000/auth/login";
  };

  const handleLogout = async () => {
    await API.get("/logout");
    window.location.reload();
  };

  const addFavorite = async (post) => {
    await API.post("/favorites", null, {
      params: {
        title: post.title,
        url: post.url,
      },
    });

    setSaveText("Пост успешно добавлен в избранное ⭐");
    setShowSaveModal(true);
  };

  const analyze = async (title) => {
    setAnalysisText("Загрузка анализа...");
    setShowModal(true);

    const res = await API.get("/analyze", {
      params: { title },
    });

    setAnalysisText(res.data.analysis);
  };

  const loadTrends = async () => {
    setTrendsText("Загрузка трендов...");
    setShowTrendsModal(true);

    const res = await API.get("/trends");

    setTrendsText(res.data.trends);
  };

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <h1>SignalFeed 🚀</h1>

        <div>
          <button
            style={styles.navBtn}
            onClick={() => setPage("home")}
          >
            🏠 Главная
          </button>

          <button
            style={styles.navBtn}
            onClick={() => {
              setPage("favorites");
              loadFavorites();
            }}
          >
            ⭐ Избранное
          </button>
        </div>
      </div>

      {!user ? (
        <button style={styles.loginBtn} onClick={login}>
          Войти через Google
        </button>
      ) : (
        <div style={styles.userBox}>
          <img
            src={user.picture}
            alt="avatar"
            style={styles.avatar}
          />

          <span>Привет, {user.name}</span>

          <button
            style={styles.logoutBtn}
            onClick={handleLogout}
          >
            Выйти
          </button>
        </div>
      )}

      <button
        style={styles.trendBtn}
        onClick={loadTrends}
      >
        📈 Показать тренды
      </button>

      {/* ГЛАВНАЯ */}
      {page === "home" && (
        <div style={styles.grid}>
          {posts.map((post, i) => (
            <div
              key={i}
              style={styles.card}
              onMouseEnter={(e) => {
                e.currentTarget.style.transform =
                  "translateY(-5px)";

                e.currentTarget.style.boxShadow =
                  "0 12px 25px rgba(59,130,246,0.4)";
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.transform =
                  "translateY(0)";

                e.currentTarget.style.boxShadow =
                  "0 10px 30px rgba(0,0,0,0.45)";
              }}
            >
              <a
                href={post.url}
                target="_blank"
                style={{
                  color: "white",
                  textDecoration: "none",
                }}
              >
                <h3
                  style={{
                    fontSize: 24,
                    lineHeight: 1.3,
                  }}
                >
                  {post.title}
                </h3>
              </a>

              {user && (
                <div style={styles.actions}>
                  <button
                    style={styles.actionBtn}
                    onClick={() => addFavorite(post)}
                  >
                    ⭐ Сохранить
                  </button>

                  <button
                    style={styles.actionBtn}
                    onClick={() => analyze(post.title)}
                  >
                    🤖 Анализ
                  </button>
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      {/* ИЗБРАННОЕ */}
      {page === "favorites" && (
        <div style={styles.grid}>
          {favorites.length === 0 && <p>Пусто</p>}

          {favorites.map((fav, i) => (
            <div
              key={i}
              style={styles.card}
              onMouseEnter={(e) => {
                e.currentTarget.style.transform =
                  "translateY(-5px)";

                e.currentTarget.style.boxShadow =
                  "0 12px 25px rgba(59,130,246,0.4)";
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.transform =
                  "translateY(0)";

                e.currentTarget.style.boxShadow =
                  "0 10px 30px rgba(0,0,0,0.45)";
              }}
            >
              <a
                href={fav.url}
                target="_blank"
                style={{
                  color: "white",
                  textDecoration: "none",
                }}
              >
                <h3
                  style={{
                    fontSize: 24,
                    lineHeight: 1.3,
                  }}
                >
                  {fav.title}
                </h3>
              </a>

              <button
                style={styles.deleteBtn}
                onClick={() => removeFavorite(fav.url)}
              >
                ❌ Удалить
              </button>
            </div>
          ))}
        </div>
      )}

      {/* AI MODAL */}
      {showModal && (
        <div style={styles.modalOverlay}>
          <div style={styles.modal}>
            <h2>🤖 AI Анализ</h2>

            <p style={{ whiteSpace: "pre-line" }}>
              {analysisText}
            </p>

            <button
              style={styles.closeBtn}
              onClick={() => setShowModal(false)}
            >
              Закрыть
            </button>
          </div>
        </div>
      )}

      {/* TRENDS MODAL */}
      {showTrendsModal && (
        <div style={styles.modalOverlay}>
          <div style={styles.modal}>
            <h2>📈 AI Тренды</h2>

            <p style={{ whiteSpace: "pre-line" }}>
              {trendsText}
            </p>

            <button
              style={styles.closeBtn}
              onClick={() => setShowTrendsModal(false)}
            >
              Закрыть
            </button>
          </div>
        </div>
      )}

      {/* SAVE MODAL */}
      {showSaveModal && (
        <div style={styles.modalOverlay}>
          <div style={styles.modal}>
            <h2>⭐ Избранное</h2>

            <p>{saveText}</p>

            <button
              style={styles.closeBtn}
              onClick={() => setShowSaveModal(false)}
            >
              Закрыть
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;

const styles = {
  container: {
    padding: 40,
    fontFamily: "Arial",
    background:
      "linear-gradient(to bottom, #0f172a, #020617)",
    minHeight: "100vh",
    color: "white",
  },

  header: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: 20,
  },

  navBtn: {
    marginRight: 10,
    padding: "10px 16px",
    borderRadius: 12,
    border: "1px solid rgba(255,255,255,0.1)",
    background: "rgba(255,255,255,0.06)",
    color: "white",
    cursor: "pointer",
    transition: "0.3s",
  },

  loginBtn: {
    padding: "12px 18px",
    borderRadius: 12,
    marginBottom: 20,
    border: "none",
    background: "#2563eb",
    color: "white",
    cursor: "pointer",
    fontSize: 16,
  },

  logoutBtn: {
    marginLeft: 10,
    padding: "10px 16px",
    borderRadius: 12,
    border: "1px solid rgba(255,255,255,0.1)",
    background: "rgba(255,255,255,0.06)",
    color: "white",
    cursor: "pointer",
  },

  trendBtn: {
    marginBottom: 20,
    padding: "12px 18px",
    borderRadius: 12,
    border: "1px solid rgba(255,255,255,0.1)",
    background: "rgba(255,255,255,0.06)",
    color: "white",
    cursor: "pointer",
    fontSize: 16,
  },

  userBox: {
    marginBottom: 20,
    display: "flex",
    alignItems: "center",
    gap: 10,
  },

  grid: {
    display: "grid",
    gridTemplateColumns:
      "repeat(auto-fill, minmax(350px, 1fr))",
    gap: 24,
  },

  card: {
    background:
      "linear-gradient(135deg, #1e293b 0%, #0f172a 100%)",
    padding: 24,
    borderRadius: 20,
    boxShadow: "0 10px 30px rgba(0,0,0,0.45)",
    border: "1px solid rgba(96,165,250,0.25)",
    transition: "all 0.3s ease",
    cursor: "pointer",
    backdropFilter: "blur(10px)",
  },

  actions: {
    marginTop: 14,
    display: "flex",
    gap: 12,
  },

  actionBtn: {
    background: "rgba(255,255,255,0.06)",
    color: "white",
    border: "1px solid rgba(255,255,255,0.1)",
    padding: "10px 16px",
    borderRadius: 12,
    cursor: "pointer",
    fontSize: 16,
    transition: "all 0.3s ease",
    backdropFilter: "blur(6px)",
  },

  deleteBtn: {
    marginTop: 14,
    background: "rgba(239,68,68,0.15)",
    color: "#f87171",
    padding: "10px 16px",
    borderRadius: 12,
    border: "1px solid rgba(239,68,68,0.25)",
    cursor: "pointer",
    fontSize: 16,
    transition: "all 0.3s ease",
  },

  avatar: {
    width: 45,
    height: 45,
    borderRadius: "50%",
    objectFit: "cover",
    border: "2px solid rgba(255,255,255,0.15)",
  },

  modalOverlay: {
    position: "fixed",
    top: 0,
    left: 0,
    width: "100%",
    height: "100%",
    background: "rgba(0,0,0,0.7)",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    zIndex: 1000,
  },

  modal: {
    width: "600px",
    maxWidth: "90%",
    background:
      "linear-gradient(135deg, #1e293b, #0f172a)",
    padding: 30,
    borderRadius: 20,
    border: "1px solid rgba(96,165,250,0.25)",
    boxShadow: "0 20px 50px rgba(0,0,0,0.5)",
    overflowY: "auto",
    maxHeight: "80vh",
  },

  closeBtn: {
    marginTop: 20,
    padding: "10px 16px",
    borderRadius: 12,
    border: "none",
    background: "#2563eb",
    color: "white",
    cursor: "pointer",
    fontSize: 16,
  },
};