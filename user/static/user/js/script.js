document.addEventListener("DOMContentLoaded", function (event) {
    
    document.querySelector('.img__btn').addEventListener('click', function () {
        document.querySelector('.cont').classList.toggle('s--signup');
    });

    // Seleciona todos os pares de ícones e campos de senha
    document.querySelectorAll('.toggle-password').forEach(function (eyeIcon) {
        const passwordInput = eyeIcon.previousElementSibling; // Encontra o campo de senha próximo do ícone
        const eyeSlashIcon = eyeIcon.nextElementSibling; // O ícone de olho cortado

        // Alterna a visibilidade da senha quando o ícone de olho for clicado
        eyeIcon.addEventListener('click', function () {
            const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordInput.setAttribute('type', type);

            // Alterna a visibilidade dos ícones
            eyeIcon.hidden = true;
            eyeSlashIcon.hidden = false;
        });

        // Alterna a visibilidade novamente ao clicar no ícone de olho cortado
        eyeSlashIcon.addEventListener('click', function () {
            passwordInput.setAttribute('type', 'password');

            // Alterna a visibilidade dos ícones
            eyeIcon.hidden = false;
            eyeSlashIcon.hidden = true;
        });
    });

    


});


function closeMessage(element){
    var alertBox = element.parentElement;
    alertBox.remove();
}