/* ADA Compliance Auditor — Mobile-First PWA */

// ── DOM References ──────────────────────────────────────────────
const uploadArea = document.getElementById('upload-area');
const uploadContent = document.getElementById('upload-content');
const fileInput = document.getElementById('file-input');
const preview = document.getElementById('preview');
const locationField = document.getElementById('location-field');
const analyzeBtn = document.getElementById('analyze-btn');
const progressEl = document.getElementById('progress');
const resultsEl = document.getElementById('results');
const violationsList = document.getElementById('violations-list');
const positiveSection = document.getElementById('positive-section');
const positiveList = document.getElementById('positive-list');
const followupSection = document.getElementById('followup-section');
const followupList = document.getElementById('followup-list');
const downloadPdfBtn = document.getElementById('download-pdf-btn');
const newScanBtn = document.getElementById('new-scan-btn');
const historyList = document.getElementById('history-list');
const historyEmpty = document.getElementById('history-empty');

let selectedFile = null;
let currentPdfUrl = null;
let currentReportData = null;

/** Safely remove all child nodes from an element */
function clearChildren(el) {
  while (el.firstChild) {
    el.removeChild(el.firstChild);
  }
}

// ── Navigation ──────────────────────────────────────────────────
document.querySelectorAll('.nav-btn').forEach(function(btn) {
  btn.addEventListener('click', function() {
    var targetId = btn.getAttribute('data-screen');

    // Toggle active screen
    document.querySelectorAll('.screen').forEach(function(s) { s.classList.remove('active'); });
    document.getElementById(targetId).classList.add('active');

    // Toggle active nav
    document.querySelectorAll('.nav-btn').forEach(function(b) { b.classList.remove('active'); });
    btn.classList.add('active');

    // Load history when switching to that screen
    if (targetId === 'history-screen') {
      loadHistory('all');
      // Reset filter buttons
      document.querySelectorAll('.filter-btn').forEach(function(f) { f.classList.remove('active'); });
      var allBtn = document.querySelector('.filter-btn[data-filter="all"]');
      if (allBtn) allBtn.classList.add('active');
    }
  });
});

// ── File Upload ─────────────────────────────────────────────────
uploadArea.addEventListener('click', function() { fileInput.click(); });
fileInput.addEventListener('change', function(e) { handleFile(e.target.files[0]); });

// Drag and drop
uploadArea.addEventListener('dragover', function(e) {
  e.preventDefault();
  uploadArea.classList.add('drag-over');
});
uploadArea.addEventListener('dragleave', function() { uploadArea.classList.remove('drag-over'); });
uploadArea.addEventListener('drop', function(e) {
  e.preventDefault();
  uploadArea.classList.remove('drag-over');
  handleFile(e.dataTransfer.files[0]);
});

function handleFile(file) {
  if (!file || !file.type.startsWith('image/')) return;
  selectedFile = file;
  var url = URL.createObjectURL(file);
  preview.src = url;
  preview.classList.remove('hidden');
  uploadContent.classList.add('hidden');
  analyzeBtn.disabled = false;
}

// ── Analyze (SSE Streaming) ─────────────────────────────────────
analyzeBtn.addEventListener('click', async function() {
  if (!selectedFile) return;

  analyzeBtn.disabled = true;
  analyzeBtn.textContent = 'Analyzing...';
  resultsEl.classList.add('hidden');
  progressEl.classList.remove('hidden');
  resetProgress();

  var formData = new FormData();
  formData.append('file', selectedFile);
  var loc = locationField.value.trim();
  if (loc) formData.append('location_label', loc);

  var sessionId = getSessionId();
  formData.append('session_id', sessionId);

  try {
    var response = await fetch('/api/analyze', { method: 'POST', body: formData });
    if (!response.ok) throw new Error('Server error: ' + response.status);

    var reader = response.body.getReader();
    var decoder = new TextDecoder();
    var buffer = '';

    while (true) {
      var chunk = await reader.read();
      if (chunk.done) break;

      buffer += decoder.decode(chunk.value, { stream: true });
      var lines = buffer.split('\n');
      buffer = lines.pop(); // keep incomplete line in buffer

      for (var i = 0; i < lines.length; i++) {
        var line = lines[i];
        if (!line.startsWith('data: ')) continue;
        var jsonStr = line.slice(6).trim();
        if (!jsonStr) continue;

        try {
          var event = JSON.parse(jsonStr);
          handleSSEEvent(event);
        } catch (parseErr) {
          // skip malformed JSON
        }
      }
    }

    // Process any remaining buffer
    if (buffer.startsWith('data: ')) {
      try {
        var evt = JSON.parse(buffer.slice(6).trim());
        handleSSEEvent(evt);
      } catch (e) { /* ignore */ }
    }
  } catch (err) {
    alert('Analysis failed: ' + err.message);
    progressEl.classList.add('hidden');
  } finally {
    analyzeBtn.disabled = false;
    analyzeBtn.textContent = 'Analyze for ADA Compliance';
  }
});

function handleSSEEvent(event) {
  var type = event.type || event.event;

  if (type === 'scene_classification') {
    var label = (event.data && event.data.space_type) || event.space_type || 'Identified';
    markStepDone(1, formatType(label));
  } else if (type === 'violation_detection') {
    var count = (event.data && event.data.violation_count) || event.violation_count || 0;
    markStepDone(2, count + ' violation' + (count !== 1 ? 's' : '') + ' found');
  } else if (type === 'complete' || type === 'analysis_complete') {
    markStepDone(3, 'Complete');
    var data = event.data || event;
    currentReportData = data;
    currentPdfUrl = data.pdf_url || null;
    renderResults(data);
    saveToHistory(data);
  } else if (type === 'error') {
    alert('Analysis error: ' + ((event.data && event.data.message) || event.message || 'Unknown error'));
  }
}

// ── Progress Steps ──────────────────────────────────────────────
function resetProgress() {
  document.querySelectorAll('.step-indicator').forEach(function(step) {
    var icon = step.querySelector('.step-icon');
    icon.textContent = step.getAttribute('data-step');
    icon.className = 'step-icon w-7 h-7 rounded-full bg-gray-800 flex items-center justify-center text-gray-500 font-bold text-xs shrink-0';
    step.querySelector('.step-label').textContent = '';
  });
  // Activate first step
  var first = document.querySelector('.step-indicator[data-step="1"] .step-icon');
  if (first) {
    first.className = 'step-icon w-7 h-7 rounded-full bg-blue-600 flex items-center justify-center text-white font-bold text-xs shrink-0';
  }
}

function markStepDone(num, label) {
  var step = document.querySelector('.step-indicator[data-step="' + num + '"]');
  if (!step) return;

  var icon = step.querySelector('.step-icon');
  icon.textContent = '\u2713';
  icon.className = 'step-icon w-7 h-7 rounded-full bg-green-600 flex items-center justify-center text-white font-bold text-xs shrink-0';
  step.querySelector('.step-label').textContent = label;

  // Activate next step
  var next = document.querySelector('.step-indicator[data-step="' + (num + 1) + '"] .step-icon');
  if (next) {
    next.className = 'step-icon w-7 h-7 rounded-full bg-blue-600 flex items-center justify-center text-white font-bold text-xs shrink-0';
  }
}

// ── Render Results ──────────────────────────────────────────────
function renderResults(data) {
  // Summary
  document.getElementById('summary-text').textContent = data.summary || '';

  var violations = data.violations || [];
  var confirmed = violations.filter(function(v) { return v.confidence >= 0.7; });
  var potential = violations.filter(function(v) { return v.confidence < 0.7; });

  document.getElementById('confirmed-count').textContent = confirmed.length;
  document.getElementById('potential-count').textContent = potential.length;

  // Cost range
  var costEl = document.getElementById('total-cost');
  if (data.total_estimated_cost) {
    var low = (data.total_estimated_cost.low || 0).toLocaleString();
    var high = (data.total_estimated_cost.high || 0).toLocaleString();
    costEl.textContent = violations.length > 0 ? '$' + low + '-$' + high : '$0';
  } else {
    costEl.textContent = '$0';
  }

  // Risk badge
  var riskBadge = document.getElementById('risk-badge');
  var risk = data.overall_risk || 'unknown';
  riskBadge.textContent = risk.toUpperCase() + ' RISK';
  riskBadge.className = 'px-3 py-1 rounded-full text-xs font-semibold risk-' + risk;

  // PDF button
  if (currentPdfUrl) {
    downloadPdfBtn.classList.remove('hidden');
  } else {
    downloadPdfBtn.classList.add('hidden');
  }

  // Positive features
  clearChildren(positiveList);
  if (data.positive_features && data.positive_features.length > 0) {
    positiveSection.classList.remove('hidden');
    data.positive_features.forEach(function(feature) {
      var li = document.createElement('li');
      li.className = 'text-green-300 text-sm';
      li.textContent = '\u2713 ' + feature;
      positiveList.appendChild(li);
    });
  } else {
    positiveSection.classList.add('hidden');
  }

  // Violations
  clearChildren(violationsList);

  var sorted = violations.slice().sort(function(a, b) { return severityOrder(a.severity) - severityOrder(b.severity); });

  if (confirmed.length > 0) {
    var confirmedHeader = document.createElement('h3');
    confirmedHeader.className = 'text-lg font-semibold text-red-400';
    confirmedHeader.textContent = 'Confirmed Violations';
    violationsList.appendChild(confirmedHeader);
  }

  sorted.filter(function(v) { return v.confidence >= 0.7; }).forEach(function(v) {
    violationsList.appendChild(buildViolationCard(v));
  });

  if (potential.length > 0) {
    var potentialHeader = document.createElement('h3');
    potentialHeader.className = 'text-lg font-semibold text-amber-400 mt-4';
    potentialHeader.textContent = 'Potential Violations';
    violationsList.appendChild(potentialHeader);
  }

  sorted.filter(function(v) { return v.confidence < 0.7; }).forEach(function(v) {
    violationsList.appendChild(buildViolationCard(v));
  });

  // Follow-up suggestions
  clearChildren(followupList);
  if (data.follow_up_suggestions && data.follow_up_suggestions.length > 0) {
    followupSection.classList.remove('hidden');
    data.follow_up_suggestions.forEach(function(suggestion) {
      var li = document.createElement('li');
      li.className = 'text-blue-300 text-sm';
      li.textContent = '\u2022 ' + suggestion;
      followupList.appendChild(li);
    });
  } else {
    followupSection.classList.add('hidden');
  }

  // Disclaimer
  document.getElementById('disclaimer').textContent =
    data.disclaimer || 'This is an automated analysis and should not replace a professional ADA inspection.';

  resultsEl.classList.remove('hidden');
  progressEl.classList.add('hidden');
}

function buildViolationCard(v) {
  var card = document.createElement('div');
  card.className = 'rounded-xl p-4 bg-gray-900 border border-gray-800 severity-' + (v.severity || 'medium');

  // Header row
  var header = document.createElement('div');
  header.className = 'flex items-center justify-between mb-2';

  var title = document.createElement('h4');
  title.className = 'text-base font-semibold';
  title.textContent = formatType(v.violation_type || '');

  var badges = document.createElement('div');
  badges.className = 'flex items-center gap-2';

  var confSpan = document.createElement('span');
  confSpan.className = 'text-xs text-gray-500';
  confSpan.textContent = Math.round((v.confidence || 0) * 100) + '%';

  var sevBadge = document.createElement('span');
  sevBadge.className = 'px-2 py-0.5 rounded text-xs font-medium severity-badge-' + (v.severity || 'medium');
  sevBadge.textContent = (v.severity || 'medium').toUpperCase();

  badges.appendChild(confSpan);
  badges.appendChild(sevBadge);
  header.appendChild(title);
  header.appendChild(badges);
  card.appendChild(header);

  // Description
  var desc = document.createElement('p');
  desc.className = 'text-gray-300 text-sm mb-2';
  desc.textContent = v.description || '';
  card.appendChild(desc);

  // Reasoning (italic)
  if (v.reasoning) {
    var reasoning = document.createElement('p');
    reasoning.className = 'text-gray-400 text-xs italic mb-2';
    reasoning.textContent = v.reasoning;
    card.appendChild(reasoning);
  }

  // Code references grid
  var grid = document.createElement('div');
  grid.className = 'grid grid-cols-1 gap-2 text-sm';

  // ADA Section
  if (v.ada_section) {
    var adaBox = document.createElement('div');
    adaBox.className = 'bg-gray-800 rounded-lg p-2.5';

    var adaLabel = document.createElement('p');
    adaLabel.className = 'text-gray-500 text-xs';
    adaLabel.textContent = 'ADA Section ' + v.ada_section;
    adaBox.appendChild(adaLabel);

    if (v.ada_title) {
      var adaTitle = document.createElement('p');
      adaTitle.className = 'text-gray-300 text-xs';
      adaTitle.textContent = v.ada_title;
      adaBox.appendChild(adaTitle);
    }

    grid.appendChild(adaBox);
  }

  // CBC Section
  if (v.cbc_section) {
    var cbcBox = document.createElement('div');
    cbcBox.className = 'bg-gray-800 rounded-lg p-2.5';

    var cbcLabel = document.createElement('p');
    cbcLabel.className = 'text-gray-500 text-xs';
    cbcLabel.textContent = 'CBC Section ' + v.cbc_section;
    cbcBox.appendChild(cbcLabel);

    if (v.cbc_title) {
      var cbcTitle = document.createElement('p');
      cbcTitle.className = 'text-gray-300 text-xs';
      cbcTitle.textContent = v.cbc_title;
      cbcBox.appendChild(cbcTitle);
    }

    grid.appendChild(cbcBox);
  }

  if (grid.children.length > 0) {
    card.appendChild(grid);
  }

  // Stricter note
  if (v.stricter_note) {
    var stricter = document.createElement('p');
    stricter.className = 'text-red-400 text-xs mt-2 font-medium';
    stricter.textContent = v.stricter_note;
    card.appendChild(stricter);
  }

  // Cost
  if (v.cost_low != null && v.cost_high != null) {
    var costRow = document.createElement('div');
    costRow.className = 'mt-2 flex items-center justify-between';

    var costText = document.createElement('span');
    costText.className = 'text-amber-400 text-sm font-semibold';
    costText.textContent = '$' + (v.cost_low || 0).toLocaleString() + ' - $' + (v.cost_high || 0).toLocaleString();

    var costUnit = document.createElement('span');
    costUnit.className = 'text-gray-500 text-xs';
    costUnit.textContent = v.cost_unit || '';

    costRow.appendChild(costText);
    costRow.appendChild(costUnit);
    card.appendChild(costRow);
  }

  // Remediation
  if (v.remediation) {
    var rem = document.createElement('p');
    rem.className = 'text-gray-400 text-xs mt-1';
    rem.textContent = v.remediation;
    card.appendChild(rem);
  }

  return card;
}

// ── PDF Download ────────────────────────────────────────────────
downloadPdfBtn.addEventListener('click', function() {
  if (!currentPdfUrl) return;
  var a = document.createElement('a');
  a.href = currentPdfUrl;
  a.download = '';
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
});

// ── New Scan ────────────────────────────────────────────────────
newScanBtn.addEventListener('click', function() {
  selectedFile = null;
  currentPdfUrl = null;
  currentReportData = null;
  fileInput.value = '';
  preview.src = '';
  preview.classList.add('hidden');
  uploadContent.classList.remove('hidden');
  locationField.value = '';
  analyzeBtn.disabled = true;
  resultsEl.classList.add('hidden');
  progressEl.classList.add('hidden');
  downloadPdfBtn.classList.add('hidden');
  clearChildren(violationsList);
  clearChildren(positiveList);
  clearChildren(followupList);
  window.scrollTo(0, 0);
});

// ── History ─────────────────────────────────────────────────────
async function saveToHistory(report) {
  try {
    // Create thumbnail from preview image
    var thumbnail = '';
    if (preview.src && !preview.classList.contains('hidden')) {
      try {
        var canvas = document.createElement('canvas');
        canvas.width = 120;
        canvas.height = 120;
        var ctx = canvas.getContext('2d');
        var img = preview;
        var size = Math.min(img.naturalWidth, img.naturalHeight);
        var sx = (img.naturalWidth - size) / 2;
        var sy = (img.naturalHeight - size) / 2;
        ctx.drawImage(img, sx, sy, size, size, 0, 0, 120, 120);
        thumbnail = canvas.toDataURL('image/jpeg', 0.6);
      } catch (e) {
        // thumbnail creation failed, continue without it
      }
    }

    var violations = report.violations || [];
    var confirmedCount = violations.filter(function(v) { return v.confidence >= 0.7; }).length;
    var potentialCount = violations.filter(function(v) { return v.confidence < 0.7; }).length;

    var record = {
      id: report.report_id || report.id || crypto.randomUUID(),
      date: new Date().toISOString(),
      thumbnail: thumbnail,
      location: locationField.value.trim() || 'Unknown location',
      spaceType: report.space_type || report.scene_type || '',
      riskLevel: report.overall_risk || 'unknown',
      confirmedCount: confirmedCount,
      potentialCount: potentialCount,
      violationCount: violations.length,
      costRange: report.total_estimated_cost
        ? '$' + (report.total_estimated_cost.low || 0).toLocaleString() + ' - $' + (report.total_estimated_cost.high || 0).toLocaleString()
        : '$0',
      pdfUrl: report.pdf_url || null,
      reportData: report
    };

    await saveReport(record);
  } catch (e) {
    console.error('Failed to save to history:', e);
  }
}

async function loadHistory(filter) {
  try {
    var reports = await getAllReports();

    if (filter && filter !== 'all') {
      reports = reports.filter(function(r) { return r.riskLevel === filter; });
    }

    clearChildren(historyList);

    if (reports.length === 0) {
      historyEmpty.classList.remove('hidden');
      return;
    }

    historyEmpty.classList.add('hidden');

    reports.forEach(function(r) {
      var card = document.createElement('div');
      card.className = 'bg-gray-900 border border-gray-800 rounded-xl p-3 flex gap-3 cursor-pointer hover:bg-gray-800 transition';
      card.addEventListener('click', function() { viewHistoryReport(r); });

      // Thumbnail
      if (r.thumbnail) {
        var img = document.createElement('img');
        img.src = r.thumbnail;
        img.className = 'w-16 h-16 rounded-lg object-cover shrink-0';
        img.alt = 'Report thumbnail';
        card.appendChild(img);
      }

      // Info
      var info = document.createElement('div');
      info.className = 'flex-1 min-w-0';

      var topRow = document.createElement('div');
      topRow.className = 'flex items-center justify-between mb-1';

      var loc = document.createElement('p');
      loc.className = 'text-sm font-medium text-gray-200 truncate';
      loc.textContent = r.location || 'Unknown';

      var badge = document.createElement('span');
      badge.className = 'px-2 py-0.5 rounded-full text-xs font-medium risk-' + (r.riskLevel || 'unknown') + ' shrink-0 ml-2';
      badge.textContent = (r.riskLevel || '?').toUpperCase();

      topRow.appendChild(loc);
      topRow.appendChild(badge);
      info.appendChild(topRow);

      var dateP = document.createElement('p');
      dateP.className = 'text-xs text-gray-500';
      var d = new Date(r.date);
      dateP.textContent = d.toLocaleDateString() + ' ' + d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
      info.appendChild(dateP);

      var meta = document.createElement('div');
      meta.className = 'flex gap-3 mt-1 text-xs text-gray-400';

      if (r.spaceType) {
        var sp = document.createElement('span');
        sp.textContent = formatType(r.spaceType);
        meta.appendChild(sp);
      }

      var vc = document.createElement('span');
      vc.textContent = (r.violationCount || 0) + ' violations';
      meta.appendChild(vc);

      if (r.costRange && r.costRange !== '$0') {
        var cost = document.createElement('span');
        cost.className = 'text-amber-400';
        cost.textContent = r.costRange;
        meta.appendChild(cost);
      }

      info.appendChild(meta);
      card.appendChild(info);
      historyList.appendChild(card);
    });
  } catch (e) {
    console.error('Failed to load history:', e);
  }
}

function viewHistoryReport(r) {
  // Switch to scan screen
  document.querySelectorAll('.screen').forEach(function(s) { s.classList.remove('active'); });
  document.getElementById('scan-screen').classList.add('active');
  document.querySelectorAll('.nav-btn').forEach(function(b) { b.classList.remove('active'); });
  document.querySelector('.nav-btn[data-screen="scan-screen"]').classList.add('active');

  // Load thumbnail as preview
  if (r.thumbnail) {
    preview.src = r.thumbnail;
    preview.classList.remove('hidden');
    uploadContent.classList.add('hidden');
  }

  // Load location
  locationField.value = r.location || '';

  // Set PDF url
  currentPdfUrl = r.pdfUrl || null;
  currentReportData = r.reportData || null;

  // Render results
  if (r.reportData) {
    progressEl.classList.add('hidden');
    renderResults(r.reportData);
  }
}

// History filter buttons
document.querySelectorAll('.filter-btn').forEach(function(btn) {
  btn.addEventListener('click', function() {
    document.querySelectorAll('.filter-btn').forEach(function(f) { f.classList.remove('active'); });
    btn.classList.add('active');
    loadHistory(btn.getAttribute('data-filter'));
  });
});

// ── Session ID ──────────────────────────────────────────────────
function getSessionId() {
  var id = localStorage.getItem('ada-session-id');
  if (!id) {
    id = crypto.randomUUID();
    localStorage.setItem('ada-session-id', id);
  }
  return id;
}

// ── Service Worker ──────────────────────────────────────────────
if ('serviceWorker' in navigator) {
  window.addEventListener('load', function() {
    navigator.serviceWorker.register('/static/sw.js').catch(function(err) {
      console.warn('SW registration failed:', err);
    });
  });
}

// ── Helpers ─────────────────────────────────────────────────────
function severityOrder(s) {
  return { high: 0, medium: 1, low: 2 }[s] || 3;
}

function formatType(type) {
  if (!type) return '';
  return type.replace(/_/g, ' ').replace(/\b\w/g, function(c) { return c.toUpperCase(); });
}
