document.addEventListener('DOMContentLoaded', () => {
    const modal = document.getElementById('modal');
    const openBtn = document.getElementById('openModal');
    const closeBtn = document.getElementById('closeModal');

    if (openBtn && modal) {
        openBtn.onclick = () => modal.classList.add('active');
        closeBtn.onclick = () => modal.classList.remove('active');
        window.onclick = (e) => { if (e.target === modal) modal.classList.remove('active'); };
    }

    // Flip card functionality
    const flipCard = document.querySelector('.flip-card');
    if (flipCard) {
        flipCard.addEventListener('click', () => {
            flipCard.classList.toggle('flipped');
        });

        // Optional: Prevent accidental flips from scrolling on mobile
        flipCard.addEventListener('touchstart', (e) => {
            // Only toggle if it's a tap, not a scroll
            flipCard.dataset.touchStartY = e.touches[0].clientY;
        });

        flipCard.addEventListener('touchend', (e) => {
            const touchEndY = e.changedTouches[0].clientY;
            const touchStartY = parseFloat(flipCard.dataset.touchStartY);
            
            // If movement is less than 10px, it's a tap not a scroll
            if (Math.abs(touchEndY - touchStartY) < 10) {
                // Click event will handle the flip
            }
        });
    }
});