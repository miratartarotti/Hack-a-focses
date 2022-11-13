var active_sentence = -1;

function reveal(evt) {
    var target = evt.target;
    var sentence_id = -1;
    if (target.tagName.toUpperCase() == "A") {
        sentence_id = target.id;
    } else if (target.tagName.toUpperCase() == "IMG") {
        sentence_id = target.parentElement.id;
    }

    console.log(sentence_id);
    active_sentence = sentence_id;
    // show button to allow creating comments
    document.getElementById("create-comment").hidden = false;

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


document.getElementById("create-comment").onclick = function() {
    var form = document.getElementById("comment-form");
    if (form.hidden) {
        form.hidden = false;
    } else
    {
        var author = document.getElementById("comment-form-author").value;
        document.getElementById("comment-form-author").value = "";
        var comment = document.getElementById("comment-form-comment").value;
        document.getElementById("comment-form-comment").value = "";

        const xhttp = new XMLHttpRequest();
        xhttp.onload = function() {
            console.log(this.responseText);
            if (this.responseText == "OK") {
                document.getElementById(active_sentence).click();
            } else {
                alert("Could not submit comment :(")
            }
        }
        xhttp.open("POST", `/api/notes/${lecture_notes}/comments/${active_sentence}/add`, true);
        xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        xhttp.send(`author=${author}&comment=${comment}`);

        form.hidden = true;
    }
};
