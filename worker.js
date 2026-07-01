export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    
    if (url.pathname.startsWith('/guide')) {
      // Strip /guide prefix for raw GitHub path
      let ghPath = url.pathname.replace(/^\/guide\/?/, '/');
      if (ghPath === '/' || ghPath === '') ghPath = '/index.html';
      if (!ghPath.includes('.')) ghPath = ghPath.replace(/\/$/, '') + '/index.html';
      
      const ghUrl = 'https://raw.githubusercontent.com/jietuweta-sketch/bubbpackage-guide/main' + ghPath;
      
      const ghResp = await fetch(ghUrl);
      
      if (!ghResp.ok) {
        return new Response('Not Found', { status: 404 });
      }
      
      // Set proper content type
      const ct = ghPath.endsWith('.html') ? 'text/html; charset=utf-8'
               : ghPath.endsWith('.css') ? 'text/css'
               : ghPath.endsWith('.js') ? 'application/javascript'
               : ghPath.endsWith('.svg') ? 'image/svg+xml'
               : 'application/octet-stream';
      
      const body = await ghResp.text();
      
      return new Response(body, {
        status: 200,
        headers: { 'Content-Type': ct, 'Cache-Control': 'public, max-age=3600' }
      });
    }
    
    return fetch(request);
  }
};
