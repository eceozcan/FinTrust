import React, { useState, useRef, useEffect } from 'react'
import { useWallet } from '@txnlab/use-wallet-react'
import './styles/home.css'
import ConnectWallet from './components/ConnectWallet'

interface Expense {
  description: string
  amount: number
  currency: string
  category: string
  suggestion: string
  txid: string
  explorer: string
  amount_tl: number
}

const Home: React.FC = () => {
  const { activeAddress } = useWallet()

  const [description, setDescription] = useState('')
  const [amount, setAmount] = useState<number | ''>('')
  const [currency, setCurrency] = useState('TL')
  const [expenses, setExpenses] = useState<Expense[]>([])
  const [messages, setMessages] = useState<Array<any>>([])
  const [openWalletModal, setOpenWalletModal] = useState<boolean>(false)

  const toggleWalletModal = () => { setOpenWalletModal(!openWalletModal) }

  // Ref for scrolling
  const resultRef = useRef<HTMLDivElement>(null)

  // Scroll to bottom when messages change
  useEffect(() => {
    if (resultRef.current) {
      resultRef.current.scrollTop = resultRef.current.scrollHeight
    }
  }, [messages])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    if (!activeAddress) {
      alert('Please connect your wallet first!')
      return
    }

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
        const newExpense: Expense = {
          description: data.description,
          amount: data.amount,
          currency: data.currency,
          category: data.category,
          suggestion: data.suggestion,
          txid: data.txid,
          explorer: `https://testnet.explorer.perawallet.app/tx/${data.txid}/`,
          amount_tl: data.amount_tl
        }
        setExpenses((prev) => [...prev, newExpense])

        const sysMsg = {
          type: 'system',
          text: `
<span class="label">Category:</span> ${data.category}
<span class="label">Suggestion:</span> ${data.suggestion}
<span class="label">Transaction ID:</span> <a href="https://testnet.explorer.perawallet.app/tx/${data.txid}/" target="_blank" rel="noopener noreferrer">View in Explorer</a>
<span class="label">Amount:</span> ${data.amount} ${data.currency}
<span class="label">Amount in TL:</span> ${data.amount_tl} TL
`,
        }
        setMessages((prev) => [...prev, sysMsg])
      } else {
        setMessages((prev) => [...prev, { type: 'system', text: `Error: ${data.error}` }])
      }
    } catch (err) {
      setMessages((prev) => [...prev, { type: 'system', text: 'Could not connect to the server!' }])
      console.error(err)
    }

    setDescription('')
    setAmount('')
    setCurrency('TL')
  }

  return (
    <>
      <nav>
        <h1>FinTrust</h1>
        <div>
          <a href="#add-expense">What are you planning to buy today?</a>
        </div>
      </nav>

      <div className="welcome-banner">
        <h2>
          Welcome to <span>FinTrust</span>
        </h2>
        <p>Take control of your budget with smart expense tracking!</p>
      </div>

      <div className="container" id="add-expense">
        <h2>What are you planning to purchase today?</h2>

        {!activeAddress ? (
          <button onClick={toggleWalletModal} type="button">
            Connect Wallet
          </button>
        ) : (
          <button onClick={toggleWalletModal} type="button">
            Disconnect Wallet
          </button>
        )}

        <form onSubmit={handleSubmit}>
          <span className="label">Product Description:</span>{' '}
          <input
            type="text"
            placeholder="e.g., Starbucks Latte"
            required
            value={description}
            onChange={(e) => setDescription(e.target.value)}
          />
          <span className="label">Amount:</span>{' '}

          <input
            type="number"
            placeholder="e.g., 25"
            required
            value={amount}
            onChange={(e) => setAmount(Number(e.target.value))}
          />
          <span className="label">Currency:</span>
          <select value={currency} onChange={(e) => setCurrency(e.target.value)}>
            <option value="TL">TL</option>
            <option value="USD">USD</option>
            <option value="EUR">EUR</option>
          </select>
          <button type="submit">Send</button>
        </form>

        <ConnectWallet openModal={openWalletModal} closeModal={toggleWalletModal} />

        <div className="result" ref={resultRef}>
          {messages.map((msg, idx) => (
            <div key={idx} className={`message ${msg.type}`}>
              {msg.text.split('\n').map((line: any, i: number) => (
                <p key={i} dangerouslySetInnerHTML={{ __html: line }}></p>
              ))}
            </div>
          ))}
        </div>

        {expenses.length > 0 && (
          <div className="history">
            <h3>Expense History</h3>
            <ul>
              {expenses.map((exp, idx) => (
                <li key={idx}>
                  {exp.description} - {exp.amount} {exp.currency} ({exp.category}) |{' '}
                  <a href={exp.explorer} target="_blank" rel="noopener noreferrer">
                    View TX
                  </a>{' '}
                  | TL: {exp.amount_tl}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </>
  )
}

export default Home
