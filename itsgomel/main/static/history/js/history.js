document.addEventListener('DOMContentLoaded', function () {

    const slider = document.querySelector('.history-images');
    if (!slider) return;

    const slides = Array.from(slider.querySelectorAll('img'));
    let currentIndex = 0;

    if (slides.length === 0) return;

    // Показываем первый слайд
    slides[currentIndex].classList.add('active');

    const prevBtn = slider.querySelector('.slider-prev');
    const nextBtn = slider.querySelector('.slider-next');

    if (slides.length <= 1) {
        prevBtn.style.display = "none";
        nextBtn.style.display = "none";
        return;
    }

    function showSlide(index) {
        slides.forEach((slide, i) => {
            slide.classList.toggle('active', i === index);
        });
    }

    prevBtn.addEventListener('click', function () {
        currentIndex = (currentIndex - 1 + slides.length) % slides.length;
        showSlide(currentIndex);
    });

    nextBtn.addEventListener('click', function () {
        currentIndex = (currentIndex + 1) % slides.length;
        showSlide(currentIndex);
    });
});
