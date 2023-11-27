const parallax_el = document.querySelectorAll('.landing_parallax')

let xValue = 0, yValue = 0;

function update(cursorPosition) {
    parallax_el.forEach(el =>{
        let speedx = el.dataset.speedx;
        let speedy = el.dataset.speedy;
        let speedz = el.dataset.speedz;
        let rotateSpeed = el.dataset.rotation;

        let isInLeft = 
            parseFloat(getComputedStyle(el).left) < window.innerWidth / 2 ? 1 : -1;
        let zValue = (cursorPosition - parseFloat(getComputedStyle(el).left)) * isInLeft *0.1;

        el.style.transform = `translateX(calc(-50% + ${
            -xValue*speedx
        }px)) rotateY(${rotateDegree * rotateSpeed}deg) translateY(calc(-50% + ${
            yValue*speedy
        }px)) perspective(2300px) translateZ(${zValue * speedz}px)`;
    })
}

// update(0)

window.addEventListener('mousemove', (e) => {
    xValue = e.clientX - window.innerWidth / 2;
    yValue = e.clientY - window.innerHeight / 2;

    rotateDegree = (xValue / (window.innerWidth / 2)) * 20;

    update(e.clientX);
})