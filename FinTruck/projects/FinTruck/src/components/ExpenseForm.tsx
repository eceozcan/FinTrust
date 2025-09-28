import React, { useState } from "react";
import { ExpenseData, ExpenseResponse } from "../types";

interface ExpenseFormProps {
    connectedAccount: string | null;
}

export const ExpenseForm: React.FC<ExpenseFormProps> = ({ connectedAccount }) => {
    const [description, setDescription] = useState("");
    const [amount, setAmount] = useState<number | "">("");
    const [currency, setCurrency] = useState("TL");
    const [messages, setMessages] = useState<JSX.Element[]>([]);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!connectedAccount) {
            alert("Lütfen önce Wallet bağlayın!");
            return;
        }

        const userMessage = <div className="message user">👤: {description} - {amount} {currency}</div>;
        setMessages((prev) => [...prev, userMessage]);

        const payload: ExpenseData = { description, amount: Number(amount), currency, wallet: connectedAccount };

        try {
            const response = await fetch("http://192.168.1.50:5000/add_expense", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload),
            });

            const data: ExpenseResponse = await response.json();

            const systemMessage = response.ok ? (
                <div className="message system">
                    <p><strong>Kategori:</strong> {data.category}</p>
                    <p><strong>Öneri:</strong> {data.suggestion}</p>
                    <p><strong>Transaction ID:</strong> <a href={data.explorer} target="_blank" rel="noopener noreferrer">{data.txid}</a></p>
                    <p><strong>Tutar:</strong> {data.amount} {data.currency}</p>
                    <p><strong>Tutar TL:</strong> {data.amount_tl} TL</p>
                </div>
            ) : (
                <div className="message system" style={{ color: "red" }}>{data.error}</div>
            );

            setMessages((prev) => [...prev, systemMessage]);
            setDescription("");
            setAmount("");
            setCurrency("TL");

        } catch (err) {
            const errorMsg = <div className="message system" style={{ color: "red" }}>Sunucuya bağlanamadı!</div>;
            setMessages((prev) => [...prev, errorMsg]);
            console.error(err);
        }
    };

    return (
        <div className="container">
            <h2>Bugün ne satın almayı düşünüyorsun?</h2>
            <form onSubmit={handleSubmit}>
                Ürün Açıklaması: <input type="text" value={description} onChange={e => setDescription(e.target.value)} placeholder="Örn: Starbucks Latte" required />
                Tutar: <input type="number" value={amount} onChange={e => setAmount(Number(e.target.value))} placeholder="Örn: 25" required />
                Para Birimi:
                <select value={currency} onChange={e => setCurrency(e.target.value)}>
                    <option value="TL">TL</option>
                    <option value="USD">USD</option>
                    <option value="EUR">EUR</option>
                </select>
                <button type="submit">Gönder</button>
            </form>
            <div className="result">{messages}</div>
        </div>
    );
};
