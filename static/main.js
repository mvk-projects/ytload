function submitForm(e) {
    var text = document.getElementById("search-bar").value;
    var formats = document.getElementsByName('switch-two');
    var selectedFormat = ""
    for (i = 0; i < formats.length; i++) {
        if (formats[i].checked) selectedFormat = (formats[i].value == "haq") ? "Audio
    Only":"Video + Audio"; } $.getJSON('https://noembed.com/embed', {format: 'json' , url: text}, function (data) {
        if (!confirm('Do you want to Download : ' + data.title + ' ? \n\nFormat : ' + selectedFormat)) {
            e.preventDefault();
        }
        else {
            document.getElementById("formclass").submit();
        }
    });
}

function matchYoutubeUrl(url) {
    var p = /^(?:https?:\/\/)?(?:m\.|www\.)?(?:youtu\.be\/|youtube\.com\/(?:embed\/|v\/|watch\?v=|watch\?.+&v=))((\w|-){11})(?:\S+)?$/;
    if (url.match(p)) {
        return url.match(p)[1];
    }
    return false;
}


async function paste(input) {
    const text = await navigator.clipboard.readText();
    if (matchYoutubeUrl(text)) {
        input.value = text;
    }
}