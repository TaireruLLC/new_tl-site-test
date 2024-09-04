window.onload = function() {
    const drop = document.getElementById('water-drop');
    const contentContainer = document.getElementById('content-container');

    // Step 1: Initial drop animation using GSAP
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

    // Step 2: Function to fill the screen
    function fillScreen() {
        gsap.to(drop, {
            scaleX: 50,  // Stretch the drop horizontally
            scaleY: 50,  // Stretch the drop vertically
            duration: 1.5,  // Duration of the fill
            ease: "power2.inOut",
            onComplete: loadContent  // Load the content after fill
        });
    }

    // Step 3: Function to load 'about.html' content
    function loadContent() {
        const xhr = new XMLHttpRequest();
        xhr.open('GET', 'about.html', true);
        xhr.onreadystatechange = function() {
            if (xhr.readyState === 4 && xhr.status === 200) {
                // Load the new content into content-container
                contentContainer.innerHTML = xhr.responseText;

                // Step 4: Fade in the new content
                gsap.to(contentContainer, { opacity: 1, duration: 1 });
            }
        };
        xhr.send();
    }
};
