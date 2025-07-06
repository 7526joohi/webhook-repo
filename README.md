# Webhook Listener – TechStax Assignment

This project is a Flask-based webhook listener that receives GitHub events (`push`, `pull_request`, and `merge`), stores them in MongoDB,
and displays them through a simple frontend with auto-refresh.

---

## 📌 Features

- Listens for GitHub webhook events (`push`, `pull_request`, `merge`)
- Extracts and stores author, branches, and timestamp
- Stores data in MongoDB
- Displays latest events on a web page (auto-refresh every 15 seconds)
- Bonus: Detects merged pull requests

---

## 🧑‍💻 How to Run

### 1. Clone the Repository
```bash
git clone https://github.com/7526joohi/webhook-repo.git
cd webhook-repo
