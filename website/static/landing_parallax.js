const parallax_el = document.querySelectorAll('.landing_parallax')

let xValue = 0, yValue = 0;
let vw = window.innerWidth,
    vh = window.innerHeight;

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
        }vh)) rotateY(${rotateDegree * rotateSpeed}deg) translateY(calc(-50% + ${
            yValue*speedy
        }vh)) perspective(2300px) translateZ(${zValue * speedz}vh)`;
    })
}

// update(0)

window.addEventListener('mousemove', (e) => {
    // xValue = e.clientX - window.innerWidth / 2;
    // yValue = e.clientY - window.innerHeight / 2;
    vw = window.innerWidth;
    vh = window.innerHeight;
    xValue = e.clientX / vw * 100 - 50; // Multiplying by 100 to get percentage 
    yValue = e.clientY / vh * 100 - 50; // Multiplying by 100 to get percentage 

    rotateDegree = (xValue / (window.innerWidth / 2)) * 20;

    update(e.clientX);
})