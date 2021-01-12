const wppButton = document.getElementById('wpp-logo');
const wppList = document.getElementById('wpp-list');

wppButton.addEventListener('click', () => {
    wppList.classList.toggle('wpp-static__links--active')
})
