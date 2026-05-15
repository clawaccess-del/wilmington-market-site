const TRACKING_QUERY_KEYS = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content', 'gclid', 'fbclid', 'msclkid'];
const ATTRIBUTION_STORAGE_KEY = 'oc_attribution';

const toggle = document.querySelector('.nav-toggle');
const nav = document.querySelector('.nav');
const leadForm = document.querySelector('#lead-form');
const formNote = document.querySelector('#form-note');

function pushAnalyticsEvent(eventName, params = {}) {
  window.dataLayer = window.dataLayer || [];
  window.dataLayer.push({
    event: eventName,
    ...params,
  });
}

function readStoredAttribution() {
  try {
    return JSON.parse(sessionStorage.getItem(ATTRIBUTION_STORAGE_KEY) || '{}');
  } catch {
    return {};
  }
}

function writeStoredAttribution(value) {
  try {
    sessionStorage.setItem(ATTRIBUTION_STORAGE_KEY, JSON.stringify(value));
  } catch {
    // Ignore storage issues.
  }
}

function getAttributionSnapshot() {
  const params = new URLSearchParams(window.location.search);
  const stored = readStoredAttribution();
  const next = { ...stored };

  if (!next.landing_page) {
    next.landing_page = `${window.location.pathname}${window.location.search}`;
  }

  if (!next.first_seen_at) {
    next.first_seen_at = new Date().toISOString();
  }

  if (!next.referrer && document.referrer) {
    next.referrer = document.referrer;
  }

  TRACKING_QUERY_KEYS.forEach((key) => {
    const value = params.get(key);
    if (value) {
      next[key] = value;
    }
  });

  writeStoredAttribution(next);
  return next;
}

function buildAttributionLines() {
  const attribution = getAttributionSnapshot();
  const lines = [];

  if (attribution.landing_page) {
    lines.push(`Landing page: ${attribution.landing_page}`);
  }

  lines.push(`Current page: ${window.location.pathname}${window.location.search}`);

  if (attribution.referrer) {
    lines.push(`Referrer: ${attribution.referrer}`);
  }

  TRACKING_QUERY_KEYS.forEach((key) => {
    if (attribution[key]) {
      lines.push(`${key}: ${attribution[key]}`);
    }
  });

  return lines;
}

function getLinkLabel(link) {
  return (link.dataset.trackLabel || link.textContent || link.getAttribute('aria-label') || '').trim();
}

getAttributionSnapshot();
pushAnalyticsEvent('session_attribution_ready', {
  page_path: window.location.pathname,
});

if (toggle && nav) {
  const closeNav = () => {
    nav.classList.remove('open');
    toggle.setAttribute('aria-expanded', 'false');
  };

  toggle.addEventListener('click', () => {
    const open = nav.classList.toggle('open');
    toggle.setAttribute('aria-expanded', String(open));
    pushAnalyticsEvent('nav_toggle', { open, page_path: window.location.pathname });
  });

  nav.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', closeNav);
  });

  document.addEventListener('click', (event) => {
    if (!nav.contains(event.target) && !toggle.contains(event.target)) {
      closeNav();
    }
  });

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') {
      closeNav();
    }
  });
}

document.querySelectorAll('a[href^="tel:"]').forEach((link) => {
  link.addEventListener('click', () => {
    pushAnalyticsEvent('click_call', {
      link_url: link.href,
      link_text: getLinkLabel(link),
      page_path: window.location.pathname,
    });
  });
});

document.querySelectorAll('a[href^="sms:"]').forEach((link) => {
  link.addEventListener('click', () => {
    pushAnalyticsEvent('click_sms', {
      link_url: link.href,
      link_text: getLinkLabel(link),
      page_path: window.location.pathname,
    });
  });
});

if (leadForm) {
  leadForm.addEventListener('submit', (event) => {
    event.preventDefault();

    const target = leadForm.dataset.smsTarget;
    if (!target) {
      if (formNote) {
        formNote.textContent = 'This form is not connected right now. Please call or text (803) 602-4458 instead.';
      }
      return;
    }

    const formData = new FormData(leadForm);
    const lines = [
      `Name: ${formData.get('name') || ''}`,
      `Phone: ${formData.get('phone') || ''}`,
      `Email: ${formData.get('email') || ''}`,
      `Business: ${formData.get('business') || ''}`,
      `Service: ${formData.get('service') || ''}`,
      '',
      `${formData.get('message') || ''}`,
    ];

    const attributionLines = buildAttributionLines();
    if (attributionLines.length) {
      lines.push('', 'Tracking context:', ...attributionLines);
    }

    const message = encodeURIComponent(lines.join('\n').trim());
    const smsUrl = `sms:${target}?body=${message}`;

    pushAnalyticsEvent('lead_form_submit', {
      page_path: window.location.pathname,
      service: String(formData.get('service') || ''),
      contact_method: 'sms_prefill',
    });

    if (formNote) {
      formNote.innerHTML = 'Opening your text draft now. If nothing happens on this device, call or text <a href="tel:+18036024458">(803) 602-4458</a> directly.';
    }

    window.location.href = smsUrl;
  });
}
