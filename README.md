# **🌐 Zenith - Open-Source AI Chatbot**  

**Zenith** is a lightweight, open-source AI chatbot built with **Node.js, PostgreSQL, and React**. Designed for seamless conversations and developer-friendly customization.  

👉 **Live Demo**: [Coming Soon]  
📌 **Main Branch**: `main` (stable releases)  
💻 **Dev Branch**: `dev` (active development)  

---

## **✨ Features**  
✅ **Node.js + Express** backend  
✅ **PostgreSQL** chat history storage  
✅ **React** frontend with TailwindCSS  
✅ **OpenAI/Llama 3** API integration  
✅ **Easy deployment** (Vercel + Railway)  

---

## **🧑‍💻 Development Setup**  

### **1. Clone & Switch to `dev` Branch**  
```bash
git clone https://github.com/your-username/zenith-chatbot.git
cd zenith-chatbot
git checkout dev  # Switch to development branch
```

### **2. Set Up Backend**  
```bash
cd server
npm install
cp .env.example .env  # Add your OpenAI + DB keys
npm run dev          # Starts server (3001)
```

### **3. Set Up Frontend**  
```bash
cd ../client
npm install
npm run dev          # Starts React app (3000)
```

---

## **🌲 Branch Strategy**  
| Branch   | Purpose                          | 
|----------|----------------------------------|
| `main`   | Production-ready code            | 
| `dev`    | Active development (PRs go here) | 
| `feat/*` | Feature branches (e.g., `feat/auth`) | 

**Contributors**:  
1. Create a **new branch** from `dev`:  
   ```bash
   git checkout -b feat/your-feature
   ```
2. Submit a **PR to `dev`** after testing.  

---

## **📂 Project Structure**  
```markdown
zenith-chatbot/
├── client/           # React frontend
│   ├── public/
│   └── src/          # Components, pages, styles
├── server/           # Node.js backend
│   ├── config/       # DB setup
│   ├── controllers/  # API logic
│   └── models/       # PostgreSQL queries
├── .gitignore
├── LICENSE           # MIT
└── README.md
```

---

## **🤝 Contributing Guidelines**  
1. **Fork the repo** and clone your fork.  
2. **Branch off `dev`**:  
   ```bash
   git checkout -b fix/issue-name
   ```
3. **Commit changes**:  
   ```bash
   git commit -m "feat: add user authentication"
   ```
4. **Push & submit a PR to `dev`**.  

**Code Standards**:  
- Use **ES6+** (JavaScript/React).  
- Document new endpoints with **JSDoc**.  
- Test changes locally before PRs.  

---

## **🚀 Deployment**  
### **Frontend (Vercel)**  
1. Link your GitHub repo to Vercel.  
2. Deploy the `client` folder.  

### **Backend (Railway)**  
1. Upload `server/` and connect PostgreSQL.  
2. Add environment variables from `.env`.  

---

## **📜 License**  
MIT © [F. M. David F. RATIANDRAIBE ]  

---

### **🔗 Key Files for Contributors**  
- [`server/app.js`](server/app.js) - Express API entrypoint.  
- [`client/src/App.js`](client/src/App.js) - Main React component.  
- [`CONTRIBUTING.md`](CONTRIBUTING.md) - Detailed guidelines.  
