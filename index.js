// Animate random key presses
function animateTyping() {
  const keys = document.querySelectorAll('.key');
  
  setInterval(() => {
    const randomKey = keys[Math.floor(Math.random() * keys.length)];
    randomKey.classList.add('active');
    
    setTimeout(() => {
      randomKey.classList.remove('active');
    }, 150);
  }, 100);
}

// Start when page loads
animateTyping();