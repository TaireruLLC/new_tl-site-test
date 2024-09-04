// Wait for the DOM to load
window.onload = function() {
    // Select elements
    const drop = document.getElementById('water-drop');
    const menu = document.getElementById('menu');

    // Initial drop animation using GSAP
    gsap.fromTo(drop, 
        { y: -100, scale: 1 },  // Start above screen and small
        { 
            y: window.innerHeight / 2 - 25,  // Drop to center
            scale: 1.5,  // Slightly enlarge
            duration: 2,  // Duration of the drop
            ease: "bounce.out",  // Bounce effect
            onComplete: fillScreen  // Trigger screen fill
        }
    );

    // Function to fill the screen and show the menu
    function fillScreen() {
        gsap.to(drop, {
            scaleX: 50,  // Stretch the drop horizontally
            scaleY: 50,  // Stretch the drop vertically
            duration: 1.5,  // Duration of the fill
            ease: "power2.inOut",
            onComplete: showMenu  // Trigger menu reveal
        });
    }

    // Function to fade in the menu
    function showMenu() {
        gsap.to(menu, { opacity: 1, duration: 1 });
    }
};
