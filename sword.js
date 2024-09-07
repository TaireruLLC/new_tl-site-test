const slashButton = document.getElementById('slashButton');
const swordSlash = document.querySelector('.sword-slash');

slashButton.addEventListener('click', () => {
    swordSlash.style.left = `${Math.random() * 100}%`;
    swordSlash.style.top = `${Math.random() * 100}%`;

    swordSlash.style.animation = 'none'; // Reset animation
    requestAnimationFrame(() => {
        swordSlash.style.animation = 'slash 0.6s ease-out';
    });
});
