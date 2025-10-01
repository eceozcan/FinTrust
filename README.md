## 🚀 FinTrust - Smart Expense Tracker

### 🌟 Project Description
**FinTrust** is an **AI-powered expense tracking application** designed to help users **monitor daily purchases, categorize spending**, and receive **intelligent budget suggestions**.  
It leverages **blockchain technology (Algorand)** to securely log transactions and integrates a **wallet connection system (Pera Wallet)** for transaction verification.  
The application is built with **React** for the frontend and **Flask** for the backend.

---

### ✨ Features
- 🔗 **Connect to Pera Wallet** to verify transactions
- 📝 **Add daily expenses** with description, amount, and currency
- 📊 **Automatic categorization** of expenses:
  - Food 🍔
  - Transportation 🚆
  - Entertainment 🎮
  - Health 💊
  - Shopping 🛍️
  - Other 🗂️
- 🤖 **AI-powered suggestions** to optimize spending
- 🔍 **View transaction ID** directly in Algorand Explorer
- 💰 **Automatic TL conversion** for all amounts
- 💬 **Interactive chat-style UI** to display expense history and recommendations

---

### 🛠️ Technologies Used
- **Frontend:** React, TypeScript, CSS
- **Backend:** Flask, Python
- **Blockchain:** Algorand SDK
- **AI:** Google Gemini (optional)
- **Wallet Integration:** Pera Wallet
- **Other:** CORS, dotenv for environment management

---

### 🏗️ Project Architecture
- **Frontend:**  
  React components (`Home.tsx`, `ConnectWallet.tsx`) handle:
  - User input
  - Wallet connections
  - Display of expenses & messages
- **Backend:**  
  Flask server handles:
  - Expense processing
  - AI categorization or rule-based fallback
  - TL conversion
  - Logging transactions to Algorand
- **AI Integration:**  
  Optional AI categorization via **Gemini API**, fallback **rule-based system** ensures reliability.

---

### 💻 Installation
1. Clone the repository: `git clone https://github.com/yourusername/FinTrust.git`
2. Backend setup:
    ```bash
    cd backend
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```
3. Frontend setup:
    ```bash
    cd frontend
    npm install
    npm start
    ```
4. Configure `.env` file for API keys, Algorand credentials, and Gemini API if used.
5. Run backend: `python app.py`
6. Access the app at `http://localhost:3000`

### Notes
- Ensure Algorand TestNet account and Pera Wallet connection are set up.
- Gemini API key is optional; a fallback rule-based categorization exists.
- Demo video is here: **https://drive.google.com/file/d/1T3uRsKLrK2qlBenWNhjgOlQ3ZRoCksmn/view?usp=sharing**
- Presentation link: **https://www.canva.com/design/DAG0QG0nDbw/03LWQS0SGQlAbnnFGWgHIg/edit?utm_content=DAG0QG0nDbw&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton**
  
