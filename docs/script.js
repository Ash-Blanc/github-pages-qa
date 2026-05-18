async function loadQA() {
  const res = await fetch('qa.json');
  const data = await res.json();
  const container = document.getElementById('qa-list');
  const countEl = document.getElementById('qa-count');
  const answeredEl = document.getElementById('answered-count');

  countEl.textContent = data.length;
  answeredEl.textContent = data.filter(d => d.a && d.a.trim()).length;

  if (data.length === 0) {
    container.innerHTML = `
      <div class="text-center py-16 text-zinc-600">
        <p class="text-sm uppercase tracking-wider mb-2">No threads yet</p>
        <p class="text-zinc-500">Be the first to suggest a question.</p>
      </div>
    `;
    return;
  }

  data.forEach((item, i) => {
    const div = document.createElement('div');
    div.className = 'group bg-zinc-900/40 border border-zinc-800 hover:border-zinc-600 rounded-2xl p-6 transition-all duration-200 hover:bg-zinc-900/60';
    div.innerHTML = `
      <div class="flex items-start gap-4">
        <div class="flex-shrink-0 w-10 h-10 rounded-full bg-gradient-to-br from-emerald-500/20 to-violet-500/20 border border-zinc-700 flex items-center justify-center text-xs font-mono text-zinc-400">
          #${i + 1}
        </div>
        <div class="flex-1 min-w-0">
          <h3 class="font-['Space_Grotesk'] text-lg font-semibold text-white mb-2 leading-snug">${escapeHtml(item.q)}</h3>
          <p class="text-zinc-400 text-sm leading-relaxed">${escapeHtml(item.a)}</p>
          <div class="mt-3 flex items-center gap-3 text-xs text-zinc-600">
            <span class="flex items-center gap-1">
              <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path></svg>
              Thread
            </span>
            <span>Synced from session</span>
          </div>
        </div>
      </div>
    `;
    container.appendChild(div);
  });
}

function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

function openModal() {
  document.getElementById('modal').classList.remove('hidden');
  document.getElementById('modal').classList.add('flex');
  document.getElementById('suggest-input').focus();
}

function closeModal() {
  document.getElementById('modal').classList.add('hidden');
  document.getElementById('modal').classList.remove('flex');
  document.getElementById('suggest-input').value = '';
}

async function submitSuggestion() {
  const text = document.getElementById('suggest-input').value.trim();
  if (!text) return;

  // For now: redirect to GitHub issue creation
  const title = encodeURIComponent(`[Q&A Suggestion] ${text.slice(0, 60)}`);
  const body = encodeURIComponent(`Suggested from the forum:\n\n> ${text}\n\nPlease review and add to qa.json.`);
  window.open(`https://github.com/Ash-Blanc/github-pages-qa/issues/new?title=${title}&body=${body}&labels=qa-suggestion`, '_blank');
  closeModal();
}

// Close modal on backdrop click
document.getElementById('modal').addEventListener('click', (e) => {
  if (e.target === document.getElementById('modal')) closeModal();
});

// Close on Escape
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') closeModal();
});

loadQA();
