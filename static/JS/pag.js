//Obtenemos la URL actual
const currentUrl = window.location.href;

const links = document.querySelectorAll(".nav-links a");

//Itera sobre los enlaces
links.forEach(link => {
    const linkPath = new URL(link.href).pathname;
    const currentPath = new URL(currentUrl).pathname;

    //compara los pathnames
    if (linkPath === currentPath) {
        link.classList.add("active");
    } else {
        link.classList.remove("active"); //cambio de página
    }
});