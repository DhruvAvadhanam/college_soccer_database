function openPopup(team) {
    const id = 'popup-' + team.replaceAll(' ', '-');
    document.getElementById(id).classList.add('active');
}
function closePopup(team) {
    const id = 'popup-' + team.replaceAll(' ', '-');
    document.getElementById(id).classList.remove('active');
}