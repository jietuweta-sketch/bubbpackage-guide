/* Shared guide navigation. Installation links are intentionally absent until store approval. */
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.site-header').forEach(header => {
    if (header.querySelector('.helper-nav-link')) return;
    const link = document.createElement('a');
    link.className = 'helper-nav-link';
    link.href = '/print-helper/';
    link.textContent = '印刷稿下载助手';
    if (location.pathname.startsWith('/print-helper')) link.setAttribute('aria-current', 'page');
    header.insertBefore(link, header.querySelector('.back-home') || null);
  });
});
