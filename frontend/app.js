const uploadArea = document.getElementById('upload-area');
const fileInput = document.getElementById('file-input');
const preview = document.getElementById('preview');
const uploadContent = document.getElementById('upload-content');
const analyzeBtn = document.getElementById('analyze-btn');
const loading = document.getElementById('loading');
const results = document.getElementById('results');

let selectedFile = null;

// File selection
uploadArea.addEventListener('click', () => fileInput.click());
fileInput.addEventListener('change', (e) => handleFile(e.target.files[0]));

// Drag and drop
uploadArea.addEventListener('dragover', (e) => {
  e.preventDefault();
  uploadArea.classList.add('drag-over');
});
uploadArea.addEventListener('dragleave', () => uploadArea.classList.remove('drag-over'));
uploadArea.addEventListener('drop', (e) => {
  e.preventDefault();
  uploadArea.classList.remove('drag-over');
  handleFile(e.dataTransfer.files[0]);
});

function handleFile(file) {
  if (!file || !file.type.startsWith('image/')) return;
  selectedFile = file;
  const url = URL.createObjectURL(file);
  preview.src = url;
  preview.classList.remove('hidden');
  uploadContent.classList.add('hidden');
  analyzeBtn.disabled = false;
}

// Analyze
analyzeBtn.addEventListener('click', async () => {
  if (!selectedFile) return;

  analyzeBtn.disabled = true;
  loading.classList.remove('hidden');
  results.classList.add('hidden');

  const formData = new FormData();
  formData.append('file', selectedFile);

  try {
    const response = await fetch('/api/analyze', { method: 'POST', body: formData });
    if (!response.ok) throw new Error(`Server error: ${response.status}`);
    const data = await response.json();
    renderResults(data);
  } catch (err) {
    alert('Analysis failed: ' + err.message);
  } finally {
    loading.classList.add('hidden');
    analyzeBtn.disabled = false;
  }
});

function renderResults(data) {
  // Summary
  document.getElementById('summary-text').textContent = data.summary;
  document.getElementById('violation-count').textContent = data.violation_count;

  const costLow = data.total_estimated_cost.low.toLocaleString();
  const costHigh = data.total_estimated_cost.high.toLocaleString();
  document.getElementById('total-cost').textContent =
    data.violation_count > 0 ? `$${costLow} - $${costHigh}` : '$0';

  // Risk badge
  const riskBadge = document.getElementById('risk-badge');
  riskBadge.textContent = (data.overall_risk || 'unknown').toUpperCase() + ' RISK';
  riskBadge.className = `px-4 py-1.5 rounded-full text-sm font-semibold risk-${data.overall_risk}`;

  // Positive features
  const positiveSection = document.getElementById('positive-section');
  const positiveList = document.getElementById('positive-list');
  positiveList.innerHTML = '';
  if (data.positive_features && data.positive_features.length > 0) {
    positiveSection.classList.remove('hidden');
    data.positive_features.forEach(feature => {
      const li = document.createElement('li');
      li.className = 'text-green-300';
      li.textContent = '✓ ' + feature;
      positiveList.appendChild(li);
    });
  } else {
    positiveSection.classList.add('hidden');
  }

  // Violations
  const violationsList = document.getElementById('violations-list');
  violationsList.innerHTML = '';

  data.violations
    .sort((a, b) => severityOrder(a.severity) - severityOrder(b.severity))
    .forEach(v => {
      const card = document.createElement('div');
      card.className = `rounded-xl p-5 bg-gray-900 border border-gray-800 severity-${v.severity}`;
      card.innerHTML = `
        <div class="flex items-center justify-between mb-3">
          <h3 class="text-lg font-semibold">${formatViolationType(v.violation_type)}</h3>
          <div class="flex items-center gap-2">
            <span class="text-xs text-gray-500">Confidence: ${Math.round(v.confidence * 100)}%</span>
            <span class="px-2 py-0.5 rounded text-xs font-medium severity-badge-${v.severity}">
              ${v.severity.toUpperCase()}
            </span>
          </div>
        </div>
        <p class="text-gray-300 mb-3">${v.description}</p>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-sm">
          <div class="bg-gray-800 rounded-lg p-3">
            <p class="text-gray-500 mb-1">ADA Section ${v.ada_section}</p>
            <p class="text-gray-300">${v.ada_title}</p>
            <p class="text-gray-500 text-xs mt-1">${v.ada_requirement}</p>
          </div>
          <div class="bg-gray-800 rounded-lg p-3">
            <p class="text-gray-500 mb-1">Est. Remediation Cost</p>
            <p class="text-amber-400 font-semibold">$${v.cost_low.toLocaleString()} - $${v.cost_high.toLocaleString()} <span class="text-gray-500 font-normal text-xs">${v.cost_unit}</span></p>
            <p class="text-gray-400 text-xs mt-1">${v.remediation}</p>
          </div>
        </div>
        ${v.needs_measurement ? '<p class="text-xs text-yellow-600 mt-2">⚠ Physical measurement needed to confirm this violation</p>' : ''}
      `;
      violationsList.appendChild(card);
    });

  // Disclaimer
  document.getElementById('disclaimer').textContent = data.disclaimer;

  results.classList.remove('hidden');
}

function severityOrder(s) {
  return { high: 0, medium: 1, low: 2 }[s] || 3;
}

function formatViolationType(type) {
  return type.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
}
