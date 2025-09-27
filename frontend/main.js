const form = document.getElementById("expense-form");
const resultDiv = document.getElementById("result");

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const description = document.getElementById("description").value;
    const amount = parseFloat(document.getElementById("amount").value);

    try {
        const response = await fetch("http://127.0.0.1:5000/add_expense", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ description, amount })
        });

        const data = await response.json();

        if (response.ok) {
            // Sonucu göster
            resultDiv.innerHTML = `
                <p><strong>Kategori:</strong> ${data.category}</p>
                <p><strong></strong> ${data.suggestion}</p>
                <p><strong>Transaction ID:</strong> 
                    <a href="${data.explorer}" target="_blank" rel="noopener noreferrer">${data.txid}</a>
                </p>
            `;
        } else {
            resultDiv.innerHTML = `<p style="color:red;">Hata: ${data.error}</p>`;
        }

    } catch (err) {
        resultDiv.innerHTML = `<p style="color:red;">Sunucuya bağlanamadı!</p>`;
        console.error(err);
    }
});
