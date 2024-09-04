window.onload = function() {
    const drop = document.getElementById('water-drop');
    
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
            onComplete: loadHomePage  // Load the home page after fill
        });
    }

    // Step 3: Function to load 'home.html' content
    function loadHomePage() {
        const xhr = new XMLHttpRequest();
        xhr.open('GET', 'home.html', true);
        xhr.onreadystatechange = function() {
            if (xhr.readyState === 4 && xhr.status === 200) {
                // Replace the entire body content with the loaded content
                document.open();
                document.write(xhr.responseText);
                document.close();

                // Optionally: reinitialize any scripts or animations after loading the new page
            }
        };
        xhr.send();
    }
};
