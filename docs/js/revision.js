if (typeof document$ !== "undefined") {
  document$.subscribe(function () {
    const h1 = document.querySelector('.md-content h1');
    const meta = document.querySelector('.md-source-file');

    if (h1 && meta) {
      h1.insertAdjacentElement('afterend', meta);
    }
  });
}
