function tag(dom) {
    var value = dom.getAttribute('name')
    var txt = document.getElementById('technology').value
    document.getElementById('technology').value = txt + value
}