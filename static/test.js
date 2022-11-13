function reveal(evt) {
    var sentence_id = evt.target.id;

    const xhttp = new XMLHttpRequest();
    xhttp.onload = function() {
        document.getElementById("comment-contents").innerHTML = this.responseText;
    }
    xhttp.open("GET", `/api/notes/${lecture_notes}/comments/${sentence_id}`, true);
    xhttp.send();
}


var sentence_tags = document.getElementsByClassName("sentence");
for (var a = 0; a < sentence_tags.length; a++) {
    sentence_tags[a].onclick = reveal;
}
