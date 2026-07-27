(function () {
  const viewer = document.getElementById('viewer');
  const status = document.getElementById('load-status');

  function showFailure(title, message, error) {
    console.error(title, error || '');
    if (status) {
      status.className = 'load-status error';
      const label = status.querySelector('b');
      if (label) label.textContent = title;
    }
    if (!viewer) return;
    viewer.querySelectorAll('.viewer-fallback').forEach((element) => element.remove());
    const fallback = document.createElement('div');
    fallback.className = 'viewer-fallback viewer-fallback-error';
    const heading = document.createElement('strong');
    heading.textContent = title;
    const text = document.createElement('span');
    text.textContent = message;
    const retry = document.createElement('button');
    retry.type = 'button';
    retry.className = 'viewer-retry';
    retry.textContent = 'Reload page';
    retry.addEventListener('click', () => location.reload());
    fallback.append(heading, text, retry);
    viewer.append(fallback);
  }

  try {
    const canvas = document.createElement('canvas');
    const webgl = canvas.getContext('webgl2') || canvas.getContext('webgl');
    if (!webgl) {
      showFailure(
        'WebGL is unavailable',
        'Enable hardware acceleration or open the site in a current desktop browser. The documents and downloads below remain usable.'
      );
      return;
    }
  } catch (error) {
    showFailure('WebGL check failed', 'The browser could not initialise 3D graphics.', error);
    return;
  }

  const scriptUrl = document.currentScript?.src || new URL('./js/bootstrap.js', document.baseURI).href;
  const appUrl = new URL('./app.js', scriptUrl).href;
  import(appUrl).catch((error) => {
    showFailure(
      '3D application failed to start',
      'Check the internet connection for the pinned Three.js modules, then reload. Local use must be through the included HTTP server rather than file://.',
      error
    );
  });
})();
