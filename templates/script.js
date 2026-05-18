// Minimal Q&A renderer
async function loadQA() {
  const res = await fetch('qa.json');
  const data = await res.json();
  const container = document.getElementById('qa-list');

  data.forEach(item => {
    const div = document.createElement('div');
    div.className = 'bg-zinc-900 p-4 rounded-xl border border-zinc-800';
    div.innerHTML = `
      <div class="font-medium">${item.q}</div>
      <div class="text-sm text-zinc-400 mt-2">${item.a}</div>
    `;
    container.appendChild(div);
  });
}

loadQA();