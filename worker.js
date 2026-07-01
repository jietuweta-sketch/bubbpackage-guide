// Cloudflare Worker: Proxy /guide/* to GitHub Pages
// Other requests pass through to origin server

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    
    // Route /guide/* to GitHub Pages
    if (url.pathname.startsWith('/guide')) {
      // Remove /guide prefix for GitHub Pages (which serves at root)
      const ghPath = url.pathname.replace(/^\/guide\/?/, '/');
      const ghUrl = `https://jietuweta-sketch.github.io/bubbpackage-guide${ghPath}${url.search}`;
      
      const ghResp = await fetch(ghUrl, {
        method: request.method,
        headers: filterHeaders(request.headers),
        body: request.method !== 'GET' && request.method !== 'HEAD' ? request.body : undefined,
      });
      
      // Return GitHub response with cleaned headers
      const newHeaders = new Headers(ghResp.headers);
      newHeaders.set('x-served-by', 'cloudflare-worker-guide');
      return new Response(ghResp.body, {
        status: ghResp.status,
        headers: newHeaders,
      });
    }
    
    // Pass through to origin
    const originResp = await fetch(request);
    return originResp;
  }
};

function filterHeaders(headers) {
  const keep = ['accept', 'accept-encoding', 'accept-language', 'user-agent', 'if-modified-since', 'if-none-match'];
  const result = new Headers();
  for (const [key, value] of headers) {
    if (keep.includes(key.toLowerCase())) {
      result.set(key, value);
    }
  }
  return result;
}
