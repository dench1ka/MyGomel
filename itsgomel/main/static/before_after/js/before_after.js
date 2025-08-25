document.querySelectorAll('.comparison-container').forEach(container => {
  const handle = container.querySelector('.comparison-handle');
  const resize = container.querySelector('.comparison-resize');
  let dragging = false;

  const startDrag = () => dragging = true;
  const stopDrag = () => dragging = false;

  const moveDrag = e => {
    if (!dragging) return;
    let clientX = e.clientX ?? e.touches[0].clientX;
    let rect = container.getBoundingClientRect();
    let offsetX = clientX - rect.left;

// Ползунок нельзя уводить за края
offsetX = Math.max(0, Math.min(offsetX, rect.width));
handle.style.left = offsetX + "px"; // handle всегда в пределах
resize.style.width = offsetX + "px"; // картинка “после”

  };

  handle.addEventListener('mousedown', startDrag);
  window.addEventListener('mouseup', stopDrag);
  window.addEventListener('mousemove', moveDrag);

  handle.addEventListener('touchstart', startDrag);
  window.addEventListener('touchend', stopDrag);
  window.addEventListener('touchmove', moveDrag);
});

const comparisonContainer = document.querySelector('.comparison-container');

comparisonContainer.addEventListener('dragstart', function(e) {
    e.preventDefault(); // блокируем стандартное перетаскивание картинки
});
