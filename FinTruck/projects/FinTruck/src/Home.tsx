// src/components/Home.tsx
import React, { useState } from 'react'
import { useWallet } from '@txnlab/use-wallet-react'
import './styles/home.css'
import ConnectWallet from './components/ConnectWallet'

const Home: React.FC = () => {
  const { activeAddress } = useWallet()

  const [description, setDescription] = useState('')
  const [amount, setAmount] = useState<number | ''>('')
  const [currency, setCurrency] = useState('TL')
  const [messages, setMessages] = useState<Array<any>>([])
  const [openWalletModal, setOpenWalletModal] = useState<boolean>(false)
  const toggleWalletModal = () => { setOpenWalletModal(!openWalletModal) }

  // Form submit
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    if (!activeAddress) {
      alert('Lütfen önce Wallet bağlayın!')
      return
    }

    // Kullanıcı mesajı
    const userMsg = { type: 'user', text: `👤: ${description} - ${amount} ${currency}` }
    setMessages((prev) => [...prev, userMsg])

    try {
      const res = await fetch('http://localhost:5000/add_expense', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ description, amount, currency, wallet: activeAddress }),
      })
      const data = await res.json()

      if (res.ok) {
        // Sistem mesajı
        const sysMsg = {
          type: 'system',
          text: `
Kategori: ${data.category}
Öneri: ${data.suggestion}
Transaction ID: <a href="https://testnet.explorer.perawallet.app/tx/${data.txid}/" target="_blank" rel="noopener noreferrer">View in explorer</a>
Tutar: ${data.amount} ${data.currency}
Tutar TL: ${data.amount_tl} TL
          `,
        }
        setMessages((prev) => [...prev, sysMsg])
      } else {
        const sysMsg = { type: 'system', text: `Hata: ${data.error}` }
        setMessages((prev) => [...prev, sysMsg])
      }
    } catch (err) {
      const sysMsg = { type: 'system', text: 'Sunucuya bağlanamadı!' }
      setMessages((prev) => [...prev, sysMsg])
      console.error(err)
    }

    // Form reset
    setDescription('')
    setAmount('')
    setCurrency('TL')
  }

  return (
    <>
      {/* Navbar */}
      <nav>
        <h1>FinTrust</h1>
        <div>
          <a href="#add-expense">Bugün ne almayı düşünüyorsun?</a>
        </div>
      </nav>

      {/* Welcome Banner */}
      <div className="welcome-banner">
        <h2>
          Welcome to <span>FinTrust</span>
        </h2>
        <p>Akıllı harcama takibiyle bütçene yön ver!</p>
      </div>

      {/* Container */}
      <div className="container" id="add-expense">
        <h2>Bugün ne satın almayı düşünüyorsun?</h2>

        {/* Wallet Button */}
        {!activeAddress ? (
          <button onClick={toggleWalletModal} type="button">
            Wallet Bağla
          </button>
        ) : (
          <button onClick={toggleWalletModal} type="button">
            Wallet Çıkış
          </button>
        )}

        {/* Expense Form */}
        <form onSubmit={handleSubmit}>
          Ürün Açıklaması:{' '}
          <input
            type="text"
            placeholder="Örn: Starbucks Latte"
            required
            value={description}
            onChange={(e) => setDescription(e.target.value)}
          />
          Tutar:{' '}
          <input
            type="number"
            placeholder="Örn: 25"
            required
            value={amount}
            onChange={(e) => setAmount(Number(e.target.value))}
          />
          Para Birimi:
          <select value={currency} onChange={(e) => setCurrency(e.target.value)}>
            <option value="TL">TL</option>
            <option value="USD">USD</option>
            <option value="EUR">EUR</option>
          </select>
          <button type="submit">Gönder</button>
        </form>

        {/* Wallet Modal */}
        <ConnectWallet openModal={openWalletModal} closeModal={toggleWalletModal} />

        {/* Messages */}
        <div className="result">
          {messages.map((msg, idx) => (
            <div key={idx} className={`message ${msg.type}`}>
              {msg.text.split('\n').map((line: any, i: number) => (
                <p key={i} dangerouslySetInnerHTML={{ __html: line }}></p>
              ))}
            </div>
          ))}
        </div>
      </div>
    </>
  )
}

export default Home
