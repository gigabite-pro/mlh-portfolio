window.onload = () => {
    const theme = localStorage.getItem("theme");
    if (theme === "dark") {
        gsap.to("body", { "--black": "white" });
        gsap.to("body", { "--white": "#000" });
        gsap.to("#moon", {
            display: "block",
            opacity: 1,
            scale: 1,
            duration: 0.1,
        });
    } else {
        gsap.to("body", { "--black": "#000" });
        gsap.to("body", { "--white": "white" });
        gsap.to("#sun", {
            display: "block",
            opacity: 1,
            scale: 1,
            duration: 0.1,
        });
    }

    var elements = document.getElementsByClassName("typewrite");
    for (var i = 0; i < elements.length; i++) {
        var toRotate = elements[i].getAttribute("data-type");
        var period = elements[i].getAttribute("data-period");
        if (toRotate) {
            new TxtType(elements[i], JSON.parse(toRotate), period);
        }
    }
    // INJECT CSS
    var css = document.createElement("style");
    css.innerHTML =
        ".typewrite > .wrap { border-right: 0.08em solid var(--black)}";
    document.body.appendChild(css);
};

function handleThemeToggle() {
    const state = localStorage.getItem("theme");
    const timeline = gsap.timeline();
    if (state === "dark") {
        gsap.to("body", { "--black": "#000", duration: 0.5 });
        gsap.to("body", { "--white": "white", duration: 0.5 });
        localStorage.setItem("theme", "light");
        timeline
            .to("#moon", {
                opacity: 0,
                duration: 0.1,
                scale: 0,
                display: "none",
            })
            .to("#sun", {
                opacity: 1,
                duration: 0.1,
                scale: 1,
                display: "block",
            });
        pJSDom[0].pJS.particles.color.value = "#000";
        pJSDom[0].pJS.fn.particlesRefresh();
    } else {
        gsap.to("body", { "--black": "white", duration: 0.5 });
        gsap.to("body", { "--white": "#000", duration: 0.5 });
        localStorage.setItem("theme", "dark");
        timeline
            .to("#sun", {
                opacity: 0,
                duration: 0.1,
                scale: 0,
                display: "none",
            })
            .to("#moon", {
                opacity: 1,
                duration: 0.1,
                scale: 1,
                display: "block",
            });
        pJSDom[0].pJS.particles.color.value = "#fff";
        pJSDom[0].pJS.fn.particlesRefresh();
    }
}
