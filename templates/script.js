const REPO = 'Ash-Blanc/github-pages-qa';
let qaData = [];
let pendingData = [];
let lastHash = '';

// --- Utils ---
const $ = (s) => document.querySelector(s);
const $$ = (s) => document.querySelectorAll(s);
const esc = (t) => { const d=document.createElement('div'); d.textContent=t; return d.innerHTML; };
const fmtDate = (d) => new Date(d).toLocaleDateString(undefined, {month:'short', day:'numeric', year:'numeric'});
const toast = (msg, type='info') => {
  const el = document.createElement('div');
  el.className = `fixed bottom-6 right-6 px-4 py-3 rounded-xl text-sm font-medium z-50 transition-all duration-300 translate-y-10 opacity-0 ${
    type==='error' ? 'bg-red-500/90 text-white' : type==='success' ? 'bg-emerald-500/90 text-black' : 'bg-zinc-800 text-zinc-200 border border-zinc-700'
  }`;
  el.textContent = msg;
  document.body.appendChild(el);
  requestAnimationFrame(() => { el.classList.remove('translate-y-10','opacity-0'); });
  setTimeout(() => { el.classList.add('translate-y-10','opacity-0'); setTimeout(()=>el.remove(),300); }, 3000);
};

// --- Loading skeleton ---
function showSkeleton() {
  $('#qa-list').innerHTML = Array(4).fill(0).map((_,i)=>`
    <div class="bg-zinc-900/40 border border-zinc-800 rounded-2xl p-6 animate-pulse">
      <div class="flex items-start gap-4">
        <div class="w-10 h-10 rounded-full bg-zinc-800"></div>
        <div class="flex-1 space-y-3">
          <div class="h-5 bg-zinc-800 rounded w-3/4"></div>
          <div class="h-3 bg-zinc-800 rounded w-full"></div>
          <div class="h-3 bg-zinc-800 rounded w-2/3"></div>
        </div>
      </div>
    </div>
  `).join('');
}

// --- Core: Load Q&A ---
async function loadQA(force=false) {
  try {
    const res = await fetch('qa.json?t='+Date.now());
    if (!res.ok) throw new Error(res.status);
    const data = await res.json();
    if (!Array.isArray(data)) throw new Error('bad format');

    // Detect new items
    const oldIds = new Set(qaData.map(d => d.q+d.a));
    const newItems = data.filter(d => !oldIds.has(d.q+d.a));
    qaData = data;

    render();
    updateStats();

    if (!force && newItems.length > 0 && qaData.length > oldIds.size) {
      toast(`${newItems.length} new thread${newItems.length>1?'s':''}`, 'success');
    }
  } catch (e) {
    $('#qa-list').innerHTML = `
      <div class="text-center py-16">
        <p class="text-red-400 font-medium mb-2">Failed to load threads</p>
        <p class="text-zinc-600 text-sm">${esc(e.message)}</p>
        <button onclick="loadQA(true)" class="mt-4 px-4 py-2 bg-zinc-800 hover:bg-zinc-700 rounded-xl text-sm transition-colors">Retry</button>
      </div>`;
    toast('Load failed', 'error');
  }
}

// --- Core: Load pending from GitHub Issues ---
async function loadPending() {
  try {
    const res = await fetch(`https://api.github.com/repos/${REPO}/issues?labels=qa-suggestion&state=open&per_page=10`);
    if (!res.ok) throw new Error(res.status);
    pendingData = await res.json();
    renderPending();
  } catch (e) {
    $('#pending-list').innerHTML = '<p class="text-zinc-600 text-sm text-center py-4">Could not load pending suggestions</p>';
  }
}

// --- Render threads ---
function render() {
  const q = $('#search-input').value.toLowerCase().trim();
  const tag = $('#tag-filter').value;
  let filtered = qaData;

  if (q) filtered = filtered.filter(d => (d.q+' '+d.a).toLowerCase().includes(q));
  if (tag) filtered = filtered.filter(d => (d.tags||[]).includes(tag));

  const container = $('#qa-list');
  if (filtered.length === 0) {
    container.innerHTML = `
      <div class="text-center py-20">
        <p class="text-zinc-500 text-lg mb-2">No threads match</p>
        <p class="text-zinc-600 text-sm">Try a different search or suggest a new question.</p>
      </div>`;
    return;
  }

  container.innerHTML = filtered.map((item, i) => {
    const hash = `#thread-${i}`;
    const isOpen = location.hash === hash;
    const isNew = !localStorage.getItem('seen:'+hash);
    const tags = (item.tags || []).map(t =>
      `<span class="px-2 py-0.5 bg-zinc-800 border border-zinc-700 rounded-md text-[11px] text-zinc-400 uppercase tracking-wider">${esc(t)}</span>`
    ).join('');

    return `
      <div id="thread-${i}" class="group bg-zinc-900/40 border ${isOpen?'border-emerald-500/40 ring-1 ring-emerald-500/10':'border-zinc-800 hover:border-zinc-600'} rounded-2xl transition-all duration-200 hover:bg-zinc-900/60">
        <div class="p-6 cursor-pointer" onclick="toggleThread(${i})">
          <div class="flex items-start gap-4">
            <div class="flex-shrink-0 w-10 h-10 rounded-full bg-gradient-to-br from-emerald-500/20 to-violet-500/20 border border-zinc-700 flex items-center justify-center text-xs font-mono text-zinc-400">
              ${isNew ? `<span class="w-2 h-2 rounded-full bg-emerald-400"></span>` : `#${i+1}`}
            </div>
            <div class="flex-1 min-w-0">
              <div class="flex items-start justify-between gap-3">
                <h3 class="font-['Space_Grotesk'] text-lg font-semibold text-white leading-snug">${esc(item.q)}</h3>
                <button onclick="event.stopPropagation(); copyLink('${hash}')" class="opacity-0 group-hover:opacity-100 p-1.5 hover:bg-zinc-800 rounded-lg transition-all" title="Copy link">
                  <svg class="w-4 h-4 text-zinc-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"></path></svg>
                </button>
              </div>
              <div class="flex items-center gap-2 mt-2 mb-3">${tags}</div>
              <div class="text-zinc-400 text-sm leading-relaxed ${isOpen?'':'line-clamp-2'}">${esc(item.a)}</div>
              <div class="mt-3 flex items-center gap-4 text-xs text-zinc-600">
                <span class="flex items-center gap-1"><svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path></svg> Thread</span>
                ${item.date ? `<span>${fmtDate(item.date)}</span>` : ''}
                <span class="ml-auto text-zinc-700">${isOpen ? 'Click to collapse' : 'Click to expand'}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    `;
  }).join('');

  // Mark opened thread as seen
  if (isOpen && location.hash.startsWith('#thread-')) {
    localStorage.setItem('seen:'+location.hash, '1');
  }
}

// --- Render pending sidebar ---
function renderPending() {
  const container = $('#pending-list');
  if (!pendingData.length) {
    container.innerHTML = '<p class="text-zinc-600 text-sm text-center py-4">No pending suggestions</p>';
    return;
  }
  container.innerHTML = pendingData.map(issue => `
    <a href="${issue.html_url}" target="_blank" class="block p-3 bg-zinc-900/40 border border-zinc-800 rounded-xl hover:border-zinc-600 transition-colors group">
      <p class="text-sm text-zinc-300 group-hover:text-white line-clamp-2">${esc(issue.title.replace('[Q&A Suggestion] ',''))}</p>
      <p class="text-xs text-zinc-600 mt-1">#${issue.number} · ${fmtDate(issue.created_at)}</p>
    </a>
  `).join('');
}

// --- Stats ---
function updateStats() {
  $('#qa-count').textContent = qaData.length;
  $('#answered-count').textContent = qaData.filter(d => d.a && d.a.trim()).length;
  const tags = [...new Set(qaData.flatMap(d => d.tags || []))];
  $('#tag-filter').innerHTML = '<option value="">All tags</option>' +
    tags.map(t => `<option value="${esc(t)}">${esc(t)}</option>`).join('');
}

// --- Interactions ---
function toggleThread(i) {
  const hash = `#thread-${i}`;
  if (location.hash === hash) {
    history.pushState('', document.title, window.location.pathname + window.location.search);
  } else {
    location.hash = hash;
  }
  render();
}

function copyLink(hash) {
  const url = location.origin + location.pathname + hash;
  navigator.clipboard.writeText(url).then(() => toast('Link copied'));
}

function openModal() {
  $('#modal').classList.remove('hidden');
  $('#modal').classList.add('flex');
  $('#suggest-input').focus();
}

function closeModal() {
  $('#modal').classList.add('hidden');
  $('#modal').classList.remove('flex');
  $('#suggest-input').value = '';
}

function submitSuggestion() {
  const text = $('#suggest-input').value.trim();
  if (!text) return;
  const title = encodeURIComponent(`[Q&A Suggestion] ${text.slice(0,80)}`);
  const body = encodeURIComponent(`Suggested from the live forum:\n\n> ${text}\n\n---\n*Submitted via forum suggestion form*`);
  window.open(`https://github.com/${REPO}/issues/new?title=${title}&body=${body}&labels=qa-suggestion`, '_blank');
  closeModal();
  toast('Opening GitHub issue...', 'success');
}

// --- Event wiring ---
$('#search-input').addEventListener('input', () => render());
$('#tag-filter').addEventListener('change', () => render());
$('#modal').addEventListener('click', (e) => { if (e.target === $('#modal')) closeModal(); });
document.addEventListener('keydown', (e) => { if (e.key === 'Escape') closeModal(); });
window.addEventListener('hashchange', render);

// --- Init ---
showSkeleton();
loadQA(true);
loadPending();
setInterval(() => loadQA(false), 30000); // Poll every 30s
setInterval(loadPending, 60000); // Poll pending every 60s
