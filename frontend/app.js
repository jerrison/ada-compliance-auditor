/* ADA Compliance Auditor — Mobile-First PWA */

// ── DOM References ──────────────────────────────────────────────
var uploadArea = document.getElementById('upload-area');
var uploadContent = document.getElementById('upload-content');
var fileInput = document.getElementById('file-input');
var preview = document.getElementById('preview');
var locationField = document.getElementById('location-field');
var analyzeBtn = document.getElementById('analyze-btn');
var progressEl = document.getElementById('progress');
var resultsEl = document.getElementById('results');
var violationsList = document.getElementById('violations-list');
var positiveSection = document.getElementById('positive-section');
var positiveList = document.getElementById('positive-list');
var followupSection = document.getElementById('followup-section');
var followupList = document.getElementById('followup-list');
var downloadPdfBtn = document.getElementById('download-pdf-btn');
var newScanBtn = document.getElementById('new-scan-btn');
var historyList = document.getElementById('history-list');
var historyEmpty = document.getElementById('history-empty');
var complianceBanner = document.getElementById('compliance-banner');
var complianceIcon = document.getElementById('compliance-icon');
var complianceLabel = document.getElementById('compliance-label');
var complianceSublabel = document.getElementById('compliance-sublabel');
var positiveCount = document.getElementById('positive-count');

var selectedFile = null;
var currentPdfUrl = null;
var currentReportData = null;
var detectedState = '';
var detectedLocation = null;

function clearChildren(el) {
  while (el.firstChild) el.removeChild(el.firstChild);
}

// ── Navigation ──────────────────────────────────────────────────
document.querySelectorAll('.nav-btn').forEach(function(btn) {
  btn.addEventListener('click', function() {
    var targetId = btn.getAttribute('data-screen');
    document.querySelectorAll('.screen').forEach(function(s) { s.classList.remove('active'); });
    document.getElementById(targetId).classList.add('active');
    document.querySelectorAll('.nav-btn').forEach(function(b) { b.classList.remove('active'); });
    btn.classList.add('active');
    if (targetId === 'history-screen') {
      loadHistory('all');
      document.querySelectorAll('.filter-btn').forEach(function(f) { f.classList.remove('active'); });
      var allBtn = document.querySelector('.filter-btn[data-filter="all"]');
      if (allBtn) allBtn.classList.add('active');
    }
  });
});

// ── File Upload ─────────────────────────────────────────────────
uploadArea.addEventListener('click', function() { fileInput.click(); });
fileInput.addEventListener('change', function(e) { handleFile(e.target.files[0]); });
uploadArea.addEventListener('dragover', function(e) { e.preventDefault(); uploadArea.classList.add('drag-over'); });
uploadArea.addEventListener('dragleave', function() { uploadArea.classList.remove('drag-over'); });
uploadArea.addEventListener('drop', function(e) {
  e.preventDefault();
  uploadArea.classList.remove('drag-over');
  handleFile(e.dataTransfer.files[0]);
});

function handleFile(file) {
  if (!file || !file.type.startsWith('image/')) return;
  selectedFile = file;
  preview.src = URL.createObjectURL(file);
  preview.classList.remove('hidden');
  uploadContent.classList.add('hidden');
  analyzeBtn.disabled = false;
}

// ── Google Places Autocomplete ───────────────────────────────────
var placesAutocomplete = null;
var locateBtn = document.getElementById('locate-btn');
var locateBtnText = document.getElementById('locate-btn-text');
var locationDetail = document.getElementById('location-detail');
var standardLabel = document.getElementById('standard-label');

function initPlacesAutocomplete(apiKey) {
  if (!apiKey) return;
  var script = document.createElement('script');
  script.src = 'https://maps.googleapis.com/maps/api/js?key=' + apiKey + '&libraries=places&callback=onGoogleMapsLoaded';
  script.async = true;
  script.defer = true;
  document.head.appendChild(script);
}

window.onGoogleMapsLoaded = function() {
  placesAutocomplete = new google.maps.places.Autocomplete(locationField, {
    types: ['address'],
    fields: ['address_components', 'formatted_address', 'geometry'],
  });
  placesAutocomplete.addListener('place_changed', function() {
    var place = placesAutocomplete.getPlace();
    if (!place || !place.address_components) return;
    var city = '', county = '', state = '';
    for (var i = 0; i < place.address_components.length; i++) {
      var types = place.address_components[i].types;
      if (types.indexOf('locality') !== -1) city = place.address_components[i].long_name;
      else if (types.indexOf('administrative_area_level_2') !== -1) county = place.address_components[i].long_name;
      else if (types.indexOf('administrative_area_level_1') !== -1) state = place.address_components[i].long_name;
    }
    detectedState = state;
    detectedLocation = { city: city, county: county, state: state, full: place.formatted_address || '' };
    var parts = [city, county, state].filter(Boolean);
    locationDetail.textContent = parts.join(' \u00B7 ');
    locationDetail.classList.remove('hidden');
    updateStandardLabel(state);
  });
};

fetch('/api/config')
  .then(function(r) { return r.json(); })
  .then(function(c) { if (c.google_maps_api_key) initPlacesAutocomplete(c.google_maps_api_key); })
  .catch(function() {});

// ── Geolocation (Locate Me) ─────────────────────────────────────
locateBtn.addEventListener('click', function() {
  if (!navigator.geolocation) { alert('Geolocation not supported.'); return; }
  locateBtnText.textContent = '...';
  locateBtn.disabled = true;
  navigator.geolocation.getCurrentPosition(
    function(pos) { reverseGeocode(pos.coords.latitude, pos.coords.longitude); },
    function(err) {
      locateBtnText.textContent = 'Locate';
      locateBtn.disabled = false;
      var msg = 'Location unavailable.';
      if (err.code === 1) msg = 'Location permission denied.';
      alert(msg);
    },
    { enableHighAccuracy: true, timeout: 10000, maximumAge: 60000 }
  );
});

function reverseGeocode(lat, lon) {
  fetch('https://nominatim.openstreetmap.org/reverse?lat=' + lat + '&lon=' + lon + '&format=json&addressdetails=1')
    .then(function(r) { return r.json(); })
    .then(function(data) {
      var a = data.address || {};
      var city = a.city || a.town || a.village || '';
      var county = a.county || '';
      var state = a.state || '';
      var road = a.road || '';
      var num = a.house_number || '';
      var zip = a.postcode || '';
      var parts = [];
      if (num && road) parts.push(num + ' ' + road);
      else if (road) parts.push(road);
      if (city) parts.push(city);
      if (state) parts.push(state);
      if (zip) parts.push(zip);
      locationField.value = parts.join(', ');
      detectedState = state;
      detectedLocation = { city: city, county: county, state: state, full: parts.join(', ') };
      var detail = [city, county, state].filter(Boolean);
      locationDetail.textContent = detail.join(' \u00B7 ');
      locationDetail.classList.remove('hidden');
      updateStandardLabel(state);
      locateBtnText.textContent = '\u2713';
      locateBtn.disabled = false;
      setTimeout(function() { locateBtnText.textContent = 'Locate'; }, 2000);
    })
    .catch(function() {
      locateBtnText.textContent = 'Locate';
      locateBtn.disabled = false;
      alert('Could not determine address.');
    });
}

function updateStandardLabel(state) {
  if (!standardLabel) return;
  if (state === 'California') {
    standardLabel.textContent = 'Federal ADA + CA CBC Title 24';
    standardLabel.classList.remove('text-slate-500');
    standardLabel.classList.add('text-sky-400');
  } else if (state) {
    standardLabel.textContent = 'Federal ADA Standards \u00B7 ' + state;
    standardLabel.classList.remove('text-sky-400');
    standardLabel.classList.add('text-slate-500');
  } else {
    standardLabel.textContent = 'Federal ADA Standards';
    standardLabel.classList.remove('text-sky-400');
    standardLabel.classList.add('text-slate-500');
  }
}

// ── SSE Analysis ────────────────────────────────────────────────
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
  if (detectedState) formData.append('state', detectedState);
  formData.append('session_id', getSessionId());

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
      buffer = lines.pop();
      for (var i = 0; i < lines.length; i++) {
        if (!lines[i].startsWith('data: ')) continue;
        try { handleSSEEvent(JSON.parse(lines[i].slice(6).trim())); } catch(e) {}
      }
    }
    if (buffer.startsWith('data: ')) {
      try { handleSSEEvent(JSON.parse(buffer.slice(6).trim())); } catch(e) {}
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
  var type = event.type || event.event || event.pass;
  if (type === 'scene_classification') {
    markStepDone(1, formatType((event.data && event.data.space_type) || event.space_type || 'Identified'));
  } else if (type === 'violation_detection') {
    var c = (event.data && event.data.violation_count) || event.violation_count || 0;
    markStepDone(2, c + ' violation' + (c !== 1 ? 's' : '') + ' detected');
  } else if (type === 'complete' || type === 'analysis_complete') {
    markStepDone(3, 'Report ready');
    var data = (event.data && event.data.report) || event.data || event.report || event;
    currentReportData = data;
    currentPdfUrl = data.pdf_url || null;
    renderResults(data);
    saveToHistory(data);
  } else if (type === 'error') {
    alert('Analysis error: ' + ((event.data && event.data.message) || event.message || 'Unknown'));
  }
}

// ── Progress ────────────────────────────────────────────────────
function resetProgress() {
  document.querySelectorAll('.step-indicator').forEach(function(step) {
    var icon = step.querySelector('.step-icon');
    icon.textContent = step.getAttribute('data-step');
    icon.className = 'step-icon w-8 h-8 rounded-full bg-slate-800 flex items-center justify-center text-slate-500 font-mono font-bold text-xs shrink-0';
    step.querySelector('.step-label').textContent = '';
  });
  var first = document.querySelector('.step-indicator[data-step="1"] .step-icon');
  if (first) first.className = 'step-icon w-8 h-8 rounded-full bg-sky-600 flex items-center justify-center text-white font-mono font-bold text-xs shrink-0 animate-pulse';
}

function markStepDone(num, label) {
  var step = document.querySelector('.step-indicator[data-step="' + num + '"]');
  if (!step) return;
  var icon = step.querySelector('.step-icon');
  icon.textContent = '\u2713';
  icon.className = 'step-icon w-8 h-8 rounded-full bg-emerald-600 flex items-center justify-center text-white font-mono font-bold text-xs shrink-0';
  step.querySelector('.step-label').textContent = label;
  var next = document.querySelector('.step-indicator[data-step="' + (num + 1) + '"] .step-icon');
  if (next) next.className = 'step-icon w-8 h-8 rounded-full bg-sky-600 flex items-center justify-center text-white font-mono font-bold text-xs shrink-0 animate-pulse';
}

// ── Render Full Report ──────────────────────────────────────────
function renderResults(data) {
  var violations = data.violations || [];
  var confirmed = violations.filter(function(v) { return (v.confidence || 0) >= 0.7; });
  var potential = violations.filter(function(v) { return (v.confidence || 0) < 0.7; });

  // Headline
  var headlineEl = document.getElementById('report-headline');
  headlineEl.textContent = data.headline || (violations.length + ' violation' + (violations.length !== 1 ? 's' : '') + ' found');

  // Summary
  document.getElementById('summary-text').textContent = data.summary || '';

  // Risk badge
  var risk = data.overall_risk || 'unknown';
  var riskBadge = document.getElementById('risk-badge');
  riskBadge.textContent = risk.toUpperCase() + ' RISK';
  riskBadge.className = 'px-3 py-1 rounded-full text-xs font-bold shrink-0 ml-3 risk-' + risk;

  // Stats
  document.getElementById('total-violations').textContent = violations.length;
  document.getElementById('confirmed-count').textContent = confirmed.length;
  document.getElementById('potential-count').textContent = potential.length;
  var totalCost = data.total_estimated_cost ? (data.total_estimated_cost.low || 0) : 0;
  document.getElementById('total-cost').textContent = violations.length > 0 ? '$' + totalCost.toLocaleString() : '$0';

  // Severity breakdown
  var bySev = data.by_severity || {};
  var high = bySev.high || 0, med = bySev.medium || 0, low = bySev.low || 0;
  var total = high + med + low || 1;
  document.getElementById('sev-high-count').textContent = high;
  document.getElementById('sev-med-count').textContent = med;
  document.getElementById('sev-low-count').textContent = low;
  var bar = document.getElementById('severity-bar');
  clearChildren(bar);
  if (high > 0) { var s = document.createElement('div'); s.className = 'sev-bar-high h-full'; s.style.width = (high/total*100)+'%'; bar.appendChild(s); }
  if (med > 0)  { var s = document.createElement('div'); s.className = 'sev-bar-medium h-full'; s.style.width = (med/total*100)+'%'; bar.appendChild(s); }
  if (low > 0)  { var s = document.createElement('div'); s.className = 'sev-bar-low h-full'; s.style.width = (low/total*100)+'%'; bar.appendChild(s); }

  // PDF button
  if (currentPdfUrl) { downloadPdfBtn.classList.remove('hidden'); } else { downloadPdfBtn.classList.add('hidden'); }

  // Compliance banner
  var isCompliant = violations.length === 0;
  var hasPositives = data.positive_features && data.positive_features.length > 0;
  if (complianceBanner) {
    complianceBanner.classList.remove('hidden');
    if (isCompliant) {
      complianceBanner.className = 'rounded-2xl p-5 border border-emerald-900/40 bg-emerald-950/20 text-center';
      complianceIcon.className = 'mx-auto w-12 h-12 rounded-full flex items-center justify-center mb-3 bg-emerald-900/50';
      complianceIcon.textContent = '\u2713';
      complianceIcon.style.cssText = 'color:#34d399;font-size:24px;font-weight:bold';
      complianceLabel.textContent = 'No Violations Detected';
      complianceLabel.className = 'text-lg font-bold mb-1 text-emerald-300';
      complianceSublabel.textContent = hasPositives
        ? data.positive_features.length + ' compliant feature' + (data.positive_features.length !== 1 ? 's' : '') + ' identified'
        : 'This space appears to meet accessibility standards based on visual inspection';
      complianceSublabel.className = 'text-sm text-emerald-400/70';
    } else if (hasPositives) {
      complianceBanner.className = 'rounded-2xl p-5 border border-slate-800 bg-slate-900/50 text-center';
      complianceIcon.className = 'mx-auto w-12 h-12 rounded-full flex items-center justify-center mb-3 bg-slate-800';
      complianceIcon.textContent = '\u00B1';
      complianceIcon.style.cssText = 'color:#94a3b8;font-size:24px;font-weight:bold';
      complianceLabel.textContent = 'Partial Compliance';
      complianceLabel.className = 'text-lg font-bold mb-1 text-slate-300';
      complianceSublabel.textContent = data.positive_features.length + ' compliant feature' + (data.positive_features.length !== 1 ? 's' : '') + ' alongside ' + violations.length + ' violation' + (violations.length !== 1 ? 's' : '');
      complianceSublabel.className = 'text-sm text-slate-400';
    } else {
      complianceBanner.classList.add('hidden');
    }
  }

  // Positive features
  clearChildren(positiveList);
  if (hasPositives) {
    positiveSection.classList.remove('hidden');
    if (positiveCount) positiveCount.textContent = data.positive_features.length + ' found';
    data.positive_features.forEach(function(f) {
      var li = document.createElement('li');
      li.className = 'flex items-start gap-3 text-sm';

      var iconWrap = document.createElement('div');
      iconWrap.className = 'w-6 h-6 rounded-full bg-emerald-900/50 flex items-center justify-center shrink-0 mt-0.5';
      iconWrap.textContent = '\u2713';
      iconWrap.style.cssText = 'color:#34d399;font-size:12px;font-weight:bold';

      var textWrap = document.createElement('div');
      var featureText = document.createElement('p');
      featureText.className = 'text-emerald-300';
      featureText.textContent = f;
      textWrap.appendChild(featureText);

      li.appendChild(iconWrap);
      li.appendChild(textWrap);
      positiveList.appendChild(li);
    });
  } else { positiveSection.classList.add('hidden'); }

  // Violation cards
  clearChildren(violationsList);
  var sorted = violations.slice().sort(function(a, b) { return (a.priority || 99) - (b.priority || 99); });

  if (confirmed.length > 0) {
    var h = document.createElement('p');
    h.className = 'text-xs font-mono text-rose-400/80 uppercase tracking-widest mb-1';
    h.textContent = 'Confirmed (' + confirmed.length + ')';
    violationsList.appendChild(h);
    sorted.filter(function(v) { return (v.confidence||0) >= 0.7; }).forEach(function(v) {
      violationsList.appendChild(buildViolationCard(v));
    });
  }

  if (potential.length > 0) {
    var h = document.createElement('p');
    h.className = 'text-xs font-mono text-amber-400/80 uppercase tracking-widest mb-1 mt-4';
    h.textContent = 'Potential (' + potential.length + ')';
    violationsList.appendChild(h);
    sorted.filter(function(v) { return (v.confidence||0) < 0.7; }).forEach(function(v) {
      violationsList.appendChild(buildViolationCard(v));
    });
  }

  // Cost summary table
  var costTable = document.getElementById('cost-table');
  clearChildren(costTable);
  sorted.forEach(function(v) {
    var row = document.createElement('div');
    row.className = 'cost-row';
    var left = document.createElement('div');
    left.className = 'flex items-center gap-2 flex-1 min-w-0';
    var dot = document.createElement('div');
    dot.className = 'w-2 h-2 rounded-full shrink-0 ' + ({high:'bg-rose-500',medium:'bg-amber-500',low:'bg-sky-500'}[v.severity]||'bg-slate-500');
    var name = document.createElement('span');
    name.className = 'text-xs text-slate-400 truncate';
    name.textContent = v.title || formatType(v.violation_type || '');
    left.appendChild(dot);
    left.appendChild(name);
    var cost = document.createElement('span');
    cost.className = 'text-xs font-mono text-amber-400 shrink-0 ml-2';
    cost.textContent = '$' + (v.estimated_cost || 0).toLocaleString();
    row.appendChild(left);
    row.appendChild(cost);
    costTable.appendChild(row);
  });
  document.getElementById('cost-total-display').textContent = '$' + totalCost.toLocaleString();

  // Tax credits
  var tcList = document.getElementById('tax-credits-list');
  clearChildren(tcList);
  var credits = data.tax_credits || [];
  credits.forEach(function(tc) {
    var card = document.createElement('div');
    card.className = 'tax-credit-card';
    card.innerHTML =
      '<div class="flex items-center justify-between mb-1">' +
        '<span class="text-sm font-semibold text-emerald-300">' + escHtml(tc.name) + '</span>' +
        '<span class="text-sm font-mono font-bold text-emerald-400">up to $' + (tc.max_amount||0).toLocaleString() + '</span>' +
      '</div>' +
      '<p class="text-xs text-slate-400">' + escHtml(tc.eligibility || '') + '</p>' +
      (tc.form ? '<p class="text-[10px] font-mono text-slate-500 mt-1">' + escHtml(tc.form || tc.section || '') + '</p>' : '');
    tcList.appendChild(card);
  });

  // Next steps
  var nsList = document.getElementById('next-steps-list');
  clearChildren(nsList);
  var steps = data.next_steps || [];
  steps.forEach(function(step, idx) {
    var li = document.createElement('li');
    li.className = 'remediation-step';
    li.innerHTML =
      '<div class="step-number">' + (idx + 1) + '</div>' +
      '<p class="text-sm text-slate-300">' + escHtml(step) + '</p>';
    nsList.appendChild(li);
  });

  // Follow-up suggestions
  clearChildren(followupList);
  var followups = data.follow_up_suggestions || [];
  if (followups.length > 0) {
    followupSection.classList.remove('hidden');
    followups.forEach(function(s) {
      var text = typeof s === 'string' ? s : (s.description || '');
      var li = document.createElement('li');
      li.className = 'text-sm text-violet-300';
      li.textContent = '\u2022 ' + text;
      followupList.appendChild(li);
    });
  } else { followupSection.classList.add('hidden'); }

  // Disclaimer
  document.getElementById('disclaimer').textContent = data.disclaimer || '';

  resultsEl.classList.remove('hidden');
  progressEl.classList.add('hidden');
}

// ── Build Violation Card ────────────────────────────────────────
function buildViolationCard(v) {
  var card = document.createElement('div');
  card.className = 'violation-card severity-' + (v.severity || 'medium');

  // ── Header (always visible, clickable) ──
  var header = document.createElement('div');
  header.className = 'violation-card-header';

  // Priority badge
  var priority = document.createElement('div');
  priority.className = 'priority-badge sev-' + (v.severity || 'medium');
  priority.textContent = '#' + (v.priority || '?');

  // Title + meta
  var titleArea = document.createElement('div');
  titleArea.className = 'flex-1 min-w-0';
  var titleRow = document.createElement('div');
  titleRow.className = 'flex items-center gap-2';
  var title = document.createElement('h4');
  title.className = 'text-sm font-semibold text-white truncate';
  title.textContent = v.title || formatType(v.violation_type || '');
  var sevBadge = document.createElement('span');
  sevBadge.className = 'px-1.5 py-0.5 rounded text-[10px] font-bold uppercase severity-badge-' + (v.severity||'medium');
  sevBadge.textContent = (v.severity||'medium').toUpperCase();
  titleRow.appendChild(title);
  titleRow.appendChild(sevBadge);
  titleArea.appendChild(titleRow);

  var metaRow = document.createElement('div');
  metaRow.className = 'flex items-center gap-3 mt-1 text-[11px] text-slate-500';
  metaRow.innerHTML =
    '<span>' + Math.round((v.confidence||0)*100) + '% confidence</span>' +
    '<span class="text-amber-400 font-mono font-semibold">$' + (v.estimated_cost||0).toLocaleString() + '</span>' +
    (v.cost_unit ? '<span class="text-slate-600">' + escHtml(v.cost_unit) + '</span>' : '');
  titleArea.appendChild(metaRow);

  // Chevron
  var chevron = document.createElement('svg');
  chevron.setAttribute('class', 'violation-card-chevron');
  chevron.setAttribute('fill', 'none');
  chevron.setAttribute('stroke', 'currentColor');
  chevron.setAttribute('viewBox', '0 0 24 24');
  chevron.innerHTML = '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>';

  header.appendChild(priority);
  header.appendChild(titleArea);
  header.appendChild(chevron);
  card.appendChild(header);

  // Toggle expand
  header.addEventListener('click', function() {
    card.classList.toggle('expanded');
  });

  // ── Body (expandable) ──
  var body = document.createElement('div');
  body.className = 'violation-card-body';

  // Description
  if (v.description) {
    var desc = document.createElement('p');
    desc.className = 'text-sm text-slate-300 mb-3';
    desc.textContent = v.description;
    body.appendChild(desc);
  }

  // Legal risk callout
  if (v.legal_risk) {
    var legal = document.createElement('div');
    legal.className = 'legal-risk-box mb-3';
    legal.innerHTML =
      '<div class="flex items-start gap-2">' +
        '<svg class="w-4 h-4 mt-0.5 shrink-0 text-rose-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>' +
        '<div>' +
          '<p class="text-[10px] font-mono text-rose-400 uppercase tracking-widest mb-1">Legal Risk</p>' +
          '<p class="text-xs text-rose-200/80 leading-relaxed">' + escHtml(v.legal_risk) + '</p>' +
        '</div>' +
      '</div>';
    body.appendChild(legal);
  }

  // Code references
  var codes = document.createElement('div');
  codes.className = 'grid grid-cols-1 sm:grid-cols-2 gap-2 mb-3';
  if (v.ada_section && v.ada_section !== 'N/A') {
    var ada = document.createElement('div');
    ada.className = 'code-ref';
    ada.innerHTML =
      '<p class="text-[10px] font-mono text-sky-400 uppercase tracking-widest mb-1">Federal ADA</p>' +
      '<p class="text-xs text-slate-300 font-semibold">Section ' + escHtml(v.ada_section) + '</p>' +
      '<p class="text-[11px] text-slate-400">' + escHtml(v.ada_title || '') + '</p>';
    codes.appendChild(ada);
  }
  if (v.cbc_section && v.cbc_section !== 'N/A') {
    var cbc = document.createElement('div');
    cbc.className = 'code-ref';
    cbc.innerHTML =
      '<p class="text-[10px] font-mono text-amber-400 uppercase tracking-widest mb-1">CA CBC Title 24</p>' +
      '<p class="text-xs text-slate-300 font-semibold">Section ' + escHtml(v.cbc_section) + '</p>' +
      '<p class="text-[11px] text-slate-400">' + escHtml(v.cbc_title || '') + '</p>';
    codes.appendChild(cbc);
  }
  if (codes.children.length > 0) body.appendChild(codes);

  // Remediation detail
  var rem = v.remediation_detail || {};
  if (rem.steps && rem.steps.length > 0) {
    var remSection = document.createElement('div');
    remSection.className = 'mb-3';
    remSection.innerHTML = '<p class="text-[10px] font-mono text-emerald-400 uppercase tracking-widest mb-2">Remediation Steps</p>';
    rem.steps.forEach(function(step, idx) {
      var row = document.createElement('div');
      row.className = 'remediation-step mb-1.5';
      // Strip leading "N. " if present
      var stepText = step.replace(/^\d+\.\s*/, '');
      row.innerHTML =
        '<div class="step-number">' + (idx + 1) + '</div>' +
        '<p class="text-xs text-slate-300 leading-relaxed">' + escHtml(stepText) + '</p>';
      remSection.appendChild(row);
    });
    body.appendChild(remSection);
  } else if (v.remediation) {
    var remP = document.createElement('p');
    remP.className = 'text-xs text-slate-400 mb-3';
    remP.innerHTML = '<span class="text-emerald-400 font-semibold">Fix:</span> ' + escHtml(v.remediation);
    body.appendChild(remP);
  }

  // Info tags row (contractor, permit, timeline)
  var tags = document.createElement('div');
  tags.className = 'flex flex-wrap gap-1.5 mb-3';
  if (rem.contractor_type) {
    tags.innerHTML += '<span class="info-tag"><svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/></svg>' + escHtml(rem.contractor_type) + '</span>';
  }
  if (rem.permit_required) {
    tags.innerHTML += '<span class="info-tag"><svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>' + escHtml(rem.permit_type || 'Permit required') + '</span>';
  }
  if (rem.timeline) {
    tags.innerHTML += '<span class="info-tag"><svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>' + escHtml(rem.timeline) + '</span>';
  }
  if (tags.children.length > 0) body.appendChild(tags);

  // Cost note
  if (v.cost_note) {
    var cn = document.createElement('p');
    cn.className = 'text-[11px] text-slate-500 italic';
    cn.textContent = v.cost_note;
    body.appendChild(cn);
  }

  card.appendChild(body);
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
  if (complianceBanner) complianceBanner.classList.add('hidden');
  clearChildren(violationsList);
  clearChildren(positiveList);
  clearChildren(followupList);
  window.scrollTo(0, 0);
});

// ── History ─────────────────────────────────────────────────────
async function saveToHistory(report) {
  try {
    var thumbnail = '';
    if (preview.src && !preview.classList.contains('hidden')) {
      try {
        var canvas = document.createElement('canvas');
        canvas.width = 120; canvas.height = 120;
        var ctx = canvas.getContext('2d');
        var size = Math.min(preview.naturalWidth, preview.naturalHeight);
        ctx.drawImage(preview, (preview.naturalWidth-size)/2, (preview.naturalHeight-size)/2, size, size, 0, 0, 120, 120);
        thumbnail = canvas.toDataURL('image/jpeg', 0.6);
      } catch(e) {}
    }
    var violations = report.violations || [];
    await saveReport({
      id: report.report_id || report.id || crypto.randomUUID(),
      date: new Date().toISOString(),
      thumbnail: thumbnail,
      location: locationField.value.trim() || 'Unknown location',
      spaceType: report.space_type || '',
      riskLevel: violations.length === 0 ? 'none' : (report.overall_risk || 'unknown'),
      isCompliant: violations.length === 0,
      positiveCount: (report.positive_features || []).length,
      confirmedCount: violations.filter(function(v){return (v.confidence||0)>=0.7;}).length,
      potentialCount: violations.filter(function(v){return (v.confidence||0)<0.7;}).length,
      violationCount: violations.length,
      costRange: report.total_estimated_cost ? '$'+((report.total_estimated_cost.low||0).toLocaleString()) : '$0',
      pdfUrl: report.pdf_url || null,
      reportData: report
    });
  } catch(e) { console.error('History save failed:', e); }
}

async function loadHistory(filter) {
  try {
    var reports = await getAllReports();
    if (filter === 'compliant') {
      reports = reports.filter(function(r) { return r.isCompliant || r.riskLevel === 'none'; });
    } else if (filter && filter !== 'all') {
      reports = reports.filter(function(r) { return r.riskLevel === filter; });
    }
    clearChildren(historyList);
    if (reports.length === 0) { historyEmpty.classList.remove('hidden'); return; }
    historyEmpty.classList.add('hidden');
    reports.forEach(function(r) {
      var card = document.createElement('div');
      card.className = 'bg-slate-900 border border-slate-800 rounded-xl p-3 flex gap-3 cursor-pointer hover:bg-slate-800 transition';
      card.addEventListener('click', function(){ viewHistoryReport(r); });
      if (r.thumbnail) {
        var img = document.createElement('img');
        img.src = r.thumbnail;
        img.className = 'w-14 h-14 rounded-lg object-cover shrink-0';
        card.appendChild(img);
      }
      var info = document.createElement('div');
      info.className = 'flex-1 min-w-0';
      var badgeClass = r.isCompliant ? 'risk-none' : 'risk-' + (r.riskLevel||'unknown');
      var badgeText = r.isCompliant ? 'COMPLIANT' : (r.riskLevel||'?').toUpperCase();
      var metaLine = r.isCompliant
        ? '<span class="text-emerald-400">' + (r.positiveCount||0) + ' compliant features</span>'
        : '<span>' + (r.violationCount||0) + ' violations</span>' +
          (r.costRange && r.costRange!=='$0' ? '<span class="text-amber-400">' + r.costRange + '</span>' : '');

      info.innerHTML =
        '<div class="flex items-center justify-between mb-0.5">' +
          '<p class="text-sm font-medium text-slate-200 truncate">' + escHtml(r.location||'Unknown') + '</p>' +
          '<span class="px-2 py-0.5 rounded-full text-[10px] font-bold ' + badgeClass + ' shrink-0 ml-2">' + badgeText + '</span>' +
        '</div>' +
        '<p class="text-[10px] text-slate-500 font-mono">' + new Date(r.date).toLocaleDateString() + '</p>' +
        '<div class="flex gap-3 mt-0.5 text-[10px] text-slate-500">' + metaLine + '</div>';
      card.appendChild(info);
      historyList.appendChild(card);
    });
  } catch(e) { console.error('History load failed:', e); }
}

function viewHistoryReport(r) {
  document.querySelectorAll('.screen').forEach(function(s){s.classList.remove('active');});
  document.getElementById('scan-screen').classList.add('active');
  document.querySelectorAll('.nav-btn').forEach(function(b){b.classList.remove('active');});
  document.querySelector('.nav-btn[data-screen="scan-screen"]').classList.add('active');
  if (r.thumbnail) { preview.src = r.thumbnail; preview.classList.remove('hidden'); uploadContent.classList.add('hidden'); }
  locationField.value = r.location || '';
  currentPdfUrl = r.pdfUrl || null;
  currentReportData = r.reportData || null;
  if (r.reportData) { progressEl.classList.add('hidden'); renderResults(r.reportData); }
}

document.querySelectorAll('.filter-btn').forEach(function(btn) {
  btn.addEventListener('click', function() {
    document.querySelectorAll('.filter-btn').forEach(function(f){f.classList.remove('active');});
    btn.classList.add('active');
    loadHistory(btn.getAttribute('data-filter'));
  });
});

// ── Helpers ─────────────────────────────────────────────────────
function getSessionId() {
  var id = localStorage.getItem('ada-session-id');
  if (!id) { id = crypto.randomUUID(); localStorage.setItem('ada-session-id', id); }
  return id;
}

if ('serviceWorker' in navigator) {
  window.addEventListener('load', function() {
    navigator.serviceWorker.register('/static/sw.js').catch(function(e){});
  });
}

function severityOrder(s) { return {high:0,medium:1,low:2}[s]||3; }
function formatType(t) { return t ? t.replace(/_/g,' ').replace(/\b\w/g,function(c){return c.toUpperCase();}) : ''; }
function escHtml(s) {
  var d = document.createElement('div');
  d.appendChild(document.createTextNode(s || ''));
  return d.innerHTML;
}
