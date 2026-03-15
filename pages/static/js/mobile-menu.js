(() => {
    const menuBtn = document.querySelector('[data-menu-open]');
    const closeBtn = document.querySelector('[data-menu-close]');
    const menu = document.querySelector('[data-menu]');

    if (menuBtn && closeBtn && menu) {
        menuBtn.addEventListener('click', () => {
            menu.classList.add('is-open');
            document.body.style.overflow = 'hidden'; 
        });

        closeBtn.addEventListener('click', () => {
            menu.classList.remove('is-open');
            document.body.style.overflow = ''; 
        });
    }
})();