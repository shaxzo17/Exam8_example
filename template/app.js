// Dummy data
let cards = [
  {id:1, number:"**** 1234", holder:"John Doe", balance: 1200},
  {id:2, number:"**** 5678", holder:"Jane Smith", balance: 850}
];

let transactions = [
  {id:1, to:"**** 5678", category:"Food", amount:50},
  {id:2, to:"**** 1234", category:"Shopping", amount:120}
];

let categories = ["Food", "Shopping", "Transport"];

// Render balance on main page
function renderBalance() {
  let total = cards.reduce((sum,c)=>sum+c.balance,0);
  const el = document.getElementById("balance");
  if(el) el.innerText = "$" + total;
}

// Render cards
function renderCards() {
  const box = document.getElementById("cards");
  if(!box) return;
  box.innerHTML = "";
  cards.forEach(c=>{
    box.innerHTML += `
      <div class="card">
        <h3>${c.holder}</h3>
        <p>${c.number}</p>
        <div class="balance">$${c.balance}</div>
      </div>
    `;
  });
}

// Render transactions
function renderTransactions() {
  const list = document.getElementById("transactions");
  if(!list) return;
  list.innerHTML = "";
  transactions.forEach(t=>{
    list.innerHTML += `
      <div class="transaction-item">
        <span>${t.category} → ${t.to}</span>
        <span class="amount">-$${t.amount}</span>
      </div>
    `;
  });
}

// Init
document.addEventListener("DOMContentLoaded", ()=>{
  renderBalance();
  renderCards();
  renderTransactions();
});
